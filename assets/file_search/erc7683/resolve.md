// State variables that postconditions MUST reference
mapping(address => mapping(uint256 => bool)) public usedNonces;
mapping(bytes32 => bool) public openedOrders;

// Constants for validation
uint256 public constant SUPPORTED_CHAIN_ID = 1;
bytes32 public constant ORDER_DATA_TYPE_HASH = bytes32(uint256(1));

/**
 * @notice Resolves a specific OnchainCrossChainOrder into a generic ResolvedCrossChainOrder
 * @dev Intended to improve standardized integration of various order types and settlement contracts
 * @dev MUST be a view function
 * @dev User MUST be msg.sender
 * @dev originChainId MUST be current chain
 * @dev MUST preserve fillDeadline from input order
 * @param order The OnchainCrossChainOrder definition
 * @return ResolvedCrossChainOrder hydrated order data including the inputs and outputs of the order
 */

$ADD POSTCONDITION HERE
function resolve(
    ERC7683Types.OnchainCrossChainOrder calldata order
) external view returns (ERC7683Types.ResolvedCrossChainOrder memory resolvedOrder);
