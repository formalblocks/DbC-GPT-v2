# EIP-X: Evolving Multi-Token Standard

## Overview

This standard proposes a novel multi-token contract that introduces two primary features on top of a base similar to ERC-1155: Token Evolution and Internal Exchange.

Token Evolution allows tokens to change their state and metadata over time based on predefined rules, such as a required holding period. Each evolution advances the token to a new "stage," which can alter its properties and associated URI.
Internal Exchange provides a native mechanism for users to swap one type of token for another within the same contract, based on administrator-set exchange rates.

This proposal defines the interface for managing token balances, approvals, transfers, evolution, and exchanges. Function names are intentionally distinct from ERC-1155 to prevent interface clashes and highlight the unique functionality.

## Motivation

The existing ERC-1155 standard provides an excellent framework for managing multiple token types in a single contract. However, it lacks native support for dynamic tokens whose attributes or metadata can change based on on-chain conditions. Such "evolving" tokens are valuable for applications like gaming (e.g., items that level up), decentralized identity (e.g., reputation that grows over time), or dynamic art.
Furthermore, projects utilizing multiple fungible token types often require a decentralized exchange for users to swap between them. By integrating a simple, integer-based exchange mechanism directly into the token contract, this standard reduces complexity, lowers gas costs for users, and removes reliance on external DEX protocols for basic internal token swaps.

This EIP aims to provide a standardized interface for these advanced functionalities, enabling richer and more self-contained token ecosystems.

## Specification

The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.
A compliant contract MUST implement the following interface:

```solidity
interface IERCX {
    // --- Events ---

    event TransferSingle(address indexed operator, address indexed from, address indexed to, uint256 id, uint256 amount);
    event TransferBatch(address indexed operator, address indexed from, address indexed to, uint256[] ids, uint256[] amounts);
    event ApprovalForAll(address indexed account, address indexed operator, bool approved);
    event URI(string value, uint256 indexed id);
    event TokenEvolution(uint256 indexed tokenId, uint8 indexed oldEvolutionStage, uint8 indexed newEvolutionStage, bytes data);
    event ConsentGiven(address indexed owner, address indexed operator, uint256 indexed tokenId);
    event ConsentRevoked(address indexed owner, address indexed operator, uint256 indexed tokenId);
    event TokenRateUpdated(uint256 indexed tokenId, uint256 newRate);
    event TokensExchanged(address indexed user, uint256 indexed fromTokenId, uint256 indexed toTokenId, uint256 fromAmount, uint256 toAmount);

    // --- Balance Functions ---

    /**
     * @dev Gets the balance of a single token type for a single address.
     */
    function getTokenBalance(address owner, uint256 tokenId) external view returns (uint256);

    /**
     * @dev Gets the balance of multiple token types for multiple addresses.
     */
    function getBatchTokenBalance(address[] calldata owners, uint256[] calldata tokenIds) external view returns (uint256[] memory);

    // --- Approval Functions ---

    /**
     * @dev Enables or disables approval for a third party ("operator") to manage all of `msg.sender`'s assets.
     */
    function setProxyForAll(address operator, bool approved) external;

    /**
     * @dev Queries the approval status of an operator for a given owner.
     */
    function isProxyForAll(address owner, address operator) external view returns (bool);

    // --- Transfer Functions ---

    /**
     * @dev Transfers `amount` tokens of `tokenId` from `from` to `to`.
     */
    function transferTokenFrom(address from, address to, uint256 tokenId, uint256 amount, bytes calldata data) external;

    /**
     * @dev Transfers multiple token types from `from` to `to`.
     */
    function batchTransferTokenFrom(address from, address to, uint256[] calldata tokenIds, uint256[] calldata amounts, bytes calldata data) external;

    // --- Token Exchange Functionality ---

    /**
     * @dev Sets the exchange rate for a given token ID. Access control is RECOMMENDED.
     */
    function setTokenRate(uint256 tokenId, uint256 rate) external;

    /**
     * @dev Exchanges a specified amount of one token type for another based on set rates.
     */
    function exchangeTokens(uint256 fromTokenId, uint256 toTokenId, uint256 fromAmount) external;

    // --- Evolution Functionality ---

    /**
     * @dev Returns the current evolution stage of a token.
     */
    function evolutionStage(uint256 tokenId) external view returns (uint8);

    /**
     * @dev Checks if a token meets the requirements to evolve.
     */
    function canEvolve(uint256 tokenId) external view returns (bool);

    /**
     * @dev Evolves a token to its next stage if conditions are met.
     */
    function evolveToken(uint256 tokenId, bytes calldata data) external returns (bool);

    /**
     * @dev Returns the URI for a given token ID, which may depend on its evolution stage.
     */
    function uri(uint256 id) external view returns (string memory);

    /**
     * @dev Returns the detailed evolution data for a token.
     */
    function evolutionDataOf(uint256 tokenId) external view returns (uint256 stage, uint256 lastEvolutionTime, uint256 requiredHoldTime);

    /**
     * @dev Grants another address (`operator`) consent to evolve a token on the owner's behalf.
     */
    function giveEvolutionConsent(address operator, uint256 tokenId) external;

    /**
     * @dev Revokes evolution consent from an operator.
     */
    function revokeEvolutionConsent(address operator, uint256 tokenId) external;

    /**
     * @dev Checks if an operator has consent to evolve a token for a given owner.
     */
    function hasEvolutionConsent(address owner, address operator, uint256 tokenId) external view returns (bool);
}

```

