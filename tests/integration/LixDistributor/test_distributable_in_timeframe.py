import pytest
from brownie.test import given, strategy

from tests.conftest import YEAR_1_SUPPLY, approx

YEAR = 365 * 86400

@pytest.fixture(scope="module", autouse=True)
def initial_setup(chain, distributor):
    chain.sleep(86401)
    distributor.update_mining_parameters()


@given(time=strategy("decimal", min_value=1, max_value=7))
def test_distributable_in_timeframe(accounts, distributor, theoretical_distribution, time, chain):
    t0 = distributor.start_epoch_time()
    chain.sleep(int(10 ** time))
    chain.mine()
    t1 = chain[-1].timestamp
    if t1 - t0 >= YEAR:
        distributor.update_mining_parameters({"from": accounts[0]})

    t1 = chain[-1].timestamp
    available_to_distribute = distributor.available_to_distribute()
    distributable = distributor.distributable_in_timeframe(t0, t1)

    assert available_to_distribute >= distributable  # Should only round down, not up
    if t1 == t0:
        assert distributable == 0
    else:
        assert available_to_distribute / distributable - 1 < 1e-7

    assert approx(theoretical_distribution(), available_to_distribute, 1e-16)


@given(time1=strategy("uint", max_value=YEAR), time2=strategy("uint", max_value=YEAR))
def test_random_range_year_one(distributor, time1, time2):
    creation_time = distributor.start_epoch_time()
    start, end = sorted((creation_time + time1, creation_time + time2))
    rate = YEAR_1_SUPPLY // YEAR

    assert distributor.distributable_in_timeframe(start, end) == rate * (end - start)


@given(start=strategy("uint", max_value=YEAR * 6), duration=strategy("uint", max_value=YEAR))
def test_random_range_multiple_epochs(distributor, chain, accounts, start, duration):
    creation_time = distributor.start_epoch_time()
    start += creation_time
    end = duration + start
    start_epoch = (start - creation_time) // YEAR
    end_epoch = (end - creation_time) // YEAR
    rate = int(YEAR_1_SUPPLY // YEAR / (15/13) ** start_epoch)

    for i in range(end_epoch):
        chain.sleep(YEAR)
        chain.mine()
        distributor.update_mining_parameters({"from": accounts[0]})

    if start_epoch == end_epoch:
        assert approx(distributor.distributable_in_timeframe(start, end), rate * (end - start), 1e-15)
    else:
        assert distributor.distributable_in_timeframe(start, end) < rate * end


# this test is nondeterministic because of chain.time() so don't worry if it doesn't pass
# should only be off by 24090563165905631 (one LIX/second)
@given(duration=strategy("uint", min_value=1, max_value=YEAR))
def test_available_to_distribute(chain, web3, distributor, duration):
    creation_time = distributor.start_epoch_time()
    initial_supply = distributor.available_to_distribute()
    rate = distributor.rate()
    chain.sleep(duration)
    chain.mine()

    expected = initial_supply + (web3.eth.getBlock("latest")["timestamp"] - creation_time) * rate
    actual = distributor.available_to_distribute()
    assert actual == expected or actual + rate == expected
