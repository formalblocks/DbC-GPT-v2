// State variables that postconditions MUST reference
mapping(address => mapping(uint256 => bool)) public usedNonces;
mapping(bytes32 => bool) public openedOrders;

// Constants for validation
uint256 public constant SUPPORTED_CHAIN_ID = 1;
bytes32 public constant ORDER_DATA_TYPE_HASH = bytes32(uint256(1));

/**
 * @notice Resolves a specific GaslessCrossChainOrder into a generic ResolvedCrossChainOrder
 * @dev Intended to improve standardized integration of various order types and settlement contracts
 * @dev MUST be a view function
 * @dev MUST preserve user, originChainId, openDeadline, fillDeadline from input order
 * @dev MUST compute consistent orderId
 * @param order The GaslessCrossChainOrder definition
 * @param originFillerData Any filler-defined data required by the settler
 * @return ResolvedCrossChainOrder hydrated order data including the inputs and outputs of the order
 */

$ADD POSTCONDITION HERE
function resolveFor(
    ERC7683Types.GaslessCrossChainOrder calldata order,
    bytes calldata originFillerData
) external view returns (ERC7683Types.ResolvedCrossChainOrder memory resolvedOrder);
