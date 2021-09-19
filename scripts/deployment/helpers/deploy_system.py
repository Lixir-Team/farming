from tests.conftest import fee_distributor
from .chain_to_name import chain_to_name
from brownie import chain
from ..StakingSystem import (
    StakingSystem,
    get_deployer,
    connect_dependencies,
    StakingDependenciesConfig,
    get_deployer,
)
import json


def deploy_system():
    network = chain_to_name[chain.id]
    deployer = get_deployer()
    f = open(f"deployed/{network}_dependencies.json", "r")
    dependencies = json.loads(f.read())
    f.close()
    lix, registry = connect_dependencies(
        StakingDependenciesConfig(dependencies["lix"], dependencies["registry"])
    )
    staking_system = StakingSystem.deploy(lix, registry, deployer)
    f = open(f"deployed/{network}_system.json", "w")
    f.write(
        json.dumps(
            {
                "lix": str(lix),
                "registry": str(registry),
                "escrow": str(staking_system.escrow),
                "fee_distributor": str(staking_system.fee_distributor)
                if staking_system.fee_distributor
                else None,
                "gauge_controller": str(staking_system.gauge_controller),
                "lix_distributor": str(staking_system.lix_distributor),
            },
            indent=2,
        )
    )
    f.close()
    return staking_system
