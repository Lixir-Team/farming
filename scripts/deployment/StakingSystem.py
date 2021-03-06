from collections import namedtuple
import json
from brownie import (
    GaugeController,
    VaultGauge,
    LixirVault,
    LixirRegistry,
    LixDistributor,
    VotingEscrow,
    FeeDistributor,
    accounts,
    chain,
    web3,
)
from brownie.network.contract import Contract
from brownie.network import accounts
from .helpers.chain_to_name import chain_to_name
from dotenv import load_dotenv

load_dotenv()
import os

StakingDependenciesConfig = namedtuple("LixirDependenciesConfig", ["lix", "registry"])

StakingSystemConfig = namedtuple(
    "StakingSystemConfig",
    [
        "escrow",
        "fee_distributor",
        "gauge_controller",
        "lix_distributor",
    ],
)


class StakingSystem:
    __create_key = object()

    def __init__(
        self,
        create_key,
        deployer,
        dep_config: StakingDependenciesConfig,
        system_config: StakingSystemConfig,
    ):
        assert create_key == self.__create_key

        # dep_config
        # idk if we need self.registry = dep_config.registry
        self.lix = dep_config.lix
        self.registry = dep_config.registry
        self.deployer = deployer

        # system config
        self.escrow = system_config.escrow
        self.fee_distributor = system_config.fee_distributor
        self.gauge_controller = system_config.gauge_controller
        self.lix_distributor = system_config.lix_distributor

    def deploy_gauge(self, lp_token):
        return VaultGauge.deploy(
            lp_token,
            self.lix_distributor,
            self.registry,
            {"from": self.deployer, "gas": 5000000, "priority_fee": chain.priority_fee},
        )

    def add_gauge(self, gauge, weight):
        return self.gauge_controller.add_gauge(
            gauge,
            0,
            weight,
            {"from": self.deployer, "gas": 5000000, "priority_fee": chain.priority_fee},
        )

    @classmethod
    def deploy(cls, lix, registry, deployer):
        escrow = VotingEscrow.deploy(
            registry,
            lix,
            "Vote-escrowed LIX",
            "veLIX",
            "veLIX_0.99",
            {"from": deployer, "priority_fee": chain.priority_fee},
        )
        # fee_distributor = FeeDistributor.deploy(escrow, 0, lix, fee_dist_admin, emergency_return, {"from": deployer, "priority_fee": chain.priority_fee})
        gauge_controller = GaugeController.deploy(
            registry, lix, escrow, {"from": deployer, "priority_fee": chain.priority_fee}
        )
        lix_distributor = LixDistributor.deploy(
            lix, gauge_controller, registry, {"from": deployer, "priority_fee": chain.priority_fee}
        )  # should I

        gauge_controller.add_type(b"Vaults", {"from": deployer, "priority_fee": chain.priority_fee})
        gauge_controller.change_type_weight(
            0, 10 ** 18, {"from": deployer, "priority_fee": chain.priority_fee}
        )
        # lix.approve(distributor, 6000000, {"from": deployer})
        # distributor.set_initial_params(6000000, {"from": deployer})
        dep_config = StakingDependenciesConfig(lix, registry)
        staking_config = StakingSystemConfig(escrow, None, gauge_controller, lix_distributor)

        return StakingSystem(cls.__create_key, deployer, dep_config, staking_config)

    @classmethod
    def connect(
        cls,
        deployer,
        dep_config: StakingDependenciesConfig,
        config: StakingSystemConfig,
    ):
        return StakingSystem(
            cls.__create_key,
            deployer,
            dep_config,
            StakingSystemConfig(
                escrow=VotingEscrow.at(config.escrow),
                fee_distributor=FeeDistributor.at(config.fee_distributor)
                if config.fee_distributor
                else None,
                gauge_controller=GaugeController.at(config.gauge_controller),
                lix_distributor=LixDistributor.at(config.lix_distributor),
            ),
        )

    @classmethod
    def load(cls, deployer, dependencies_file_path, system_file_path):
        deps = load_dependencies(dependencies_file_path)
        f = open(system_file_path, "r")
        system_config = json.loads(f.read())
        f.close()
        system = StakingSystemConfig(
            escrow=system_config["escrow"],
            fee_distributor=system_config["fee_distributor"],
            gauge_controller=system_config["gauge_controller"],
            lix_distributor=system_config["lix_distributor"],
        )
        return cls.connect(deployer, deps, system)


mnem_accounts = accounts.from_mnemonic(os.getenv("MNEMONIC"), 10)


def try_get_signer(account):
    try:
        return next(v for v in mnem_accounts if v == account)
    except:
        return account


def get_deployer():
    network = chain_to_name[chain.id]
    if network == "ganache":
        return accounts[0]
    f = open(f"deploy_config_{network}.json", "r")
    deploy_config = json.loads(f.read())
    f.close()
    deployer = try_get_signer(deploy_config["deployer"])
    return deployer


def connect_dependencies(dep_config: StakingDependenciesConfig):
    lix_address, registry_address = dep_config
    f = open("build/contracts/ERC20.json", "r")
    lix_artifact = json.loads(f.read())
    f.close()
    lix = Contract.from_abi("LIX", lix_address, lix_artifact["abi"])

    if registry_address:
        f = open("build/contracts/LixirRegistry.json", "r")
        registry_artifact = json.loads(f.read())
        f.close()
        registry = Contract.from_abi("LixirRegistry", registry_address, registry_artifact["abi"])
    else:
        registry = None

    return StakingDependenciesConfig(lix, registry)


def load_dependencies(file_path):
    f = open(file_path, "r")
    dependencies = json.loads(f.read())
    f.close()
    return connect_dependencies(
        StakingDependenciesConfig(dependencies["lix"], dependencies["registry"])
    )
