from collections import deque
from enum import IntEnum

import pytest
from brownie import chain
from brownie.test import given, strategy
from hypothesis import settings

# number of liquidity gauges
GAUGE_COUNT = 100
# number of gauge types (distributed evenly across the gauges)
TYPE_COUNT = 5
# number of rounds per test - every gauge will be interacted with once per round
TEST_ROUNDS = 40
# number of times the test is run
TEST_RUNS = 1
# number of users in the test
USER_COUNT = 1000


class ActionEnum(IntEnum):
    """
    Enum of possible gauge actions in a test round.
    """

    deposit = 0
    withdraw = 1
    mint = 2
    noop = 3

    @classmethod
    def get_action(cls, value: int):
        value = len(cls) * value // (GAUGE_COUNT + 1)
        return cls(value)


@pytest.fixture(scope="module", autouse=True)
def setup(accounts, gauge_controller, lixir_vault, distributor, token, voting_escrow):
    while len(accounts) < USER_COUNT:
        accounts.add()

    for i in range(len(accounts)):
        lixir_vault.deposit(10**23, 0, 0, 0, accounts[i], chain.time() + 10**18, {"from": accounts[i]})
        token.transfer(accounts[i], 10**22, {"from": accounts[0]})
        token.approve(voting_escrow, 10 ** 23, {"from": accounts[i]})
        voting_escrow.create_lock(10 ** 22, chain.time() + 86400 * 365 * 2, {"from": accounts[i]})

    for i in range(TYPE_COUNT):
        gauge_controller.add_type(i, 10 ** 18, {"from": accounts[0]})


@pytest.fixture(scope="module")
def gauges(VaultGauge, accounts, gauge_controller, lixir_vault, distributor, setup):
    # deploy `GAUGE_COUNT` liquidity gauges and return them as a list
    gauges = []
    for i in range(GAUGE_COUNT):
        contract = VaultGauge.deploy(lixir_vault, distributor, accounts[0], {"from": accounts[0]})
        gauge_controller.add_gauge(contract, i % TYPE_COUNT, {"from": accounts[0]})
        gauges.append(contract)

    yield gauges


@given(st_actions=strategy(f"uint[{GAUGE_COUNT}]", max_value=GAUGE_COUNT, unique=True))
@settings(max_examples=TEST_RUNS)
def test_scalability(accounts, gauges, gauge_controller, lixir_vault, distributor, st_actions):

    # handle actions is a deque, so we can rotate it to ensure each gauge has multiple actions
    st_actions = deque(st_actions)

    # convert accounts to a deque so we can rotate it to evenly spread actions across accounts
    action_accounts = deque(accounts)

    # for voting we use a seperate deque that only rotates once per test round
    # this way accounts never vote too often
    last_voted = deque(accounts)

    balances = {i: [0] * len(accounts) for i in gauges}

    for i in range(TEST_ROUNDS):
        print(f"Round {i}")
        # rotate voting account and actions
        last_voted.rotate()
        st_actions.rotate()

        # sleep just over a day between each round
        chain.sleep(86401)

        for gauge, action in zip(gauges, st_actions):
            action = ActionEnum.get_action(action)

            action_accounts.rotate()
            acct = action_accounts[0]
            idx = list(accounts).index(acct)

            if action == ActionEnum.deposit:
                lixir_vault.approve(gauge, 10 ** 17, {"from": acct})
                gauge.deposit(10 ** 17, {"from": acct})
                balances[gauge][idx] += 10 ** 17

            elif action == ActionEnum.withdraw:
                amount = balances[gauge][idx]
                gauge.withdraw(amount, {"from": acct})
                balances[gauge][idx] = 0

            elif action == ActionEnum.mint:
                distributor.distribute(gauge, {"from": acct})
