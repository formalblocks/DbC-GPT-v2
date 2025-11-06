```solidity
// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.5.0;
pragma experimental ABIEncoderV2;

/**
 * @title ERC7683 Reference Specification with Formal Postconditions
 * @notice This file contains reference contract definitions with formal specifications
 *         suitable for verification with solc-verify
 */

library ERC7683Types {
    struct GaslessCrossChainOrder {
        address originSettler;
        address user;
        uint256 nonce;
        uint256 originChainId;
        uint32 openDeadline;
        uint32 fillDeadline;
        bytes32 orderDataType;
        bytes orderData;
    }

    struct OnchainCrossChainOrder {
        uint32 fillDeadline;
        bytes32 orderDataType;
        bytes orderData;
    }

    struct ResolvedCrossChainOrder {
        address user;
        uint256 originChainId;
        uint32 openDeadline;
        uint32 fillDeadline;
        bytes32 orderId;
        Output[] maxSpent;
        Output[] minReceived;
        FillInstruction[] fillInstructions;
    }

    struct Output {
        bytes32 token;
        uint256 amount;
        bytes32 recipient;
        uint256 chainId;
    }

    struct FillInstruction {
        uint64 destinationChainId;
        bytes32 destinationSettler;
        bytes originData;
    }
}

contract IOriginSettler {
    mapping(address => mapping(uint256 => bool)) public usedNonces;
    mapping(bytes32 => bool) public openedOrders;

    uint256 public constant SUPPORTED_CHAIN_ID = 1;
    bytes32 public constant ORDER_DATA_TYPE_HASH = bytes32(uint256(1));

    event Open(bytes32 indexed orderId, ERC7683Types.ResolvedCrossChainOrder resolvedOrder);

    /**
     * @notice Opens a gasless cross-chain order on behalf of a user
     * @dev To be called by the filler
     * @dev This method must emit the Open event
     * @param order The GaslessCrossChainOrder definition
     * @param signature The user's signature over the order
     * @param originFillerData Any filler-defined data required by the settler
     */
    /// @notice precondition order.originSettler == address(this)
    /// @notice precondition order.originChainId == SUPPORTED_CHAIN_ID
    /// @notice precondition order.orderDataType == ORDER_DATA_TYPE_HASH
    /// @notice precondition !usedNonces[order.user][order.nonce]
    /// @notice precondition !openedOrders[bytes32(order.nonce)]
    /// @notice postcondition usedNonces[order.user][order.nonce]
    /// @notice postcondition openedOrders[bytes32(order.nonce)]
    function openFor(
        ERC7683Types.GaslessCrossChainOrder calldata order,
        bytes calldata signature,
        bytes calldata originFillerData
    ) external;

    /**
     * @notice Opens a cross-chain order initiated by the caller
     * @dev To be called by the user
     * @dev This method must emit the Open event
     * @param order The OnchainCrossChainOrder definition
     */
    /// @notice precondition order.orderDataType == ORDER_DATA_TYPE_HASH
    /// @notice precondition !openedOrders[bytes32(uint256(order.fillDeadline))]
    /// @notice postcondition openedOrders[bytes32(uint256(order.fillDeadline))]
    function open(ERC7683Types.OnchainCrossChainOrder calldata order) external;

    /**
     * @notice Resolves a gasless order into its canonical representation
     * @dev Intended to improve standardized integration of various order types and settlement contracts
     * @param order The GaslessCrossChainOrder definition
     * @param originFillerData Any filler-defined data required by the settler
     * @return ResolvedCrossChainOrder hydrated order data including the inputs and outputs of the order
     */
    /// @notice postcondition resolvedOrder.user == order.user
    /// @notice postcondition resolvedOrder.originChainId == order.originChainId
    /// @notice postcondition resolvedOrder.openDeadline == order.openDeadline
    /// @notice postcondition resolvedOrder.fillDeadline == order.fillDeadline
    /// @notice postcondition resolvedOrder.orderId == bytes32(order.nonce)
    function resolveFor(
        ERC7683Types.GaslessCrossChainOrder calldata order,
        bytes calldata originFillerData
    ) external view returns (ERC7683Types.ResolvedCrossChainOrder memory resolvedOrder);

    /**
     * @notice Resolves an on-chain order into its canonical representation
     * @dev Intended to improve standardized integration of various order types and settlement contracts
     * @param order The OnchainCrossChainOrder definition
     * @return ResolvedCrossChainOrder hydrated order data including the inputs and outputs of the order
     */
    /// @notice postcondition resolvedOrder.user == msg.sender
    /// @notice postcondition resolvedOrder.fillDeadline == order.fillDeadline
    /// @notice postcondition resolvedOrder.originChainId == SUPPORTED_CHAIN_ID
    /// @notice postcondition resolvedOrder.orderId == bytes32(uint256(order.fillDeadline))
    function resolve(
        ERC7683Types.OnchainCrossChainOrder calldata order
    ) external view returns (ERC7683Types.ResolvedCrossChainOrder memory resolvedOrder);
}

contract IDestinationSettler {
    mapping(bytes32 => bool) public filledOrders;

    /**
     * @notice Fills a single leg of a particular order on the destination chain
     * @param orderId Unique order identifier for this order
     * @param originData Data emitted on the origin to parameterize the fill
     * @param fillerData Data provided by the filler to inform the fill or express their preferences
     */
    /// @notice precondition !filledOrders[orderId]
    /// @notice postcondition filledOrders[orderId]
    function fill(
        bytes32 orderId,
        bytes calldata originData,
        bytes calldata fillerData
    ) external;
}
```
