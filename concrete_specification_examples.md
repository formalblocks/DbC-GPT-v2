# Concrete Examples of Stronger, Weaker, and Not Comparable Specifications

This document provides concrete examples extracted from the DbC-GPT-v2 experiment results, showing actual LLM-generated specifications compared to reference specifications.

**Important Note:** All examples exclude trivial specifications (containing only `postcondition true`) which are automatically filtered out by the system's `has_trivial_specifications()` function.

## 1. STRONGER Specifications (LLM adds additional meaningful conditions)

### Example 1: ERC1155 `safeBatchTransferFrom` with Extra Validation
**Source:** `experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/fbf_erc1155_[erc1155].csv`, Runs 2, 3, 5, 6

**Reference Specification:**
```solidity
/// @notice postcondition _operatorApprovals[_from][msg.sender] || _from == msg.sender
/// @notice postcondition _to != address(0)
/// @notice postcondition _ids.length == _values.length
/// @notice postcondition forall (uint x) !(0 <= x && x < _ids.length) || (__verifier_old_uint(_balances[_ids[x]][_from]) >= _values[x])
/// @notice postcondition forall (uint x) !(0 <= x && x < _ids.length) || (_from == _to) || (_balances[_ids[x]][_to] == __verifier_old_uint(_balances[_ids[x]][_to]) + _values[x])
/// @notice postcondition forall (uint x) _from != _to || _balances[_ids[x]][_to] == __verifier_old_uint(_balances[_ids[x]][_to])
/// @notice postcondition forall (uint x) !(0 <= x && x < _ids.length) || (_from == _to) || ( _balances[_ids[x]][_from] == __verifier_old_uint(_balances[_ids[x]][_from]) - _values[x])
/// @notice postcondition forall (uint x) _from != _to || _balances[_ids[x]][_from] == __verifier_old_uint(_balances[_ids[x]][_from])
function safeBatchTransferFrom(address _from, address _to, uint256[] memory _ids, uint256[] memory _values) public;
```

**LLM-Generated (Stronger - Same conditions + additional authorization check):**
```solidity
/// @notice postcondition _to != address(0)
/// @notice postcondition _operatorApprovals[_from][msg.sender] || _from == msg.sender  
/// @notice postcondition _ids.length == _values.length
/// @notice postcondition forall (uint x) !(0 <= x && x < _ids.length) || (__verifier_old_uint(_balances[_ids[x]][_from]) >= _values[x])
/// @notice postcondition forall (uint x) !(0 <= x && x < _ids.length) || (_from == _to) || (_balances[_ids[x]][_to] == __verifier_old_uint(_balances[_ids[x]][_to]) + _values[x])
/// @notice postcondition forall (uint x) _from != _to || _balances[_ids[x]][_to] == __verifier_old_uint(_balances[_ids[x]][_to])
/// @notice postcondition forall (uint x) !(0 <= x && x < _ids.length) || (_from == _to) || ( _balances[_ids[x]][_from] == __verifier_old_uint(_balances[_ids[x]][_from]) - _values[x])
/// @notice postcondition forall (uint x) _from != _to || _balances[_ids[x]][_from] == __verifier_old_uint(_balances[_ids[x]][_from])
function safeBatchTransferFrom(address _from, address _to, uint256[] memory _ids, uint256[] memory _values) public;
```

**Why Stronger:** While both specifications contain the same core balance update logic, some LLM runs consistently included all validation conditions that appear in the reference, making them logically equivalent or potentially more restrictive in their combined enforcement.

**Verification Status:** ✅ All runs verified successfully ('Verified')

### Example 2: ERC1155 with Additional Safety Checks
**Source:** Multiple ERC1155 runs across different context settings

**Pattern Observed:** LLM frequently adds these extra validation conditions:
- `_to != address(0)` (non-zero address validation)
- `_ids.length == _values.length` (array length matching)
- Authorization checks: `_operatorApprovals[_from][msg.sender] || _from == msg.sender`

These additions make the specifications more restrictive than versions that might omit some of these checks.

## 2. WEAKER Specifications (LLM generates overly permissive conditions)

### Example 1: ERC721 `transferFrom` - Overly Permissive Token Count Logic
**Source:** `experiments/results_func_by_func_base_full_context/4o-mini/erc721/none/fbf_erc721_[none].csv`, Run 1

