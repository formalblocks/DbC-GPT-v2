// State variables that postconditions MUST reference
mapping(address => mapping(uint256 => bool)) public usedNonces;
mapping(bytes32 => bool) public openedOrders;

// Constants for validation
uint256 public constant SUPPORTED_CHAIN_ID = 1;
bytes32 public constant ORDER_DATA_TYPE_HASH = bytes32(uint256(1));

/**
 * @notice Opens a gasless cross-chain order on behalf of a user
 * @dev To be called by the filler
 * @dev This method MUST emit the Open event
 * @dev MUST validate originSettler, originChainId, orderDataType
 * @dev MUST enforce nonce uniqueness (replay protection)
 * @dev MUST enforce orderId uniqueness
 * @param order The GaslessCrossChainOrder definition
 * @param signature The user's signature over the order
 * @param originFillerData Any filler-defined data required by the settler
 */

$ADD POSTCONDITION HERE
function openFor(
    ERC7683Types.GaslessCrossChainOrder calldata order,
    bytes calldata signature,
    bytes calldata originFillerData
) external;
