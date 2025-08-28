---
eip: X
title: Conditional Multi-State Token Standard
description: A token standard for conditional state transitions with time-based and threshold-based mechanics
author: DbC-GPT Research Team
discussions-to: https://ethereum-magicians.org/t/erc-x-conditional-multi-state-token-standard
status: Draft
type: Standards Track
category: ERC
created: 2024-01-01
requires: 165
---

## Abstract

This EIP proposes a standard for tokens that can exist in multiple states with conditional transitions between them. The standard introduces time-based mechanics, threshold-based state changes, and complex approval systems that challenge automated verification while remaining implementable.

## Motivation

Existing token standards like ERC-20 and ERC-721 provide basic functionality but lack sophisticated state management capabilities. Many real-world use cases require tokens that can:

1. Transition between different states based on conditions
2. Have time-dependent behaviors
3. Implement threshold-based mechanics
4. Support complex approval and delegation systems

This standard addresses these needs while providing a challenging test case for formal verification tools.

## Specification

### Token States

Each token can exist in one of four states:
- `INACTIVE` (0): Token is dormant
- `ACTIVE` (1): Token is operational
- `LOCKED` (2): Token is temporarily restricted
- `BURNED` (3): Token is permanently destroyed

### Core Interface

```solidity
interface IERCX {
    // Events
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    event StateTransition(uint256 indexed tokenId, uint8 fromState, uint8 toState, uint256 timestamp);
    event ConditionalApproval(address indexed owner, address indexed approved, uint256 indexed tokenId, uint256 condition);
    event ThresholdReached(uint256 indexed tokenId, uint256 threshold, uint256 currentValue);
    event TimeBasedAction(uint256 indexed tokenId, uint256 actionType, uint256 timestamp);

    // Core functions
    function balanceOf(address owner) external view returns (uint256);
    function ownerOf(uint256 tokenId) external view returns (address);
    function approve(address to, uint256 tokenId) external;
    function getApproved(uint256 tokenId) external view returns (address);
    function setApprovalForAll(address operator, bool approved) external;
    function isApprovedForAll(address owner, address operator) external view returns (bool);
    function transferFrom(address from, address to, uint256 tokenId) external;
    
    // State management
    function getTokenState(uint256 tokenId) external view returns (uint8);
    function transitionState(uint256 tokenId, uint8 newState) external;
    function canTransitionState(uint256 tokenId, uint8 newState) external view returns (bool);
    
    // Conditional mechanics
    function setConditionalApproval(address to, uint256 tokenId, uint256 condition) external;
    function executeConditionalTransfer(uint256 tokenId, address to) external;
    function updateThreshold(uint256 tokenId, uint256 newThreshold) external;
    function getThreshold(uint256 tokenId) external view returns (uint256);
    
    // Time-based functions
    function setTimeBasedAction(uint256 tokenId, uint256 actionType, uint256 executeAt) external;
    function executeTimeBasedAction(uint256 tokenId) external;
    function getTimeBasedAction(uint256 tokenId) external view returns (uint256 actionType, uint256 executeAt);
}
```

### State Transition Rules

1. `INACTIVE` → `ACTIVE`: Always allowed by owner
2. `ACTIVE` → `LOCKED`: Allowed by owner or when threshold conditions are met
3. `LOCKED` → `ACTIVE`: Allowed after time delay or by authorized operator
4. Any state → `BURNED`: Irreversible, only by owner
5. `BURNED` → Any state: Not allowed

### Conditional Approval System

Tokens can have conditional approvals that are only valid when specific conditions are met:
- Threshold-based conditions
- Time-based conditions
- State-dependent conditions
- Multi-signature requirements

### Implementation Requirements

1. **State Validation**: All state transitions must be validated according to the rules
2. **Time Management**: Contracts must handle time-based mechanics correctly
3. **Threshold Tracking**: Contracts must maintain and update threshold values
4. **Event Emission**: All state changes must emit appropriate events
5. **Access Control**: Proper authorization checks for all operations

## Rationale

This standard introduces complexity in several dimensions:

1. **State Management**: Multiple states with conditional transitions
2. **Time Dependencies**: Actions that depend on block timestamps
3. **Threshold Logic**: Conditions based on accumulated values
4. **Complex Approvals**: Multi-layered approval mechanisms

These features create verification challenges that distinguish between basic and advanced formal verification capabilities.

## Backwards Compatibility

This standard is not backwards compatible with existing token standards due to its fundamentally different approach to token management. However, it can coexist with other standards in the same ecosystem.

## Security Considerations

1. **Time Manipulation**: Contracts should be resistant to timestamp manipulation
2. **State Consistency**: State transitions must maintain contract invariants
3. **Access Control**: Proper validation of permissions for all operations
4. **Reentrancy**: Protection against reentrancy attacks in state transitions
5. **Integer Overflow**: Safe arithmetic operations for threshold calculations

## Copyright

Copyright and related rights waived via [CC0](../LICENSE.md).