/* Autogenerated file. Do not edit manually. */
/* tslint:disable */
/* eslint-disable */

import { Signer, utils, Contract, ContractFactory, Overrides } from "ethers";
import { Provider, TransactionRequest } from "@ethersproject/providers";
import type {
  LixDistributor,
  LixDistributorInterface,
} from "../LixDistributor";

const _abi = [
  {
    anonymous: false,
    inputs: [
      {
        indexed: false,
        name: "time",
        type: "uint256",
      },
      {
        indexed: false,
        name: "rate",
        type: "uint256",
      },
      {
        indexed: false,
        name: "supply",
        type: "uint256",
      },
    ],
    name: "UpdateMiningParameters",
    type: "event",
  },
  {
    anonymous: false,
    inputs: [
      {
        indexed: true,
        name: "recipient",
        type: "address",
      },
      {
        indexed: false,
        name: "gauge",
        type: "address",
      },
      {
        indexed: false,
        name: "distributed",
        type: "uint256",
      },
    ],
    name: "Distributed",
    type: "event",
  },
  {
    inputs: [
      {
        name: "_lix",
        type: "address",
      },
      {
        name: "_controller",
        type: "address",
      },
      {
        name: "_admin",
        type: "address",
      },
      {
        name: "_emergency_return",
        type: "address",
      },
    ],
    outputs: [],
    stateMutability: "nonpayable",
    type: "constructor",
  },
  {
    gas: 3838,
    inputs: [],
    name: "available_to_distribute",
    outputs: [
      {
        name: "",
        type: "uint256",
      },
    ],
    stateMutability: "view",
    type: "function",
  },
  {
    gas: 148808,
    inputs: [],
    name: "update_mining_parameters",
    outputs: [],
    stateMutability: "nonpayable",
    type: "function",
  },
  {
    gas: 149663,
    inputs: [],
    name: "start_epoch_time_write",
    outputs: [
      {
        name: "",
        type: "uint256",
      },
    ],
    stateMutability: "nonpayable",
    type: "function",
  },
  {
    gas: 149866,
    inputs: [],
    name: "future_epoch_time_write",
    outputs: [
      {
        name: "",
        type: "uint256",
      },
    ],
    stateMutability: "nonpayable",
    type: "function",
  },
  {
    gas: 2216141,
    inputs: [
      {
        name: "start",
        type: "uint256",
      },
      {
        name: "end",
        type: "uint256",
      },
    ],
    name: "distributable_in_timeframe",
    outputs: [
      {
        name: "",
        type: "uint256",
      },
    ],
    stateMutability: "view",
    type: "function",
  },
  {
    gas: 396420,
    inputs: [
      {
        name: "gauge_addr",
        type: "address",
      },
    ],
    name: "distribute",
    outputs: [],
    stateMutability: "nonpayable",
    type: "function",
  },
  {
    gas: 2778088,
    inputs: [
      {
        name: "gauge_addrs",
        type: "address[8]",
      },
    ],
    name: "dist_many",
    outputs: [],
    stateMutability: "nonpayable",
    type: "function",
  },
  {
    gas: 6776,
    inputs: [
      {
        name: "_coin",
        type: "address",
      },
    ],
    name: "recover_balance",
    outputs: [
      {
        name: "",
        type: "bool",
      },
    ],
    stateMutability: "nonpayable",
    type: "function",
  },
  {
    gas: 1481,
    inputs: [],
    name: "initial_supply",
    outputs: [
      {
        name: "",
        type: "uint256",
      },
    ],
    stateMutability: "view",
    type: "function",
  },
  {
    gas: 1511,
    inputs: [],
    name: "mining_epoch",
    outputs: [
      {
        name: "",
        type: "int128",
      },
    ],
    stateMutability: "view",
    type: "function",
  },
  {
    gas: 1541,
    inputs: [],
    name: "start_epoch_time",
    outputs: [
      {
        name: "",
        type: "uint256",
      },
    ],
    stateMutability: "view",
    type: "function",
  },
  {
    gas: 1571,
    inputs: [],
    name: "rate",
    outputs: [
      {
        name: "",
        type: "uint256",
      },
    ],
    stateMutability: "view",
    type: "function",
  },
  {
    gas: 1601,
    inputs: [],
    name: "lix",
    outputs: [
      {
        name: "",
        type: "address",
      },
    ],
    stateMutability: "view",
    type: "function",
  },
  {
    gas: 1631,
    inputs: [],
    name: "controller",
    outputs: [
      {
        name: "",
        type: "address",
      },
    ],
    stateMutability: "view",
    type: "function",
  },
  {
    gas: 1661,
    inputs: [],
    name: "admin",
    outputs: [
      {
        name: "",
        type: "address",
      },
    ],
    stateMutability: "view",
    type: "function",
  },
  {
    gas: 1691,
    inputs: [],
    name: "emergency_return",
    outputs: [
      {
        name: "",
        type: "address",
      },
    ],
    stateMutability: "view",
    type: "function",
  },
  {
    gas: 2029,
    inputs: [
      {
        name: "arg0",
        type: "address",
      },
      {
        name: "arg1",
        type: "address",
      },
    ],
    name: "distributed",
    outputs: [
      {
        name: "",
        type: "uint256",
      },
    ],
    stateMutability: "view",
    type: "function",
  },
];

