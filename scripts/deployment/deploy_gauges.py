from brownie import chain
import json
import os
from datetime import datetime
from .helpers.chain_to_name import chain_to_name
from .StakingSystem import StakingSystem, get_deployer


def deploy_gauges():
    network = chain_to_name[chain.id]
    deployer = get_deployer()
    system = StakingSystem.load(
        deployer,
        f"deployed/{network}_dependencies.json",
        f"deployed/{network}_system.json",
    )

    f = open(f"deployed/{network}_vaults.json", "r")
    vaults = json.loads(f.read())
    f.close()

    # f = open(f"deploy_config_{network}.json", "r")
    # deploy_config = json.loads(f.read())
    # f.close()

    # weights = deploy_config["gauge_weights"]
    gauge_addresses = {}
    gauges = []

    for sym, vault in vaults.items():
        print(f"Deploying gauge for {sym}")
        gauge = system.deploy_gauge(vault["address"])
        system.add_gauge(gauge, vault["gauge"])
        gauges.append(gauge)
        gauge_addresses[sym] = {
            "vault": vault["address"],
            "gauge": gauge.address,
            "weight": vault["weight"],
        }

    f = open(f"deployed/{network}_gauges_deployed_{datetime.utcnow().isoformat()}.json", "w")
    f.write(json.dumps(gauge_addresses, indent=2))
    f.close()

    if os.path.isfile(f"deployed/{network}_gauges_deployed.json"):
        f = open(f"deployed/{network}_gauges_deployed.json", "r")
        last_addresses = json.loads(f.read())
        f.close()
    else:
        last_addresses = {}
    gauges_addresses = {**last_addresses, **gauge_addresses}
    f = open(f"deployed/{network}_gauges_deployed.json", "w")
    f.write(json.dumps(gauges_addresses, indent=2))
    f.close()
    return gauges


def main():
    deploy_gauges()
