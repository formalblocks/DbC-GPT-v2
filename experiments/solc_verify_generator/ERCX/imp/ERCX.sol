// SPDX-License-Identifier: MIT
pragma solidity ^0.5.0;

import "./Address.sol";
import "./Context.sol";
import "./ERC165.sol";

/**
 * @title ERC-X Evolving Multi-Token Standard
 * @dev Implementation of the ERC-X token standard, with modifications.
 * This version refactors storage for accounts, renames functions to avoid
 * collision with ERC1155, and adds a token exchange mechanism.
 */
contract ERCX is Context, ERC165 {
    using Address for address;

    // Struct to hold account-specific data, including token balances and operator approvals.
    struct AccountInfo {
        // Mapping from token ID to a balance amount
        mapping(uint256 => uint256) tokenCount;
        // Mapping from operator address to approval status
        mapping(address => bool) proxy;
    }

    // Struct for token evolution data.
    struct EvolutionData {
        uint8 stage;
        uint256 creationTime;
        uint256 lastEvolutionTime;
        uint256 requiredHoldTime;
        address originalOwner;
    }

    // --- Storage ---

    mapping(address => AccountInfo) private accounts;
    mapping(uint256 => uint256) public tokenRates;
    mapping(address => mapping(uint256 => mapping(address => bool))) private _evolutionConsents;
    mapping(uint256 => EvolutionData) private _evolutions;
    mapping(uint256 => string) private _tokenURIs;
    string private _baseURI;

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


    constructor(string memory baseURI) public {
        _baseURI = baseURI;
    }

    // --- Balance Functions ---

    /**
     * @dev Gets the balance of a single token type for a single address.
     * @param owner The address to query the balance of.
     * @param tokenId The ID of the token.
     * @return result The balance of the owner for the specified token ID.
     * @notice precondition owner != address(0)
     * @notice postcondition result == accounts[owner].tokenCount[tokenId]
     */
    function getTokenBalance(address owner, uint256 tokenId) public view returns (uint256 result) {
        require(owner != address(0), "ERCX: balance query for the zero address");
        return accounts[owner].tokenCount[tokenId];
    }

    /**
     * @dev Gets the balance of multiple token types for multiple addresses.
     * @param owners An array of addresses to query balances for.
     * @param tokenIds An array of token IDs to query balances for.
     * @return result An array of balances.
     */
    function getBatchTokenBalance(address[] memory owners, uint256[] memory tokenIds) public view returns (uint256[] memory result) {
        require(owners.length == tokenIds.length, "ERCX: owners and tokenIds length mismatch");
        uint256[] memory batchBalances = new uint256[](owners.length);
        for (uint256 i = 0; i < owners.length; ++i) {
            batchBalances[i] = getTokenBalance(owners[i], tokenIds[i]);
        }
        return batchBalances;
    }

    // --- Approval Functions ---

    /**
     * @dev Sets or unsets the approval of a given operator.
     * @param operator Address to be approved as an operator.
     * @param approved True if the operator is approved, false to revoke approval.
     * @notice emits ApprovalForAll
     */
    function setProxyForAll(address operator, bool approved) public {
        accounts[_msgSender()].proxy[operator] = approved;
        emit ApprovalForAll(_msgSender(), operator, approved);
    }

    /**
     * @dev Checks if an address is an approved operator for another address.
     * @param owner The address that owns the tokens.
     * @param operator The address that acts on behalf of the owner.
     * @return result True if the operator is approved, false otherwise.
     * @notice postcondition result == accounts[owner].proxy[operator]
     */
    function isProxyForAll(address owner, address operator) public view returns (bool result) {
        return accounts[owner].proxy[operator];
    }

    // --- Transfer Functions ---

    /**
     * @dev Transfers `amount` tokens of `tokenId` from `from` to `to`.
     * @notice emits TransferSingle
     */
    function transferTokenFrom(address from, address to, uint256 tokenId, uint256 amount, bytes memory data) public {
        require(from == _msgSender() || accounts[from].proxy[_msgSender()], "ERCX: caller is not owner nor approved");
        _transferTokenFrom(from, to, tokenId, amount, data);
    }

    /**
     * @dev Transfers multiple token types from `from` to `to`.
     * @notice emits TransferBatch
     */
    function batchTransferTokenFrom(address from, address to, uint256[] memory tokenIds, uint256[] memory amounts, bytes memory data) public {
        require(from == _msgSender() || accounts[from].proxy[_msgSender()], "ERCX: transfer caller is not owner nor approved");
        _batchTransferTokenFrom(from, to, tokenIds, amounts, data);
    }

    // --- Internal Transfer Logic ---

    /**
     * @notice precondition to != address(0)
     * @notice precondition accounts[from].tokenCount[tokenId] >= amount
     * @notice postcondition accounts[from].tokenCount[tokenId] == __verifier_old_uint(accounts[from].tokenCount[tokenId]) - amount
     * @notice postcondition accounts[to].tokenCount[tokenId] == __verifier_old_uint(accounts[to].tokenCount[tokenId]) + amount
     * @notice emits TransferSingle
     */
    function _transferTokenFrom(address from, address to, uint256 tokenId, uint256 amount, bytes memory data) internal {
        require(to != address(0), "ERCX: transfer to the zero address");
        address operator = _msgSender();
        _beforeTokenTransfer(operator, from, to, _asSingletonArray(tokenId), _asSingletonArray(amount), data);
        uint256 fromBalance = accounts[from].tokenCount[tokenId];
        require(fromBalance >= amount, "ERCX: insufficient balance for transfer");
        accounts[from].tokenCount[tokenId] = fromBalance - amount;
        accounts[to].tokenCount[tokenId] += amount;
        if (amount > 0 && _evolutions[tokenId].stage > 0 && fromBalance == amount) {
            _evolutions[tokenId].lastEvolutionTime = now;
        }
        emit TransferSingle(operator, from, to, tokenId, amount);
        _doSafeTransferAcceptanceCheck(operator, from, to, tokenId, amount, data);
    }

    /**
     * @notice precondition tokenIds.length == amounts.length
     * @notice precondition to != address(0)
     * @notice emits TransferBatch
     */
    function _batchTransferTokenFrom(address from, address to, uint256[] memory tokenIds, uint256[] memory amounts, bytes memory data) internal {
        require(tokenIds.length == amounts.length, "ERCX: ids and amounts length mismatch");
        require(to != address(0), "ERCX: transfer to the zero address");
        address operator = _msgSender();
        _beforeTokenTransfer(operator, from, to, tokenIds, amounts, data);
        for (uint256 i = 0; i < tokenIds.length; ++i) {
            uint256 tokenId = tokenIds[i];
            uint256 amount = amounts[i];
            uint256 fromBalance = accounts[from].tokenCount[tokenId];
            require(fromBalance >= amount, "ERCX: insufficient balance for transfer");
            accounts[from].tokenCount[tokenId] = fromBalance - amount;
            accounts[to].tokenCount[tokenId] += amount;
            if (amount > 0 && _evolutions[tokenId].stage > 0 && fromBalance == amount) {
                _evolutions[tokenId].lastEvolutionTime = now;
            }
        }
        emit TransferBatch(operator, from, to, tokenIds, amounts);
        _doSafeBatchTransferAcceptanceCheck(operator, from, to, tokenIds, amounts, data);
    }

    // --- Token Exchange Functionality ---

    /**
     * @dev Sets the exchange rate for a given token ID.
     * @param tokenId The ID of the token.
     * @param rate The exchange rate for the token.
     * @notice precondition rate > 0
     * @notice postcondition tokenRates[tokenId] == rate
     * @notice emits TokenRateUpdated
     */
    function setTokenRate(uint256 tokenId, uint256 rate) public { 
        require(rate > 0, "ERCX: Rate must be positive");
        tokenRates[tokenId] = rate;
        emit TokenRateUpdated(tokenId, rate);
    }

    /**
     * @dev Exchanges a specified amount of one token type for another.
     * @param fromTokenId The ID of the token to be exchanged.
     * @param toTokenId The ID of the token to be received.
     * @param fromAmount The amount of the `fromTokenId` to exchange.
     * @notice emits TokensExchanged
     * @notice emits TransferSingle
     */
    function exchangeTokens(uint256 fromTokenId, uint256 toTokenId, uint256 fromAmount) public {
        address user = _msgSender();
        require(fromTokenId != toTokenId, "ERCX: cannot exchange a token for itself");
        uint256 fromRate = tokenRates[fromTokenId];
        uint256 toRate = tokenRates[toTokenId];
        require(fromRate > 0 && toRate > 0, "ERCX: exchange rates for tokens must be set and positive");
        uint256 userFromBalance = accounts[user].tokenCount[fromTokenId];
        require(userFromBalance >= fromAmount, "ERCX: insufficient balance for exchange");
        uint256 totalValue = fromAmount * fromRate;
        require(totalValue % toRate == 0, "ERCX: exchange results in a non-integer amount");
        uint256 toAmount = totalValue / toRate;
        accounts[user].tokenCount[fromTokenId] = userFromBalance - fromAmount;
        accounts[user].tokenCount[toTokenId] += toAmount;
        emit TokensExchanged(user, fromTokenId, toTokenId, fromAmount, toAmount);
        emit TransferSingle(user, user, address(0), fromTokenId, fromAmount);
        emit TransferSingle(user, address(0), user, toTokenId, toAmount);
    }

    // --- Evolution Functionality ---

    /**
     * @notice postcondition result == _evolutions[tokenId].stage
     */
    function evolutionStage(uint256 tokenId) public view returns (uint8 result) {
        return _evolutions[tokenId].stage;
    }

    /**
     */
    function canEvolve(uint256 tokenId) public view returns (bool result) {
        EvolutionData storage evolution = _evolutions[tokenId];
        if (evolution.stage == 0 || evolution.stage >= 5) {
            return false;
        }
        return now >= evolution.lastEvolutionTime + evolution.requiredHoldTime;
    }

    /**
     * @notice emits TokenEvolution
     * @notice emits URI
     */
    function evolveToken(uint256 tokenId, bytes memory data) public returns (bool) {
        EvolutionData storage evolution = _evolutions[tokenId];
        address sender = _msgSender();
        require(evolution.stage > 0, "ERCX: token has no evolution capability");
        require(evolution.stage < 5, "ERCX: token already at maximum evolution stage");
        require(
            getTokenBalance(sender, tokenId) > 0 || 
            hasEvolutionConsent(evolution.originalOwner, sender, tokenId) ||
            evolution.originalOwner == sender,
            "ERCX: caller cannot evolve this token"
        );
        require(canEvolve(tokenId), "ERCX: evolution requirements not met");
        uint8 oldStage = evolution.stage;
        evolution.stage += 1;
        evolution.lastEvolutionTime = now;
        evolution.requiredHoldTime = evolution.requiredHoldTime * 2;
        _setTokenURI(tokenId, _generateNewURI(tokenId, evolution.stage));
        emit TokenEvolution(tokenId, oldStage, evolution.stage, data);
        return true;
    }

    function uri(uint256 id) public view returns (string memory) {
        string memory tokenURI = _tokenURIs[id];
        if (bytes(tokenURI).length > 0) {
            return tokenURI;
        }
        return _generateNewURI(id, _evolutions[id].stage);
    }

    /**
     * @notice postcondition stage == _evolutions[tokenId].stage
     * @notice postcondition lastEvolutionTime == _evolutions[tokenId].lastEvolutionTime
     * @notice postcondition requiredHoldTime == _evolutions[tokenId].requiredHoldTime
     */
    function evolutionDataOf(uint256 tokenId) public view returns (uint256 stage, uint256 lastEvolutionTime, uint256 requiredHoldTime) {
        EvolutionData storage evolution = _evolutions[tokenId];
        return (evolution.stage, evolution.lastEvolutionTime, evolution.requiredHoldTime);
    }

    /**
     * @notice emits ConsentGiven
     */
    function giveEvolutionConsent(address operator, uint256 tokenId) public {
        _evolutionConsents[_msgSender()][tokenId][operator] = true;
        emit ConsentGiven(_msgSender(), operator, tokenId);
    }

    /**
     * @notice emits ConsentRevoked
     */
    function revokeEvolutionConsent(address operator, uint256 tokenId) public {
        _evolutionConsents[_msgSender()][tokenId][operator] = false;
        emit ConsentRevoked(_msgSender(), operator, tokenId);
    }

    /**
     * @notice postcondition result == _evolutionConsents[owner][tokenId][operator]
     */
    function hasEvolutionConsent(address owner, address operator, uint256 tokenId) public view returns (bool result) {
        return _evolutionConsents[owner][tokenId][operator];
    }

    // --- Minting ---

    /**
     * @notice precondition to != address(0)
     * @notice postcondition accounts[to].tokenCount[id] == __verifier_old_uint(accounts[to].tokenCount[id]) + amount
     * @notice emits TransferSingle
     * @notice emits URI
     */
    function _mintEvolvable(address to, uint256 id, uint256 amount, uint8 initialStage, uint256 requiredHoldTime, bytes memory data) internal {
        require(to != address(0), "ERCX: mint to the zero address");
        address operator = _msgSender();
        _beforeTokenTransfer(operator, address(0), to, _asSingletonArray(id), _asSingletonArray(amount), data);
        accounts[to].tokenCount[id] += amount;
        if (initialStage > 0 && _evolutions[id].stage == 0) {
            _evolutions[id] = EvolutionData({
                stage: initialStage,
                creationTime: now,
                lastEvolutionTime: now,
                requiredHoldTime: requiredHoldTime,
                originalOwner: to
            });
            _setTokenURI(id, _generateNewURI(id, initialStage));
        }
        emit TransferSingle(operator, address(0), to, id, amount);
        _doSafeTransferAcceptanceCheck(operator, address(0), to, id, amount, data);
    }

    // --- Internal Helper Functions ---

    /**
     * @notice emits URI
     */
    function _setTokenURI(uint256 tokenId, string memory tokenURI) internal {
        _tokenURIs[tokenId] = tokenURI;
        emit URI(tokenURI, tokenId);
    }

    function _generateNewURI(uint256 tokenId, uint8 stage) internal view returns (string memory) {
        string memory tokenIdStr = _uint2str(tokenId);
        string memory stageStr = _uint2str(stage);
        return _strConcat(_baseURI, tokenIdStr, "_", stageStr, ".json");
    }

    function _beforeTokenTransfer(address operator, address from, address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data) internal {
        // Hook for custom logic before transfers.
    }

    function _doSafeTransferAcceptanceCheck(address operator, address from, address to, uint256 id, uint256 amount, bytes memory data) private {
        if (to.isContract()) {
            // e.g., call to.onERC1155Received(operator, from, id, amount, data)
        }
    }

    function _doSafeBatchTransferAcceptanceCheck(address operator, address from, address to, uint256[] memory ids, uint256[] memory amounts, bytes memory data) private {
        if (to.isContract()) {
            // e.g., call to.onERC1155BatchReceived(operator, from, ids, amounts, data)
        }
    }

    function _uint2str(uint value) internal pure returns (string memory) {
        if (value == 0) return "0";
        uint temp = value;
        uint digits;
        while (temp != 0) {
            digits++;
            temp /= 10;
        }
        bytes memory buffer = new bytes(digits);
        while (value != 0) {
            digits -= 1;
            buffer[digits] = bytes1(uint8(48 + uint256(value % 10)));
            value /= 10;
        }
        return string(buffer);
    }

    function _strConcat(string memory a, string memory b, string memory c, string memory d, string memory e) internal pure returns (string memory) {
        bytes memory ba = bytes(a);
        bytes memory bb = bytes(b);
        bytes memory bc = bytes(c);
        bytes memory bd = bytes(d);
        bytes memory be = bytes(e);
        string memory result = new string(ba.length + bb.length + bc.length + bd.length + be.length);
        bytes memory bresult = bytes(result);
        uint k = 0;
        for (uint i = 0; i < ba.length; i++) bresult[k++] = ba[i];
        for (uint i = 0; i < bb.length; i++) bresult[k++] = bb[i];
        for (uint i = 0; i < bc.length; i++) bresult[k++] = bc[i];
        for (uint i = 0; i < bd.length; i++) bresult[k++] = bd[i];
        for (uint i = 0; i < be.length; i++) bresult[k++] = be[i];
        return string(bresult);
    }

    function _asSingletonArray(uint256 element) private pure returns (uint256[] memory) {
        uint256[] memory array = new uint256[](1);
        array[0] = element;
        return array;
    }
}