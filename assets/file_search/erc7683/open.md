// State variables that postconditions MUST reference
mapping(address => mapping(uint256 => bool)) public usedNonces;
mapping(bytes32 => bool) public openedOrders;

// Constants for validation
uint256 public constant SUPPORTED_CHAIN_ID = 1;
bytes32 public constant ORDER_DATA_TYPE_HASH = bytes32(uint256(1));

/**
 * @notice Opens a cross-chain order
 * @dev To be called by the user
 * @dev This method MUST emit the Open event
 * @dev MUST validate orderDataType
 * @dev MUST enforce orderId uniqueness
 * @param order The OnchainCrossChainOrder definition
 */

$ADD POSTCONDITION HERE
function open(ERC7683Types.OnchainCrossChainOrder calldata order) external;
