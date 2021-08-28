import pytest
from brownie.test import given, strategy
from hypothesis import settings

from tests.conftest import approx

WEEK = 86400 * 7
MONTH = 86400 * 30


@pytest.fixture(scope="module", autouse=True)
def minter_setup(accounts, lixir_vault, gauge_controller, vault_gauge, chain):
    # mint test vault tokens to accounts[0] 
    lixir_vault.deposit(10**22, 0, 0, 0, accounts[0], chain.time() + 10**18, {"from": accounts[0]})

    # set type
    gauge_controller.add_type(b"Liquidity", 10 ** 18, {"from": accounts[0]})

    # add gauge
    gauge_controller.add_gauge(vault_gauge, 0, 10 ** 19, {"from": accounts[0]})

    # transfer tokens
    for acct in accounts[1:4]:
        lixir_vault.transfer(acct, 1e18, {"from": accounts[0]})
        lixir_vault.approve(vault_gauge, 1e18, {"from": acct})


@given(st_duration=strategy("uint[3]", min_value=WEEK, max_value=MONTH, unique=True))
@settings(max_examples=30)
def test_duration(accounts, chain, vault_gauge, distributor, st_duration, token):
    accts = accounts[1:]
    chain.sleep(7 * 86400)

    deposit_time = []
    for i in range(3):
        vault_gauge.deposit(10 ** 18, {"from": accts[i]})
        deposit_time.append(chain[-1].timestamp)

    durations = []
    balances = []
    for i in range(3):
        chain.sleep(st_duration[i])
        vault_gauge.withdraw(10 ** 18, {"from": accts[i]})
        durations.append(chain[-1].timestamp - deposit_time[i])
        distributor.distribute(vault_gauge, {"from": accts[i]})
        balances.append(token.balanceOf(accts[i]))

    total_distributed = sum(balances)
    weight1 = durations[0]
    weight2 = weight1 + (durations[1] - durations[0]) * 1.5
    weight3 = weight2 + (durations[2] - durations[1]) * 3
    total_weight = weight1 + weight2 + weight3

    assert approx(balances[0] / total_distributed, weight1 / total_weight, 1e-4)
    assert approx(balances[1] / total_distributed, weight2 / total_weight, 1e-4)
    assert approx(balances[2] / total_distributed, weight3 / total_weight, 1e-4)


@given(st_amounts=strategy("uint[3]", min_value=10 ** 17, max_value=10 ** 18, unique=True))
@settings(max_examples=30)
def test_amounts(accounts, chain, vault_gauge, distributor, token, st_amounts):
    accts = accounts[1:]

    deposit_time = []
    for i in range(3):
        vault_gauge.deposit(st_amounts[i], {"from": accts[i]})
        deposit_time.append(chain[-1].timestamp)

    chain.sleep(MONTH)
    balances = []
    for i in range(3):
        vault_gauge.withdraw(st_amounts[i], {"from": accts[i]})

    for i in range(3):
        distributor.distribute(vault_gauge, {"from": accts[i]})
        balances.append(token.balanceOf(accts[i]))

    total_deposited = sum(st_amounts)
    total_minted = sum(balances)

    assert approx(balances[0] / total_minted, st_amounts[0] / total_deposited, 1e-4)
    assert approx(balances[1] / total_minted, st_amounts[1] / total_deposited, 1e-4)
    assert approx(balances[2] / total_minted, st_amounts[2] / total_deposited, 1e-4)
