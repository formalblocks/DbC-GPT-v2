// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.5.0;
pragma experimental ABIEncoderV2;

/**
 * @title ERC7683 Formal Specification
 * @notice Reference postconditions for ERC-7683 Cross-Chain Intents Standard
 * @dev These specifications are used as reference for LLM-based postcondition generation
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

interface IOriginSettler {
    event Open(bytes32 indexed orderId, ERC7683Types.ResolvedCrossChainOrder resolvedOrder);

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

    /// @notice precondition order.orderDataType == ORDER_DATA_TYPE_HASH
    /// @notice precondition !openedOrders[bytes32(uint256(order.fillDeadline))]
    /// @notice postcondition openedOrders[bytes32(uint256(order.fillDeadline))]
    function open(ERC7683Types.OnchainCrossChainOrder calldata order) external;

    /// @notice precondition order.originSettler == address(this)
    /// @notice precondition order.originChainId == SUPPORTED_CHAIN_ID
    /// @notice precondition order.orderDataType == ORDER_DATA_TYPE_HASH
    /// @notice postcondition resolvedOrder.user == order.user
    /// @notice postcondition resolvedOrder.originChainId == order.originChainId
    /// @notice postcondition resolvedOrder.openDeadline == order.openDeadline
    /// @notice postcondition resolvedOrder.fillDeadline == order.fillDeadline
    /// @notice postcondition resolvedOrder.orderId == bytes32(order.nonce)
    function resolveFor(
        ERC7683Types.GaslessCrossChainOrder calldata order,
        bytes calldata originFillerData
    ) external view returns (ERC7683Types.ResolvedCrossChainOrder memory resolvedOrder);

    /// @notice precondition order.orderDataType == ORDER_DATA_TYPE_HASH
    /// @notice postcondition resolvedOrder.user == msg.sender
    /// @notice postcondition resolvedOrder.originChainId == SUPPORTED_CHAIN_ID
    /// @notice postcondition resolvedOrder.openDeadline == uint32(-1)
    /// @notice postcondition resolvedOrder.fillDeadline == order.fillDeadline
    /// @notice postcondition resolvedOrder.orderId == bytes32(uint256(order.fillDeadline))
    function resolve(
        ERC7683Types.OnchainCrossChainOrder calldata order
    ) external view returns (ERC7683Types.ResolvedCrossChainOrder memory resolvedOrder);
}

interface IDestinationSettler {
    /// @notice precondition !filledOrders[orderId]
    /// @notice postcondition filledOrders[orderId]
    function fill(
        bytes32 orderId,
        bytes calldata originData,
        bytes calldata fillerData
    ) external;
}