const _bytecode =
  "0x740100000000000000000000000000000000000000006020526f7fffffffffffffffffffffffffffffff6040527fffffffffffffffffffffffffffffffff8000000000000000000000000000000060605274012a05f1fffffffffffffffffffffffffdabf41c006080527ffffffffffffffffffffffffed5fa0e000000000000000000000000000000000060a0526080610fd06101403934156100a157600080fd5b6020610fd060c03960c05160205181106100ba57600080fd5b5060206020610fd00160c03960c05160205181106100d757600080fd5b5060206040610fd00160c03960c05160205181106100f457600080fd5b5060206060610fd00160c03960c051602051811061011157600080fd5b506101405160055561016051600655610180516007556101a051600855426201518081818301101561014257600080fd5b808201905090506301e133808082101561015b57600080fd5b808203905090506002557fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff60015560006003556000600455610fb856600436101561000d57610e1a565b600035601c52740100000000000000000000000000000000000000006020526f7fffffffffffffffffffffffffffffff6040527fffffffffffffffffffffffffffffffff8000000000000000000000000000000060605274012a05f1fffffffffffffffffffffffffdabf41c006080527ffffffffffffffffffffffffed5fa0e000000000000000000000000000000000060a052600015610202575b610140526003546101605260045461018052600280546301e133808181830110156100d357600080fd5b80820190509050815550600180546001606051818301806040519013156100f957600080fd5b809190121561010757600080fd5b90509050815550610160511515610129576655963d53f162df610160526101b9565b6101808051610160516301e13380808202821582848304141761014b57600080fd5b8090509050905081818301101561016157600080fd5b808201905090508152506101805160045561016051670de0b6b3a7640000808202821582848304141761019357600080fd5b8090509050905067100348f6ad73627680806101ae57600080fd5b820490509050610160525b61016051600355426101a052610160516101c052610180516101e0527f27e46362a1e6129b6dd539c984ce739291a97128dfcaeca1255e8ac83abd944160606101a0a161014051565b60001561026b575b61014052600454426002548082101561022257600080fd5b80820390509050600354808202821582848304141761024057600080fd5b8090509050905081818301101561025657600080fd5b80820190509050600052600051610140515650005b637b2abd2060005114156102a057341561028457600080fd5b6006580161020a565b610140526101405160005260206000f350005b63d43b40fa60005114156102f15734156102b957600080fd5b6002546301e133808181830110156102d057600080fd5b808201905090504210156102e357600080fd5b600658016100a9565b600050005b63adc4cf43600051141561036d57341561030a57600080fd5b60025461014052610140516301e1338081818301101561032957600080fd5b808201905090504210151561035d5761014051600658016100a9565b6101405260005060025460005260206000f35061036b565b6101405160005260206000f3505b005b63b26b238e600051141561041f57341561038657600080fd5b60025461014052610140516301e133808181830110156103a557600080fd5b80820190509050421015156103f45761014051600658016100a9565b610140526000506002546301e133808181830110156103df57600080fd5b8082019050905060005260206000f35061041d565b610140516301e1338081818301101561040c57600080fd5b8082019050905060005260206000f3505b005b63795f9c1d60005114156106ea57341561043857600080fd5b602435600435111561044957600080fd5b6000610140526002546101605260035461018052610160516301e1338081818301101561047557600080fd5b8082019050905060243511156104ef5761016080516301e1338081818301101561049e57600080fd5b8082019050905081525061018051670de0b6b3a764000080820282158284830414176104c957600080fd5b8090509050905067100348f6ad73627680806104e457600080fd5b820490509050610180525b610160516301e1338081818301101561050757600080fd5b80820190509050602435111561051c57600080fd5b6101a060006103e7818352015b6101605160243510151561064a576024356101c052610160516301e1338081818301101561055657600080fd5b808201905090506101c051111561058b57610160516301e1338081818301101561057f57600080fd5b808201905090506101c0525b6004356101e052610160516301e133808181830110156105aa57600080fd5b808201905090506101e0511015156105c5576106d9566105dd565b610160516101e05110156105dc57610160516101e0525b5b6101408051610180516101c0516101e051808210156105fb57600080fd5b80820390509050808202821582848304141761061657600080fd5b8090509050905081818301101561062c57600080fd5b8082019050905081525061016051600435101515610649576106d9565b5b61016080516301e133808082101561066157600080fd5b808203905090508152506101805167100348f6ad736276808202821582848304141761068c57600080fd5b80905090509050670de0b6b3a764000080806106a757600080fd5b820490509050610180526655963d53f162df6101805111156106c857600080fd5b5b8151600101808352811415610529575b50506101405160005260206000f350005b600015610959575b610180526101405261016052600060206102206024633f9095b76101a052610140516101c0526101bc6006545afa61072957600080fd5b601f3d1161073657600080fd5b60005061022051121561074857600080fd5b6000610160511861075857600080fd5b60206102c06024634b82009361024052610160516102605261025c6000610140515af161078457600080fd5b601f3d1161079157600080fd5b6000506102c05060206103806024630940070761030052610160516103205261031c610140515afa6107c257600080fd5b601f3d116107cf57600080fd5b600050610380516102e0526102e05160096101605160e05260c052604060c0206101405160e05260c052604060c020548082101561080c57600080fd5b808203905090506103a05260006103a0511815610953576002546301e1338081818301101561083a57600080fd5b80820190509050421015156108ab576101406103c0525b6103c0515160206103c051016103c0526103c06103c051101561087357610851565b600658016100a9565b6103a06103c0525b6103c0515260206103c051036103c0526101406103c0511015156108a757610884565b6000505b6020610480604463a9059cbb6103e05261016051610400526103a051610420526103fc60006005545af16108de57600080fd5b601f3d116108eb57600080fd5b600050610480506102e05160096101605160e05260c052604060c0206101405160e05260c052604060c02055610140516104a0526102e0516104c052610160517fad4a9acf26d8bba7a8cf1a41160d59be042ee554578e256c98d2ab74cdd4354260406104a0a25b61018051565b6363453ae160005114156109c35762ffffff541561097657600080fd5b600162ffffff55341561098857600080fd5b600435602051811061099957600080fd5b506004356101405233610160526101605161014051600658016106f2565b600050600062ffffff55005b6373b5fa416000511415610ab55762ffffff54156109e057600080fd5b600162ffffff5534156109f257600080fd5b6000610120525b61012051600401356020518110610a0f57600080fd5b506020610120510161012052610100610120511015610a2d576109f9565b61014060006008818352015b60046101405160088110610a4c57600080fd5b60200201351515610a5c57610aaa565b6101405160046101405160088110610a7357600080fd5b602002013561018052336101a0526101a05161018051600658016106f2565b610140526000505b8151600101808352811415610a39575b5050600062ffffff55005b63db2f5f796000511415610c7a573415610ace57600080fd5b6004356020518110610adf57600080fd5b506007543314610aee57600080fd5b60206101e060246370a0823161016052306101805261017c6004355afa610b1457600080fd5b601f3d11610b2157600080fd5b6000506101e0516101405260006004610260527fa9059cbb00000000000000000000000000000000000000000000000000000000610280526102606004806020846102c001018260208501600060045af15050805182019150506008546020826102c0010152602081019050610140516020826102c0010152602081019050806102c0526102c090508051602001806103608284600060045af1610bc457600080fd5b505060206104206103605161038060006004355af1610be257600080fd5b60203d80821115610bf35780610bf5565b815b90509050610400526104008051602001806102008284600060045af1610c1a57600080fd5b50506000610200511815610c6d57610200806020015160008251806020901315610c4357600080fd5b8091901215610c5157600080fd5b806020036101000a82049050905090501515610c6c57600080fd5b5b600160005260206000f350005b632405e3c66000511415610ca1573415610c9357600080fd5b60005460005260206000f350005b63f9a40bf66000511415610cc8573415610cba57600080fd5b60015460005260206000f350005b637375be266000511415610cef573415610ce157600080fd5b60025460005260206000f350005b632c4e722e6000511415610d16573415610d0857600080fd5b60035460005260206000f350005b63777854796000511415610d3d573415610d2f57600080fd5b60055460005260206000f350005b63f77c47916000511415610d64573415610d5657600080fd5b60065460005260206000f350005b63f851a4406000511415610d8b573415610d7d57600080fd5b60075460005260206000f350005b632c3f531e6000511415610db2573415610da457600080fd5b60085460005260206000f350005b638d09ef336000511415610e19573415610dcb57600080fd5b6004356020518110610ddc57600080fd5b506024356020518110610dee57600080fd5b50600960043560e05260c052604060c02060243560e05260c052604060c0205460005260206000f350005b5b60006000fd5b610198610fb803610198600039610198610fb8036000f3";

