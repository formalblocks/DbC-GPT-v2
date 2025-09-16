mapping (address => uint256) private _balances;

mapping (address => mapping (address => uint256)) private _allowed;

uint256 private _totalSupply;

#### transfer

**Function Purpose**: Transfers `_value` amount of tokens to address `_to`, and MUST fire the `Transfer` event.

**ERC-20 Specification**: 
- The function SHOULD `throw` if the message caller's account balance does not have enough tokens to spend.
- Transfers of 0 values MUST be treated as normal transfers and fire the `Transfer` event.
- Must return true on success, should revert on failure

**State Variable Usage**:
- Reads and modifies `_balances[msg.sender]` (decreases by `_value`)
- Reads and modifies `_balances[_to]` (increases by `_value`)
- Does not affect `_allowed` mapping or `_totalSupply`

**Expected Behavior**:
- When `msg.sender != _to`: Decrease sender balance, increase recipient balance
- When `msg.sender == _to`: No balance change (self-transfer)
- Must maintain total supply conservation
- Should only succeed if sender has sufficient balance

**Edge Cases**:
- Zero value transfers are valid and should succeed
- Self-transfers (`msg.sender == _to`) should not change balances
- Must handle the case where sender and recipient are the same

**Postcondition Requirements**:
- Use `__verifier_old_uint()` for old balance values
- Handle both success and failure cases with `success` boolean
- Account for self-transfer scenario
- Use exact parameter names: `_to`, `_value`, `success`

$ADD POSTCONDITION HERE
function transfer(address _to, uint256 _value) public returns (bool success);