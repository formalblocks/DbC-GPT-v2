// SPDX-License-Identifier: GPL-3.0-or-later
pragma solidity ^0.5.0;
pragma experimental ABIEncoderV2;

import "./contracts/erc7683/ERC7683.sol";

/**
 * @title ERC7683OriginSettler (verification harness)
 * @notice Minimal origin settler used to exercise solc-verify specifications.
 *         The implementation focuses on nonce tracking and order opening logic
 *         and intentionally avoids advanced language features (abi.* helpers,
 *         inline assembly, dynamic decoding) that are unsupported by solc-verify.
 */
contract ERC7683OriginSettler is IOriginSettler {
    // Simplified constants – the harness only models a single chain and
    // a single accepted order type hash.
    uint256 public constant SUPPORTED_CHAIN_ID = 1;
    bytes32 public constant ORDER_DATA_TYPE_HASH = bytes32(uint256(1));

    // Nonce bookkeeping per user for gasless orders.
    mapping(address => mapping(uint256 => bool)) public usedNonces;

    // Tracked order ids to ensure an order is opened at most once.
    mapping(bytes32 => bool) public openedOrders;

    /**
     * @notice Opens a gasless cross-chain order on behalf of a user.
     *         The implementation models nonce replay protection and ensures
     *         that a derived order identifier is marked as opened.
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
    ) external {
        require(
            order.originSettler == address(this),
            "Wrong settlement contract"
        );
        require(order.originChainId == SUPPORTED_CHAIN_ID, "Wrong chain ID");
        require(
            order.orderDataType == ORDER_DATA_TYPE_HASH,
            "Wrong order data type"
        );
        require(!usedNonces[order.user][order.nonce], "Nonce already used");

        usedNonces[order.user][order.nonce] = true;

        bytes32 orderId = bytes32(order.nonce);
        require(!openedOrders[orderId], "Order already opened");
        openedOrders[orderId] = true;

        ERC7683Types.ResolvedCrossChainOrder
            memory resolvedOrder = _buildResolvedOrder(
                order.user,
                order.originChainId,
                order.openDeadline,
                order.fillDeadline,
                orderId
            );

        emit Open(orderId, resolvedOrder);
    }

    /**
     * @notice Opens an on-chain order initiated by the caller.
     */
    /// @notice precondition order.orderDataType == ORDER_DATA_TYPE_HASH
    /// @notice precondition !openedOrders[bytes32(uint256(order.fillDeadline))]
    /// @notice postcondition openedOrders[bytes32(uint256(order.fillDeadline))]
    function open(ERC7683Types.OnchainCrossChainOrder calldata order) external {
        require(
            order.orderDataType == ORDER_DATA_TYPE_HASH,
            "Wrong order data type"
        );

        bytes32 orderId = bytes32(uint256(order.fillDeadline));
        require(!openedOrders[orderId], "Order already opened");
        openedOrders[orderId] = true;

        ERC7683Types.ResolvedCrossChainOrder
            memory resolvedOrder = _buildResolvedOrder(
                msg.sender,
                SUPPORTED_CHAIN_ID,
                uint32(-1),
                order.fillDeadline,
                orderId
            );

        emit Open(orderId, resolvedOrder);
    }

    /**
     * @notice Resolves a gasless order into its canonical representation.
     */
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
    )
        external
        view
        returns (ERC7683Types.ResolvedCrossChainOrder memory resolvedOrder)
    {
        require(
            order.originSettler == address(this),
            "Wrong settlement contract"
        );
        require(order.originChainId == SUPPORTED_CHAIN_ID, "Wrong chain ID");
        require(
            order.orderDataType == ORDER_DATA_TYPE_HASH,
            "Wrong order data type"
        );

        resolvedOrder = _buildResolvedOrder(
            order.user,
            order.originChainId,
            order.openDeadline,
            order.fillDeadline,
            bytes32(order.nonce)
        );
    }

    /**
     * @notice Resolves an on-chain order initiated by the caller.
     */
    /// @notice precondition order.orderDataType == ORDER_DATA_TYPE_HASH
    /// @notice postcondition resolvedOrder.user == msg.sender
    /// @notice postcondition resolvedOrder.originChainId == SUPPORTED_CHAIN_ID
    /// @notice postcondition resolvedOrder.openDeadline == uint32(-1)
    /// @notice postcondition resolvedOrder.fillDeadline == order.fillDeadline
    /// @notice postcondition resolvedOrder.orderId == bytes32(uint256(order.fillDeadline))
    function resolve(
        ERC7683Types.OnchainCrossChainOrder calldata order
    )
        external
        view
        returns (ERC7683Types.ResolvedCrossChainOrder memory resolvedOrder)
    {
        require(
            order.orderDataType == ORDER_DATA_TYPE_HASH,
            "Wrong order data type"
        );

        resolvedOrder = _buildResolvedOrder(
            msg.sender,
            SUPPORTED_CHAIN_ID,
            uint32(-1),
            order.fillDeadline,
            bytes32(uint256(order.fillDeadline))
        );
    }

    /**
     * @notice Helper constructing a resolved order value without relying on
     *         dynamic decoding or complex arithmetic.
     */
    function _buildResolvedOrder(
        address user,
        uint256 originChainId,
        uint32 openDeadline,
        uint32 fillDeadline,
        bytes32 orderId
    )
        internal
        pure
        returns (ERC7683Types.ResolvedCrossChainOrder memory resolvedOrder)
    {
        resolvedOrder.user = user;
        resolvedOrder.originChainId = originChainId;
        resolvedOrder.openDeadline = openDeadline;
        resolvedOrder.fillDeadline = fillDeadline;
        resolvedOrder.orderId = orderId;

        resolvedOrder.maxSpent = new ERC7683Types.Output[](0);
        resolvedOrder.minReceived = new ERC7683Types.Output[](0);
        resolvedOrder.fillInstructions = new ERC7683Types.FillInstruction[](0);
    }
}
