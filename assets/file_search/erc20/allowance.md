mapping (address => uint256) private _balances;

mapping (address => mapping (address => uint256)) private _allowed;

uint256 private _totalSupply;

#### allowance

**Function Purpose**: Returns the amount which `_spender` is still allowed to withdraw from `_owner`.

**ERC-20 Specification**: This function provides read-only access to the allowance mapping, showing how much the spender is authorized to transfer on behalf of the owner.

**State Variable Usage**:
- Reads from `_allowed[_owner][_spender]` mapping
- Does not modify any state variables (view function)

**Expected Behavior**:
- Returns the exact value stored in `_allowed[_owner][_spender]`
- Should return 0 if no allowance has been set
- Should never revert under normal circumstances

**Related Functions**:
- Used in conjunction with `approve()` (which sets allowances)
- Used by `transferFrom()` (which consumes allowances)

**Postcondition Requirements**:
- The return value must equal the stored allowance value
- Must use the exact parameter names: `_owner`, `_spender`, `remaining`
- Access the `_allowed` mapping correctly

$ADD POSTCONDITION HERE
function allowance(address _owner, address _spender) public view returns (uint256 remaining);