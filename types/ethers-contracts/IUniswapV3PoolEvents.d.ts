/* Autogenerated file. Do not edit manually. */
/* tslint:disable */
/* eslint-disable */

import {
  ethers,
  EventFilter,
  Signer,
  BigNumber,
  BigNumberish,
  PopulatedTransaction,
  BaseContract,
  ContractTransaction,
} from "ethers";
import { BytesLike } from "@ethersproject/bytes";
import { Listener, Provider } from "@ethersproject/providers";
import { FunctionFragment, EventFragment, Result } from "@ethersproject/abi";
import { TypedEventFilter, TypedEvent, TypedListener } from "./commons";

interface IUniswapV3PoolEventsInterface extends ethers.utils.Interface {
  functions: {};

  events: {
    "Burn(address,int24,int24,uint128,uint256,uint256)": EventFragment;
    "Collect(address,address,int24,int24,uint128,uint128)": EventFragment;
    "CollectProtocol(address,address,uint128,uint128)": EventFragment;
    "Flash(address,address,uint256,uint256,uint256,uint256)": EventFragment;
    "IncreaseObservationCardinalityNext(uint16,uint16)": EventFragment;
    "Initialize(uint160,int24)": EventFragment;
    "Mint(address,address,int24,int24,uint128,uint256,uint256)": EventFragment;
    "SetFeeProtocol(uint8,uint8,uint8,uint8)": EventFragment;
    "Swap(address,address,int256,int256,uint160,int24)": EventFragment;
  };

  getEvent(nameOrSignatureOrTopic: "Burn"): EventFragment;
  getEvent(nameOrSignatureOrTopic: "Collect"): EventFragment;
  getEvent(nameOrSignatureOrTopic: "CollectProtocol"): EventFragment;
  getEvent(nameOrSignatureOrTopic: "Flash"): EventFragment;
  getEvent(
    nameOrSignatureOrTopic: "IncreaseObservationCardinalityNext"
  ): EventFragment;
  getEvent(nameOrSignatureOrTopic: "Initialize"): EventFragment;
  getEvent(nameOrSignatureOrTopic: "Mint"): EventFragment;
  getEvent(nameOrSignatureOrTopic: "SetFeeProtocol"): EventFragment;
  getEvent(nameOrSignatureOrTopic: "Swap"): EventFragment;
}

export class IUniswapV3PoolEvents extends BaseContract {
  connect(signerOrProvider: Signer | Provider | string): this;
  attach(addressOrName: string): this;
  deployed(): Promise<this>;

  listeners<EventArgsArray extends Array<any>, EventArgsObject>(
    eventFilter?: TypedEventFilter<EventArgsArray, EventArgsObject>
  ): Array<TypedListener<EventArgsArray, EventArgsObject>>;
  off<EventArgsArray extends Array<any>, EventArgsObject>(
    eventFilter: TypedEventFilter<EventArgsArray, EventArgsObject>,
    listener: TypedListener<EventArgsArray, EventArgsObject>
  ): this;
  on<EventArgsArray extends Array<any>, EventArgsObject>(
    eventFilter: TypedEventFilter<EventArgsArray, EventArgsObject>,
    listener: TypedListener<EventArgsArray, EventArgsObject>
  ): this;
  once<EventArgsArray extends Array<any>, EventArgsObject>(
    eventFilter: TypedEventFilter<EventArgsArray, EventArgsObject>,
    listener: TypedListener<EventArgsArray, EventArgsObject>
  ): this;
  removeListener<EventArgsArray extends Array<any>, EventArgsObject>(
    eventFilter: TypedEventFilter<EventArgsArray, EventArgsObject>,
    listener: TypedListener<EventArgsArray, EventArgsObject>
  ): this;
  removeAllListeners<EventArgsArray extends Array<any>, EventArgsObject>(
    eventFilter: TypedEventFilter<EventArgsArray, EventArgsObject>
  ): this;

  listeners(eventName?: string): Array<Listener>;
  off(eventName: string, listener: Listener): this;
  on(eventName: string, listener: Listener): this;
  once(eventName: string, listener: Listener): this;
  removeListener(eventName: string, listener: Listener): this;
  removeAllListeners(eventName?: string): this;