## Token Evolution Logic

A token starts at stage 0 (no evolution data) or a specified initial stage upon minting.
To evolve, a token must be held for a `requiredHoldTime`.
Each evolution increases the token's stage by 1 and updates its `lastEvolutionTime`. The `requiredHoldTime` for the next stage typically increases (e.g., doubles).
The token's URI SHOULD change with its stage to reflect its new state.
Evolution can be triggered by one of three parties:
1.  The current owner of the token (`getTokenBalance(sender, tokenId) > 0`).
2.  The original owner of the token (`evolution.originalOwner == sender`).
3.  An operator who has been granted consent by the original owner (`hasEvolutionConsent(evolution.originalOwner, sender, tokenId)`).

Token Exchange Logic
An administrator MUST set a positive integer rate for each token type via `setTokenRate`. This rate represents the token's relative value.
A user can call exchangeTokens to swap fromAmount of fromTokenId for an amount of toTokenId.
The resulting toAmount is calculated as (fromAmount * fromRate) / toRate.
The transaction MUST revert if the exchange would result in a fractional amount of the toTokenId (i.e., (fromAmount * fromRate) % toRate != 0).
Rationale

Struct-based Account Storage: Using an AccountInfo struct to store tokenCount and proxy mappings for each address (i.e., mapping(address => AccountInfo)), rather than the dual mapping(uint256 => mapping(address => uint256)) and mapping(address => mapping(address => bool)) of ERC-1155, can improve data locality and potentially simplify logic within the contract.

Distinct Function Naming: Functions like getTokenBalance and transferTokenFrom are deliberately named differently from their ERC-1155 counterparts (balanceOf, safeTransferFrom). This prevents interface ID collisions and makes it clear to developers and tools that this contract, while similar, has a different feature set and is not a drop-in replacement for ERC-1155.

Integer-Only Exchange: The requirement that token exchanges result in whole numbers simplifies the mechanism and avoids the complexity and potential loss of value associated with "dust" (very small fractional balances). This makes the internal exchange suitable for straightforward swaps where precision is secondary to convenience.

Flexible Evolution Permissions: Allowing the original owner and consented operators (in addition to the current owner) to trigger evolution provides flexibility. For example, a game developer (the original owner) could trigger a global "world event" that evolves all relevant items, regardless of who currently holds them.

## Backwards Compatibility

This standard is not directly backward-compatible with ERC-20, ERC-721, or ERC-1155 due to the different function signatures. However, it is conceptually based on ERC-1155 and could be adapted to work with marketplaces and wallets designed for multi-token standards, provided they are updated to recognize the new interface.

## Reference Implementation

The full reference implementation, which implements the concepts of EIP-X within a contract named `ERC845`, can be found in the `ercx.sol` file.

## Security Considerations

Access Control on `setTokenRate`: The `setTokenRate` function is critical to the economic model of the exchange. The provided reference implementation lacks any access control on this function, making it vulnerable to manipulation. A production-ready implementation MUST protect this function with strong access control (e.g., `onlyOwner` or a multi-sig governance mechanism).

Evolution Conditions: The conditions for `evolveToken` must be carefully designed. The `requiredHoldTime` prevents users from rapidly cycling through evolution stages. Developers should be aware that the `now` timestamp can be slightly manipulated by miners, though this is less of a concern for long hold times.

Consent Management: The consent mechanism contains a significant logical inconsistency. The `giveEvolutionConsent` function allows *any* current token holder to grant consent to an operator. However, the `evolveToken` function only checks for consent that was granted by the *original owner*. This means any consent granted by subsequent owners is ineffective. Users must be educated on the implications of giving consent, as a consented operator can trigger an evolution that may have economic or functional consequences for the token owner. Implementations should resolve this ambiguity.

No `onERC1155Received` Hook: The reference implementation's transfer functions (`_transferTokenFrom`, `_batchTransferTokenFrom`) lack the `onERC1155Received` check that is standard in ERC-1155. This means tokens can be transferred to a contract that does not know how to handle them, potentially locking the tokens forever. Compliant implementations SHOULD re-introduce a safe transfer check mechanism.