export class LixDistributor__factory extends ContractFactory {
  constructor(signer?: Signer) {
    super(_abi, _bytecode, signer);
  }

  deploy(
    _lix: string,
    _controller: string,
    _admin: string,
    _emergency_return: string,
    overrides?: Overrides & { from?: string | Promise<string> }
  ): Promise<LixDistributor> {
    return super.deploy(
      _lix,
      _controller,
      _admin,
      _emergency_return,
      overrides || {}
    ) as Promise<LixDistributor>;
  }
  getDeployTransaction(
    _lix: string,
    _controller: string,
    _admin: string,
    _emergency_return: string,
    overrides?: Overrides & { from?: string | Promise<string> }
  ): TransactionRequest {
    return super.getDeployTransaction(
      _lix,
      _controller,
      _admin,
      _emergency_return,
      overrides || {}
    );
  }
  attach(address: string): LixDistributor {
    return super.attach(address) as LixDistributor;
  }
  connect(signer: Signer): LixDistributor__factory {
    return super.connect(signer) as LixDistributor__factory;
  }
  static readonly bytecode = _bytecode;
  static readonly abi = _abi;
  static createInterface(): LixDistributorInterface {
    return new utils.Interface(_abi) as LixDistributorInterface;
  }
  static connect(
    address: string,
    signerOrProvider: Signer | Provider
  ): LixDistributor {
    return new Contract(address, _abi, signerOrProvider) as LixDistributor;
  }
}
