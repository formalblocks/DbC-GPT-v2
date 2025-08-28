```solidity

pragma solidity >= 0.5.0;

contract ERCX {
    // Events
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event StateTransition(uint256 indexed tokenId, uint8 fromState, uint8 toState, uint256 timestamp);
    event ConditionalApproval(address indexed owner, address indexed approved, uint256 indexed tokenId, uint256 condition);
    event ThresholdReached(uint256 indexed tokenId, uint256 threshold, uint256 currentValue);
    event TimeBasedAction(uint256 indexed tokenId, uint256 actionType, uint256 timestamp);
    event Approval(address indexed owner, address indexed approved, uint256 indexed tokenId);
    event ApprovalForAll(address indexed owner, address indexed operator, bool approved);

    // Token states
    uint8 constant INACTIVE = 0;
    uint8 constant ACTIVE = 1;
    uint8 constant LOCKED = 2;
    uint8 constant BURNED = 3;

    // Storage mappings
    mapping(uint256 => address) private _owners;
    mapping(address => uint256) private _balances;
    mapping(uint256 => address) private _tokenApprovals;
    mapping(address => mapping(address => bool)) private _operatorApprovals;
    mapping(uint256 => uint8) private _tokenStates;
    mapping(uint256 => uint256) private _thresholds;
    mapping(uint256 => uint256) private _currentValues;
    mapping(uint256 => mapping(address => uint256)) private _conditionalApprovals;
    mapping(uint256 => uint256) private _timeBasedActionTypes;
    mapping(uint256 => uint256) private _timeBasedExecuteAt;

    /**
     * @dev Returns the number of tokens in `owner`'s account.
     * Requirements:
     * - `owner` cannot be the zero address.
     */
    /// @notice postcondition owner != address(0)
    /// @notice postcondition _balances[owner] == balance
    function balanceOf(address owner) public view returns (uint256 balance);

    /**
     * @dev Returns the owner of the `tokenId` token.
     * Requirements:
     * - `tokenId` must exist.
     */
    /// @notice postcondition _owners[tokenId] != address(0)
    /// @notice postcondition _owners[tokenId] == owner
    function ownerOf(uint256 tokenId) public view returns (address owner);

    /**
     * @dev Gives permission to `to` to transfer `tokenId` token to another account.
     * The approval is cleared when the token is transferred.
     * Requirements:
     * - The caller must own the token or be an approved operator.
     * - `tokenId` must exist.
     */
    /// @notice postcondition _owners[tokenId] != address(0)
    /// @notice postcondition _owners[tokenId] == msg.sender || _operatorApprovals[_owners[tokenId]][msg.sender]
    /// @notice postcondition _tokenApprovals[tokenId] == to
    function approve(address to, uint256 tokenId) public;

    /**
     * @dev Returns the account approved for `tokenId` token.
     * Requirements:
     * - `tokenId` must exist.
     */
    /// @notice postcondition _owners[tokenId] != address(0)
    /// @notice postcondition _tokenApprovals[tokenId] == operator
    function getApproved(uint256 tokenId) public view returns (address operator);

    /**
     * @dev Approve or remove `operator` as an operator for the caller.
     * Operators can call {transferFrom} for any token owned by the caller.
     */
    /// @notice postcondition _operatorApprovals[msg.sender][operator] == approved
    function setApprovalForAll(address operator, bool approved) public;

    /**
     * @dev Returns if the `operator` is allowed to manage all of the assets of `owner`.
     */
    /// @notice postcondition _operatorApprovals[owner][operator] == \result
    function isApprovedForAll(address owner, address operator) public view returns (bool);

    /**
     * @dev Transfers `tokenId` token from `from` to `to`.
     * Requirements:
     * - `from` cannot be the zero address.
     * - `to` cannot be the zero address.
     * - `tokenId` token must be owned by `from`.
     * - If the caller is not `from`, it must be approved to move this token.
     * - Token must be in ACTIVE state for transfers.
     */
    /// @notice postcondition from != address(0)
    /// @notice postcondition to != address(0)
    /// @notice postcondition __verifier_old_address(_owners[tokenId]) == from
    /// @notice postcondition _tokenStates[tokenId] == ACTIVE
    /// @notice postcondition from == msg.sender || _tokenApprovals[tokenId] == msg.sender || _operatorApprovals[from][msg.sender]
    /// @notice postcondition _owners[tokenId] == to
    /// @notice postcondition _balances[from] == __verifier_old_uint(_balances[from]) - 1
    /// @notice postcondition _balances[to] == __verifier_old_uint(_balances[to]) + 1
    /// @notice postcondition _tokenApprovals[tokenId] == address(0)
    function transferFrom(address from, address to, uint256 tokenId) public;

    /**
     * @dev Returns the current state of the token.
     * Requirements:
     * - `tokenId` must exist.
     */
    /// @notice postcondition _owners[tokenId] != address(0)
    /// @notice postcondition _tokenStates[tokenId] == state
    /// @notice postcondition state <= BURNED
    function getTokenState(uint256 tokenId) public view returns (uint8 state);

    /**
     * @dev Transitions token to a new state.
     * Requirements:
     * - `tokenId` must exist.
     * - Caller must be owner or approved operator.
     * - State transition must be valid according to rules.
     */
    /// @notice postcondition _owners[tokenId] != address(0)
    /// @notice postcondition _owners[tokenId] == msg.sender || _operatorApprovals[_owners[tokenId]][msg.sender]
    /// @notice postcondition newState <= BURNED
    /// @notice postcondition __verifier_old_uint(_tokenStates[tokenId]) != BURNED
    /// @notice postcondition newState == BURNED || (__verifier_old_uint(_tokenStates[tokenId]) == INACTIVE && newState == ACTIVE) || (__verifier_old_uint(_tokenStates[tokenId]) == ACTIVE && (newState == LOCKED || newState == ACTIVE)) || (__verifier_old_uint(_tokenStates[tokenId]) == LOCKED && (newState == ACTIVE || newState == LOCKED))
    /// @notice postcondition _tokenStates[tokenId] == newState
    function transitionState(uint256 tokenId, uint8 newState) public;

    /**
     * @dev Checks if a state transition is valid.
     * Requirements:
     * - `tokenId` must exist.
     */
    /// @notice postcondition _owners[tokenId] != address(0)
    /// @notice postcondition newState <= BURNED
    /// @notice postcondition _tokenStates[tokenId] == BURNED ==> valid == false
    /// @notice postcondition _tokenStates[tokenId] != BURNED ==> (valid == (newState == BURNED || (_tokenStates[tokenId] == INACTIVE && newState == ACTIVE) || (_tokenStates[tokenId] == ACTIVE && (newState == LOCKED || newState == ACTIVE)) || (_tokenStates[tokenId] == LOCKED && (newState == ACTIVE || newState == LOCKED))))
    function canTransitionState(uint256 tokenId, uint8 newState) public view returns (bool valid);

    /**
     * @dev Sets a conditional approval that is only valid when condition is met.
     * Requirements:
     * - `tokenId` must exist.
     * - Caller must be owner or approved operator.
     */
    /// @notice postcondition _owners[tokenId] != address(0)
    /// @notice postcondition _owners[tokenId] == msg.sender || _operatorApprovals[_owners[tokenId]][msg.sender]
    /// @notice postcondition _conditionalApprovals[tokenId][to] == condition
    function setConditionalApproval(address to, uint256 tokenId, uint256 condition) public;

    /**
     * @dev Executes a conditional transfer if conditions are met.
     * Requirements:
     * - `tokenId` must exist.
     * - Conditional approval must exist and be valid.
     * - Conditions must be satisfied.
     */
    /// @notice postcondition _owners[tokenId] != address(0)
    /// @notice postcondition _conditionalApprovals[tokenId][to] > 0
    /// @notice postcondition _currentValues[tokenId] >= _conditionalApprovals[tokenId][to]
    /// @notice postcondition _tokenStates[tokenId] == ACTIVE
    /// @notice postcondition _owners[tokenId] == to
    /// @notice postcondition _conditionalApprovals[tokenId][to] == 0
    function executeConditionalTransfer(uint256 tokenId, address to) public;

    /**
     * @dev Updates the threshold value for a token.
     * Requirements:
     * - `tokenId` must exist.
     * - Caller must be owner.
     */
    /// @notice postcondition _owners[tokenId] != address(0)
    /// @notice postcondition _owners[tokenId] == msg.sender
    /// @notice postcondition _thresholds[tokenId] == newThreshold
    function updateThreshold(uint256 tokenId, uint256 newThreshold) public;

    /**
     * @dev Returns the current threshold for a token.
     * Requirements:
     * - `tokenId` must exist.
     */
    /// @notice postcondition _owners[tokenId] != address(0)
    /// @notice postcondition _thresholds[tokenId] == threshold
    function getThreshold(uint256 tokenId) public view returns (uint256 threshold);

    /**
     * @dev Sets a time-based action to be executed at a specific time.
     * Requirements:
     * - `tokenId` must exist.
     * - Caller must be owner.
     * - `executeAt` must be in the future.
     */
    /// @notice postcondition _owners[tokenId] != address(0)
    /// @notice postcondition _owners[tokenId] == msg.sender
    /// @notice postcondition executeAt > block.timestamp
    /// @notice postcondition _timeBasedActionTypes[tokenId] == actionType
    /// @notice postcondition _timeBasedExecuteAt[tokenId] == executeAt
    function setTimeBasedAction(uint256 tokenId, uint256 actionType, uint256 executeAt) public;

    /**
     * @dev Executes a time-based action if the time has come.
     * Requirements:
     * - `tokenId` must exist.
     * - Time-based action must be set.
     * - Current time must be >= executeAt time.
     */
    /// @notice postcondition _owners[tokenId] != address(0)
    /// @notice postcondition _timeBasedActionTypes[tokenId] > 0
    /// @notice postcondition block.timestamp >= _timeBasedExecuteAt[tokenId]
    /// @notice postcondition _timeBasedActionTypes[tokenId] == 1 ==> _tokenStates[tokenId] == ACTIVE
    /// @notice postcondition _timeBasedActionTypes[tokenId] == 2 ==> _tokenStates[tokenId] == LOCKED
    /// @notice postcondition _timeBasedActionTypes[tokenId] == 3 ==> _tokenStates[tokenId] == BURNED
    function executeTimeBasedAction(uint256 tokenId) public;

    /**
     * @dev Returns the time-based action details for a token.
     * Requirements:
     * - `tokenId` must exist.
     */
    /// @notice postcondition _owners[tokenId] != address(0)
    /// @notice postcondition _timeBasedActionTypes[tokenId] == actionType
    /// @notice postcondition _timeBasedExecuteAt[tokenId] == executeAt
    function getTimeBasedAction(uint256 tokenId) public view returns (uint256 actionType, uint256 executeAt);
}
```