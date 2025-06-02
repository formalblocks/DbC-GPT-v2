```solidity

pragma solidity ^0.5.0;

contract ERC123Identity {
    address public owner;
    address public trustedVerifier;

    struct Identity {
        address owner;
        address dataHash;
        bool verified;
    }

    mapping(bytes32 => Identity) private identities;
    mapping(address => mapping(bytes32 => bool)) private consents;

    /// @notice postcondition identities[identityId].dataHash == address(0)
    /// @notice postcondition identities[identityId].verified == false
    /// @notice postcondition identities[identityId].owner == msg.sender
    /// @notice postcondition !(__verifier_old_address(identities[identityId].owner) != address(0)) ||  identities[identityId].owner == address(0)
    function createIdentity(bytes32 identityId) external;

    /// @notice postcondition identities[identityId].owner == msg.sender || consents[msg.sender][identityId]
    /// @notice postcondition !(__verifier_old_bool(identities[identityId].verified) && __verifier_old_address(identities[identityId].dataHash) != newDataHash) || identities[identityId].verified == false
    /// @notice postcondition !(__verifier_old_address(identities[identityId].dataHash) == newDataHash) || identities[identityId].verified == __verifier_old_bool(identities[identityId].verified)
    /// @notice postcondition identities[identityId].dataHash == newDataHash
    function updateIdentity(bytes32 identityId, address newDataHash) external;

    /// @notice postcondition ret == identities[identityId].verified
    function verifyIdentity(bytes32 identityId) external view returns (bool ret);
    
    /// @notice postcondition identities[identityId].owner == msg.sender
    /// @notice postcondition consents[caller][identityId] == true
    function giveConsent(address caller, bytes32 identityId) external;

    /// @notice postcondition identities[identityId].owner == msg.sender
    /// @notice postcondition consents[caller][identityId] == false
    function revokeConsent(address caller, bytes32 identityId) external;

    /// @notice postcondition consents[caller][identityId] == ret
    function hasConsent(address caller, bytes32 identityId) external view returns (bool ret);

    /// @notice postcondition identities[identityId].verified == verified
    function verifyIdentityByTrustedVerifier(bytes32 identityId, bool verified) external;
}
```