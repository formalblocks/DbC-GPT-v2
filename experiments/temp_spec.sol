pragma solidity ^0.5.0;
pragma experimental ABIEncoderV2;

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

contract ERC7683 {

    // Events
    event Open(bytes32 indexed orderId, ERC7683Types.ResolvedCrossChainOrder resolvedOrder);

    // State Variables
    mapping(address => mapping(uint256 => bool)) public usedNonces;
    mapping(bytes32 => bool) public openedOrders;
    mapping(bytes32 => bool) public filledOrders;

    // Functions
    /// @notice postcondition true
    function openFor(ERC7683Types.GaslessCrossChainOrder calldata order,
        bytes calldata signature,
        bytes calldata originFillerData) external;

    /// @notice postcondition true
    function open(ERC7683Types.OnchainCrossChainOrder calldata order) external;

    /// @notice postcondition true
    function resolveFor(ERC7683Types.GaslessCrossChainOrder calldata order,
        bytes calldata originFillerData) external view returns (ERC7683Types.ResolvedCrossChainOrder memory resolvedOrder);

    /// @notice postcondition true
    function resolve(ERC7683Types.OnchainCrossChainOrder calldata order) external view returns (ERC7683Types.ResolvedCrossChainOrder memory resolvedOrder);

    /// @notice postcondition true
    function fill(bytes32 orderId,
        bytes calldata originData,
        bytes calldata fillerData) external;

}
