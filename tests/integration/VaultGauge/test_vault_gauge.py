from random import random, randrange

from tests.conftest import YEAR, approx

MAX_UINT256 = 2 ** 256 - 1
WEEK = 7 * 86400


def test_gauge_integral(accounts, chain, lixir_vault, distributor, token, vault_gauge, gauge_controller):
    alice, bob = accounts[:2]

    # Wire up Gauge to the controller to have proper rates and stuff
    gauge_controller.add_type(b"Liquidity", {"from": alice})
    gauge_controller.change_type_weight(0, 10 ** 18, {"from": alice})
    gauge_controller.add_gauge(vault_gauge.address, 0, 10 ** 18, {"from": alice})

    alice_staked = 0
    bob_staked = 0
    integral = 0  # ∫(balance * rate(t) / totalSupply(t) dt)
    checkpoint = chain[-1].timestamp
    checkpoint_rate = distributor.rate()
    checkpoint_supply = 0
    checkpoint_balance = 0

    # Let Alice and Bob have about the same token amount
    # lixir_vault.transfer(bob, lixir_vault.balanceOf(alice) // 2, {"from": alice})
    lixir_vault.deposit(10 ** 21, 0, 0, 0, alice, chain.time() + 10**18, {"from": alice})
    lixir_vault.deposit(10 ** 21, 0, 0, 0, bob, chain.time() + 10**18, {"from": bob})
    
    def update_integral():
        nonlocal checkpoint, checkpoint_rate, integral, checkpoint_balance, checkpoint_supply

        t1 = chain[-1].timestamp
        rate1 = distributor.rate()
        t_epoch = distributor.start_epoch_time()
        if checkpoint >= t_epoch:
            rate_x_time = (t1 - checkpoint) * rate1
        else:
            rate_x_time = (t_epoch - checkpoint) * checkpoint_rate + (t1 - t_epoch) * rate1
        if checkpoint_supply > 0:
            integral += rate_x_time * checkpoint_balance // checkpoint_supply
        checkpoint_rate = rate1
        checkpoint = t1
        checkpoint_supply = vault_gauge.totalSupply()
        checkpoint_balance = vault_gauge.balanceOf(alice)

    # Now let's have a loop where Bob always deposit or withdraws,
    # and Alice does so more rarely
    for i in range(40):
        is_alice = random() < 0.2
        dt = randrange(1, YEAR // 5)
        chain.sleep(dt)
        chain.mine()

        # For Bob
        is_withdraw = (i > 0) * (random() < 0.5)
        print("Bob", "withdraws" if is_withdraw else "deposits")
        if is_withdraw:
            amount = randrange(1, vault_gauge.balanceOf(bob) + 1)
            vault_gauge.withdraw(amount, {"from": bob})
            update_integral()
            bob_staked -= amount
        else:
            amount = randrange(1, lixir_vault.balanceOf(bob) // 10 + 1)
            lixir_vault.approve(vault_gauge.address, amount, {"from": bob})
            vault_gauge.deposit(amount, {"from": bob})
            update_integral()
            bob_staked += amount

        if is_alice:
            # For Alice
            is_withdraw_alice = (vault_gauge.balanceOf(alice) > 0) * (random() < 0.5)
            print("Alice", "withdraws" if is_withdraw_alice else "deposits")

            if is_withdraw_alice:
                amount_alice = randrange(1, vault_gauge.balanceOf(alice) // 10 + 1)
                vault_gauge.withdraw(amount_alice, {"from": alice})
                update_integral()
                alice_staked -= amount_alice
            else:
                amount_alice = randrange(1, lixir_vault.balanceOf(alice) + 1)
                lixir_vault.approve(vault_gauge.address, amount_alice, {"from": alice})
                vault_gauge.deposit(amount_alice, {"from": alice})
                update_integral()
                alice_staked += amount_alice

        # Checking that updating the checkpoint in the same second does nothing
        # Also everyone can update: that should make no difference, too
        if random() < 0.5:
            vault_gauge.user_checkpoint(alice, {"from": alice})
        if random() < 0.5:
            vault_gauge.user_checkpoint(bob, {"from": bob})

        assert vault_gauge.balanceOf(alice) == alice_staked
        assert vault_gauge.balanceOf(bob) == bob_staked
        assert vault_gauge.totalSupply() == alice_staked + bob_staked

        dt = randrange(1, YEAR // 20)
        chain.sleep(dt)
        chain.mine()

        vault_gauge.user_checkpoint(alice, {"from": alice})
        update_integral()
        print(i, dt / 86400, integral, vault_gauge.integrate_fraction(alice))
        assert approx(vault_gauge.integrate_fraction(alice), integral, 1e-15)


def test_mining_with_votelock(
    accounts,
    chain,
    history,
    lixir_vault,
    token,
    vault_gauge,
    gauge_controller,
    voting_escrow,
):
    alice, bob = accounts[:2]
    chain.sleep(2 * WEEK + 5)

    # Wire up Gauge to the controller to have proper rates and stuff
    gauge_controller.add_type(b"Liquidity", {"from": alice})
    gauge_controller.change_type_weight(0, 10 ** 18, {"from": alice})
    gauge_controller.add_gauge(vault_gauge.address, 0, 10 ** 18, {"from": alice})

    # Prepare tokens
    token.transfer(bob, 10 ** 20, {"from": alice})
    lixir_vault.deposit(10 ** 21, 0, 0, 0, alice, chain.time() + 10**18, {"from": alice})
    lixir_vault.deposit(10 ** 21, 0, 0, 0, bob, chain.time() + 10**18, {"from": bob})
    token.approve(voting_escrow, MAX_UINT256, {"from": alice})
    token.approve(voting_escrow, MAX_UINT256, {"from": bob})
    # lixir_vault.transfer(bob, lixir_vault.balanceOf(alice) // 2, {"from": alice})
    lixir_vault.approve(vault_gauge.address, MAX_UINT256, {"from": alice})
    lixir_vault.approve(vault_gauge.address, MAX_UINT256, {"from": bob})

    # Alice deposits to escrow. She now has a BOOST
    t = chain[-1].timestamp
    voting_escrow.create_lock(10 ** 20, t + 2 * WEEK, {"from": alice})

    # Alice and Bob deposit some liquidity
    vault_gauge.deposit(10 ** 21, {"from": alice})
    vault_gauge.deposit(10 ** 21, {"from": bob})

    # Time travel and checkpoint
    chain.sleep(4 * WEEK)
    alice.transfer(alice, 1)
    while True:
        vault_gauge.user_checkpoint(alice, {"from": alice})
        vault_gauge.user_checkpoint(bob, {"from": bob})
        if chain[-1].timestamp != chain[-2].timestamp:
            chain.undo(2)
        else:
            break

    # 4 weeks down the road, balanceOf must be 0
    assert voting_escrow.balanceOf(alice) == 0
    assert voting_escrow.balanceOf(bob) == 0

    # Alice earned 2.5 times more CRV because she vote-locked her CRV
    rewards_alice = vault_gauge.integrate_fraction(alice)
    rewards_bob = vault_gauge.integrate_fraction(bob)
    assert approx(rewards_alice / rewards_bob, 2.5, 1e-5)

    # Time travel / checkpoint: no one has CRV vote-locked
    chain.sleep(4 * WEEK)
    alice.transfer(alice, 1)
    voting_escrow.withdraw({"from": alice})
    while True:
        vault_gauge.user_checkpoint(alice, {"from": alice})
        vault_gauge.user_checkpoint(bob, {"from": bob})
        if chain[-1].timestamp != chain[-2].timestamp:
            chain.undo(2)
        else:
            break
    old_rewards_alice = rewards_alice
    old_rewards_bob = rewards_bob

    # Alice earned the same as Bob now
    rewards_alice = vault_gauge.integrate_fraction(alice)
    rewards_bob = vault_gauge.integrate_fraction(bob)
    d_alice = rewards_alice - old_rewards_alice
    d_bob = rewards_bob - old_rewards_bob
    assert d_alice == d_bob

    # Both Alice and Bob votelock
    while True:
        t = chain[-1].timestamp
        voting_escrow.create_lock(10 ** 20, t + 2 * WEEK, {"from": alice})
        voting_escrow.create_lock(10 ** 20, t + 2 * WEEK, {"from": bob})
        if chain[-1].timestamp != chain[-2].timestamp:
            chain.undo(2)
        else:
            break

    # Time travel / checkpoint: no one has CRV vote-locked
    chain.sleep(4 * WEEK)
    alice.transfer(alice, 1)
    voting_escrow.withdraw({"from": alice})
    voting_escrow.withdraw({"from": bob})
    while True:
        vault_gauge.user_checkpoint(alice, {"from": alice})
        vault_gauge.user_checkpoint(bob, {"from": bob})
        if chain[-1].timestamp != chain[-2].timestamp:
            chain.undo(2)
        else:
            break
    old_rewards_alice = rewards_alice
    old_rewards_bob = rewards_bob

    # Alice earned the same as Bob now
    rewards_alice = vault_gauge.integrate_fraction(alice)
    rewards_bob = vault_gauge.integrate_fraction(bob)
    d_alice = rewards_alice - old_rewards_alice
    d_bob = rewards_bob - old_rewards_bob
    assert d_alice == d_bob
