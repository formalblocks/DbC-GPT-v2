# ERC-7683 Solidity Version Downgrade: 0.8 → 0.5

## Overview

This document explains the version downgrade from Solidity 0.8.0 to 0.5.0 performed when creating the ERC-7683 verification harness (`ERC7683_template.sol`) from the production implementation (`ERC7683OrderDepositor.sol`).

## Files Involved

| File                        | Version | Purpose                                                                            |
| --------------------------- | ------- | ---------------------------------------------------------------------------------- |
| `ERC7683.sol`               | 0.5.0   | Type definitions and interfaces (IOriginSettler, IDestinationSettler)              |
| `ERC7683OrderDepositor.sol` | 0.8.0   | Production implementation with Permit2, token transfers, external dependencies     |
| `ERC7683_template.sol`      | 0.5.0   | **Verification harness** - simplified contract for solc-verify formal verification |

## Motivation

The downgrade was necessary to create a **formal verification harness** compatible with `solc-verify`:

1. **Tool Compatibility**: solc-verify requires Solidity 0.5.x
2. **Feature Restrictions**: solc-verify does not support:
   - Inline assembly
   - Complex `abi.*` helpers (decode, encode)
   - Dynamic decoding of nested structs
   - Many advanced Solidity 0.8 features
3. **Verification Focus**: Isolates core logic (nonce tracking, order state management) for formal proof generation
4. **Postcondition Generation**: Enables LLM-based specification generation without complex external dependencies

## Major Changes: What Was Removed

The verification harness removes production features to focus on verifiable logic:

### Removed Components

- ❌ **External dependencies**: OpenZeppelin (SafeERC20, SafeCast, IERC20)
- ❌ **Permit2 integration**: Signature verification, permit witness transfers
- ❌ **Token operations**: `safeTransferFrom()`, actual token handling
- ❌ **Complex type conversions**: AddressConverters, Bytes32ToAddress libraries
- ❌ **Abstract contract pattern**: Virtual functions, inheritance-based design
- ❌ **Immutable variables**: Runtime constants (PERMIT2, QUOTE_BEFORE_DEADLINE)
- ❌ **Dynamic encoding/decoding**: `abi.decode()` for complex structs

### Retained Core Logic

- ✅ **Nonce tracking**: `mapping(address => mapping(uint256 => bool)) usedNonces`
- ✅ **Order ID tracking**: `mapping(bytes32 => bool) openedOrders`
- ✅ **Interface implementation**: `openFor()`, `open()`, `resolveFor()`, `resolve()`
- ✅ **Basic validation**: Settlement contract, chain ID, order data type checks

## Solidity 0.8 → 0.5 Syntax Adaptations

| Feature            | Solidity 0.8.0                                                  | Solidity 0.5.0                                                  |
| ------------------ | --------------------------------------------------------------- | --------------------------------------------------------------- |
| **Error handling** | Custom errors: `error WrongChainId()` / `revert WrongChainId()` | String requires: `require(condition, "Wrong chain ID")`         |
| **Type casting**   | `SafeCast.toUint32()` / `SafeCast.toUint64()`                   | Direct casting: `uint32(...)`                                   |
| **Constants**      | Immutable: `IPermit2 public immutable PERMIT2`                  | Pure constant: `uint256 public constant SUPPORTED_CHAIN_ID = 1` |
| **ABI encoding**   | `abi.decode(data, (AcrossOrderData))`                           | Avoided entirely; uses hardcoded struct initialization          |
| **Library calls**  | `SafeERC20.safeTransferFrom()`, `AddressConverters.toBytes32()` | Removed                                                         |
| **Struct returns** | Requires `ABIEncoderV2`                                         | Requires `pragma experimental ABIEncoderV2` (both)              |

## Formal Specifications Added

The verification harness adds solc-verify annotations for formal verification:

```solidity
/// @notice precondition order.originSettler == address(this)
/// @notice precondition !usedNonces[order.user][order.nonce]
/// @notice postcondition usedNonces[order.user][order.nonce]
/// @notice postcondition openedOrders[bytes32(order.nonce)]
function openFor(...) external { ... }
```

These annotations enable automatic verification of correctness properties like:

- Nonce replay protection
- Order uniqueness guarantees
- State transition invariants

## Trade-offs

| Lost                                        | Gained                                              |
| ------------------------------------------- | --------------------------------------------------- |
| Production-ready token handling             | Formal verification of core logic                   |
| Security features (Permit2 signatures)      | Simplified reasoning about contract behavior        |
| Gas optimizations (SafeCast, custom errors) | Compatibility with solc-verify toolchain            |
| Full ERC-7683 feature set                   | LLM-friendly contract structure for spec generation |
