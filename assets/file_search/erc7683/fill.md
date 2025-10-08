// State variable to track filled orders
mapping(bytes32 => bool) public filledOrders;

/**
 * @notice Fills a single leg of a particular order on the destination chain
 * @dev MUST validate orderId hasn't been filled previously
 * @dev MUST execute token transfers according to originData specification
 * @param orderId Unique order identifier for this order
 * @param originData Data emitted on the origin to parameterize the fill
 * @param fillerData Data provided by the filler to inform the fill or express their preferences
 */

$ADD POSTCONDITION HERE
function fill(
    bytes32 orderId,
    bytes calldata originData,
    bytes calldata fillerData
) external;