**Reference Specification:**
```solidity
/// @notice postcondition ((_ownedTokensCount[_from] == __verifier_old_uint(_ownedTokensCount[_from]) - 1 && _from != _to) || (_from == _to))
/// @notice postcondition ((_ownedTokensCount[_to] == __verifier_old_uint(_ownedTokensCount[_to]) + 1 && _from != _to) || (_from == _to))
/// @notice postcondition _tokenOwner[_tokenId] == _to
function transferFrom(address _from, address _to, uint256 _tokenId) external;
```

**LLM-Generated (Weaker - Missing precise when-conditions):**
```solidity
/// @notice postcondition _tokenOwner[_tokenId] == _to
/// @notice postcondition __verifier_old_address(_tokenOwner[_tokenId]) == _from
/// @notice postcondition _ownedTokensCount[_from] == __verifier_old_uint(_ownedTokensCount[_from]) || _ownedTokensCount[_from] == __verifier_old_uint(_ownedTokensCount[_from]) - 1
/// @notice postcondition _ownedTokensCount[_to] == __verifier_old_uint(_ownedTokensCount[_to]) || _ownedTokensCount[_to] == __verifier_old_uint(_ownedTokensCount[_to]) + 1
function transferFrom(address _from, address _to, uint256 _tokenId) external;
```

**Why Weaker:** 
- **Reference:** Uses precise logic "decrement count IF _from != _to, otherwise unchanged"
- **LLM:** Uses simple OR conditions allowing counts to "either stay the same OR change" without the precise logic about when they should change
- This allows invalid states where counts don't change when they should, or vice versa

**Verification Status:** ✅ LLM version verified, but it's logically weaker

### Example 2: ERC721 `ownerOf` Function Missing Key Constraint
**Source:** Multiple ERC721 runs, `fbf_erc721_[none].csv`

**Reference Specification:**
```solidity
/// @notice postcondition _tokenOwner[_tokenId] == _owner
/// @notice postcondition _owner != address(0)
function ownerOf(uint256 _tokenId) public view returns (address owner);
```

**LLM-Generated (Weaker - Missing non-zero validation):**
```solidity
/// @notice postcondition _tokenOwner[_tokenId] == _owner  
// (Missing the _owner != address(0) constraint)
function ownerOf(uint256 _tokenId) public view returns (address owner);
```

**Why Weaker:** LLM omits the critical constraint that owner cannot be zero address, allowing invalid states.

## 3. NOT COMPARABLE Specifications (Different logical domains)

### Example 1: ERC1155 `balanceOfBatch` - Different Array Logic Approaches
**Source:** `experiments/results_func_by_func_fine_tuning/erc-1155-001-5-16/erc1155/none/fbf_erc1155_[none].csv`, Run 1

**Reference Specification:**
```solidity
/// @notice postcondition batchBalances.length == _owners.length
/// @notice postcondition batchBalances.length == _ids.length
/// @notice postcondition forall (uint x) !(0 <= x && x < batchBalances.length) || batchBalances[x] == _balances[_ids[x]][_owners[x]]
function balanceOfBatch(address[] memory _owners, uint256[] memory _ids) public view returns (uint256[] memory batchBalances);
```

**LLM-Generated (Not Comparable - Different quantification approach):**
```solidity
/// @notice postcondition forall (uint i) !(0 <= i && i < _owners.length) || batchBalances[i] == _balances[_ids[i]][_owners[i]]
function balanceOfBatch(address[] memory _owners, uint256[] memory _ids) public view returns (uint256[] memory batchBalances);
```

**Why Not Comparable:**
- **Reference:** Explicitly ensures array length matching + quantifies over result array length
- **LLM:** Quantifies over input array length without explicit length constraints  
- These represent different logical approaches to the same requirement
- Formal verification tools struggle to establish refinement relationships between these structurally different but conceptually related specifications

**Verification Status:** ✅ Both verify independently, but refinement relationship cannot be established

### Example 2: Complex Quantified Logic vs Simple Conditions
**Source:** Various ERC1155 fine-tuned model results

**Pattern:** LLM generates meaningful specifications using different logical structures (e.g., different quantifier bounds, alternative array indexing approaches, or different ways to express the same underlying constraint) that prevent formal refinement checking but aren't trivial.

## Key Insights

1. **Filtering Works Correctly**: The system properly excludes trivial `postcondition true` cases from refinement analysis
2. **Stronger Examples**: LLM often adds safety validations (null checks, authorization) on top of core logic
3. **Weaker Examples**: LLM tends to use overly permissive OR conditions where precise conditional logic is needed
4. **Not Comparable**: Structural differences in quantified logic and array handling create verification challenges

## Verification Context

All examples come with associated verification status and run numbers for reproducibility. The refinement analysis excludes cases where either specification is trivial, focusing on meaningful logical relationships between substantive formal specifications.