  queryFilter<EventArgsArray extends Array<any>, EventArgsObject>(
    event: TypedEventFilter<EventArgsArray, EventArgsObject>,
    fromBlockOrBlockhash?: string | number | undefined,
    toBlock?: string | number | undefined
  ): Promise<Array<TypedEvent<EventArgsArray & EventArgsObject>>>;

  interface: IUniswapV3PoolEventsInterface;

  functions: {};

  callStatic: {};

  filters: {
    Burn(
      owner?: string | null,
      tickLower?: BigNumberish | null,
      tickUpper?: BigNumberish | null,
      amount?: null,
      amount0?: null,
      amount1?: null
    ): TypedEventFilter<
      [string, number, number, BigNumber, BigNumber, BigNumber],
      {
        owner: string;
        tickLower: number;
        tickUpper: number;
        amount: BigNumber;
        amount0: BigNumber;
        amount1: BigNumber;
      }
    >;

    Collect(
      owner?: string | null,
      recipient?: null,
      tickLower?: BigNumberish | null,
      tickUpper?: BigNumberish | null,
      amount0?: null,
      amount1?: null
    ): TypedEventFilter<
      [string, string, number, number, BigNumber, BigNumber],
      {
        owner: string;
        recipient: string;
        tickLower: number;
        tickUpper: number;
        amount0: BigNumber;
        amount1: BigNumber;
      }
    >;

    CollectProtocol(
      sender?: string | null,
      recipient?: string | null,
      amount0?: null,
      amount1?: null
    ): TypedEventFilter<
      [string, string, BigNumber, BigNumber],
      {
        sender: string;
        recipient: string;
        amount0: BigNumber;
        amount1: BigNumber;
      }
    >;

    Flash(
      sender?: string | null,
      recipient?: string | null,
      amount0?: null,
      amount1?: null,
      paid0?: null,
      paid1?: null
    ): TypedEventFilter<
      [string, string, BigNumber, BigNumber, BigNumber, BigNumber],
      {
        sender: string;
        recipient: string;
        amount0: BigNumber;
        amount1: BigNumber;
        paid0: BigNumber;
        paid1: BigNumber;
      }
    >;

    IncreaseObservationCardinalityNext(
      observationCardinalityNextOld?: null,
      observationCardinalityNextNew?: null
    ): TypedEventFilter<
      [number, number],
      {
        observationCardinalityNextOld: number;
        observationCardinalityNextNew: number;
      }
    >;

    Initialize(
      sqrtPriceX96?: null,
      tick?: null
    ): TypedEventFilter<
      [BigNumber, number],
      { sqrtPriceX96: BigNumber; tick: number }
    >;

    Mint(
      sender?: null,
      owner?: string | null,
      tickLower?: BigNumberish | null,
      tickUpper?: BigNumberish | null,
      amount?: null,
      amount0?: null,
      amount1?: null
    ): TypedEventFilter<
      [string, string, number, number, BigNumber, BigNumber, BigNumber],
      {
        sender: string;
        owner: string;
        tickLower: number;
        tickUpper: number;
        amount: BigNumber;
        amount0: BigNumber;
        amount1: BigNumber;
      }
    >;

    SetFeeProtocol(
      feeProtocol0Old?: null,
      feeProtocol1Old?: null,
      feeProtocol0New?: null,
      feeProtocol1New?: null
    ): TypedEventFilter<
      [number, number, number, number],
      {
        feeProtocol0Old: number;
        feeProtocol1Old: number;
        feeProtocol0New: number;
        feeProtocol1New: number;
      }
    >;

    Swap(
      sender?: string | null,
      recipient?: string | null,
      amount0?: null,
      amount1?: null,
      sqrtPriceX96?: null,
      tick?: null
    ): TypedEventFilter<
      [string, string, BigNumber, BigNumber, BigNumber, number],
      {
        sender: string;
        recipient: string;
        amount0: BigNumber;
        amount1: BigNumber;
        sqrtPriceX96: BigNumber;
        tick: number;
      }
    >;
  };

  estimateGas: {};

  populateTransaction: {};
}
