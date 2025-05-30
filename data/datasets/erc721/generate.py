import textwrap
import random
import json

from ..template import ContractTemplate, FunctionTemplate

class BalanceOf(FunctionTemplate):
    name = "balanceOf"
    descriptions = [
        r"@notice Count all NFTs assigned to an owner",
        r"Returns the number of NFTs owned by a specific address.",
        r"Gets the token balance of a given owner.",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @param {_owner} An address for whom to query the balance
            @return The number of NFTs owned by `{_owner}`, possibly zero
            """
        ),
        textwrap.dedent(
            """
            {_owner} is the address to query the balance for.
            Returns the count of NFTs held by the owner.
            """
        ),
    ]
    sig_desc = """function balanceOf(address _owner) external view returns (uint256);"""
    postconditions = [
        """/// @notice postcondition {_ownedTokensCount}[{_owner}] == {balance}""",
    ]
    sig_spec = """function balanceOf(address {_owner}) external view returns (uint256 {balance});"""
    params_vars = {
        "_owner": ["_owner", "ownerAddress", "account"],
        "balance": ["balance", "count", "numTokens"],
    }

class OwnerOf(FunctionTemplate):
    name = "ownerOf"
    descriptions = [
        r"@notice Find the owner of an NFT",
        r"Returns the owner of a specific NFT.",
        r"Retrieves the address of the owner of a token.",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @param {_tokenId} The identifier for an NFT
            @return The address of the owner of the NFT
            """
        ),
        textwrap.dedent(
            """
            {_tokenId} is the ID of the token to query the owner for.
            Returns the owner's address.
            """
        ),
    ]
    sig_desc = """function ownerOf(uint256 _tokenId) external view returns (address);"""
    postconditions = [
        """/// @notice postcondition {_tokenOwner}[{_tokenId}] == {owner}""",
        """/// @notice postcondition {owner} != address(0)""",
    ]
    sig_spec = """function ownerOf(uint256 {_tokenId}) external view returns (address {owner});"""
    params_vars = {
        "_tokenId": ["_tokenId", "tokenId", "ID"],
        "owner": ["owner", "tokenHolder", "possessor"],
    }

class Approve(FunctionTemplate):
    name = "approve"
    descriptions = [
        r"@notice Change or reaffirm the approved address for an NFT",
        r"Approves an address to operate on a specific NFT.",
        r"Sets the approval for a given address to transfer a single token.",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @param {_approved} The new approved NFT controller
            @param {_tokenId} The NFT to approve
            """
        ),
        textwrap.dedent(
            """
            {_approved} is the address to grant approval to.
            {_tokenId} is the ID of the token to be approved.
            """
        ),
    ]
    sig_desc = """function approve(address _approved, uint256 _tokenId) external;"""
    postconditions = [
        """/// @notice postcondition {_tokenApprovals}[{_tokenId}] == {_approved}""",
    ]
    sig_spec = """function approve(address {_approved}, uint256 {_tokenId}) external;"""
    params_vars = {
        "_approved": ["_approved", "approvedAddress", "spender"],
        "_tokenId": ["_tokenId", "tokenId", "nftId"],
    }

class GetApproved(FunctionTemplate):
    name = "getApproved"
    descriptions = [
        r"@notice Get the approved address for a single NFT",
        r"Returns the approved address for a specific token, if any.",
        r"Queries the address approved to manage an NFT.",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @param {_tokenId} The NFT to find the approved address for
            @return The approved address for this NFT, or the zero address if there is none
            """
        ),
        textwrap.dedent(
            """
            {_tokenId} is the ID of the token.
            Returns the address approved for the token.
            """
        ),
    ]
    sig_desc = """function getApproved(uint256 _tokenId) external view returns (address);"""
    postconditions = [
        """/// @notice postcondition {_tokenApprovals}[{_tokenId}] == {approved}""",
    ]
    sig_spec = """function getApproved(uint256 _tokenId) external view returns (address {approved});"""
    params_vars = {
        "_tokenId": ["_tokenId", "ID", "tokenIdentifier"],
        "approved": ["approved", "approvedForToken", "controller"],
    }

class SetApprovalForAll(FunctionTemplate):
    name = "setApprovalForAll"
    descriptions = [
        r"@notice Enable or disable approval for a third party ('operator') to manage all of `msg.sender`'s assets",
        r"Approves or revokes an operator to manage all of the sender's tokens.",
        r"Sets or unsets the approval of a given operator for all tokens of the caller.",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @param {_operator} Address to add to the set of authorized operators
            @param {_approved} True if the operator is approved, false to revoke approval
            """
        ),
        textwrap.dedent(
            """
            {_operator} is the address of the operator.
            {_approved} is a boolean indicating if approval is granted or revoked.
            """
        ),
    ]
    sig_desc = """function setApprovalForAll(address _operator, bool _approved) external;"""
    postconditions = [
        """/// @notice postcondition {_operatorApprovals}[msg.sender][{_operator}] == {_approved}""",
    ]
    sig_spec = """function setApprovalForAll(address _operator, bool _approved) external;"""
    params_vars = {
        "_operator": ["_operator", "operatorAddress", "agent"],
        "_approved": ["_approved", "isApproved", "status"],
    }

class IsApprovedForAll(FunctionTemplate):
    name = "isApprovedForAll"
    descriptions = [
        r"@notice Query if an address is an authorized operator for another address",
        r"Checks if an operator is approved to manage all tokens of an owner.",
        r"Returns whether an operator has approval for all of an owner's NFTs.",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @param {_owner} The address that owns the NFTs
            @param {_operator} The address that acts on behalf of the owner
            @return True if `{_operator}` is an approved operator for `{_owner}`, false otherwise
            """
        ),
        textwrap.dedent(
            """
            {_owner} is the address of the token owner.
            {_operator} is the address of the potential operator.
            Returns true if the operator is approved, false otherwise.
            """
        ),
    ]
    sig_desc = """function isApprovedForAll(address _owner, address _operator) external view returns (bool);"""
    postconditions = [
        """/// @notice postcondition {_operatorApprovals}[{_owner}][{_operator}] == {approved}""",
    ]
    sig_spec = """function isApprovedForAll(address _owner, address _operator) external view returns (bool {approved});"""
    params_vars = {
        "_owner": ["_owner", "tokenOwnerAddress", "principal"],
        "_operator": ["_operator", "operatorAddress", "delegate"],
        "approved": ["approved", "isOperator", "hasApproval"],
    }

class TransferFrom(FunctionTemplate):
    name = "transferFrom"
    descriptions = [
        r"@notice Transfer ownership of an NFT -- THE CALLER IS RESPONSIBLE TO CONFIRM THAT `_to` IS CAPABLE OF RECEIVING NFTS OR ELSE THEY MAY BE PERMANENTLY LOST",
        r"Transfers a specific NFT from one address to another.",
        r"Moves an NFT from a sender to a recipient. Caller must be owner, approved, or operator.",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @param {_from} The current owner of the NFT
            @param {_to} The new owner
            @param {_tokenId} The NFT to transfer
            """
        ),
        textwrap.dedent(
            """
            {_from} is the address of the current owner.
            {_to} is the address of the recipient.
            {_tokenId} is the ID of the token to transfer.
            """
        ),
    ]
    sig_desc = """function transferFrom(address _from, address _to, uint256 _tokenId) external;"""
    postconditions = [
        """/// @notice  postcondition ( ( {_ownedTokensCount}[{_from}] ==  __verifier_old_uint ({_ownedTokensCount}[{_from}] ) - 1  &&  {_from}  != {_to} ) || ( {_from} == {_to} )  )""",
        """/// @notice  postcondition ( ( {_ownedTokensCount}[{_to}] ==  __verifier_old_uint ( {_ownedTokensCount}[{_to}] ) + 1  &&  {_from}  != {_to} ) || ( {_from}  == {_to} ) )""",
        """/// @notice  postcondition  {_tokenOwner}[{_tokenId}] == {_to}""",
    ]
    sig_spec = """function transferFrom(address {_from}, address {_to}, uint256 {_tokenId}) external;"""
    params_vars = {
        "_from": ["_from", "sender", "sourceAddress"],
        "_to": ["_to", "recipient", "destinationAddress"],
        "_tokenId": ["_tokenId", "ID", "nft"],
    }

class SafeTransferFrom(FunctionTemplate):
    name = "safeTransferFrom" # Solidity name
    template_name_suffix_for_generation = "" # Distinguishes from SafeTransferFromWithData for Python class name

    descriptions = [
        r"@notice Transfers the ownership of an NFT from one address to another address",
        r"Safely transfers an NFT. If `_to` is a contract, calls `onERC721Received`.",
        r"Moves an NFT securely, with a check for receiver contract compatibility.",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @param {_from} The current owner of the NFT
            @param {_to} The new owner
            @param {_tokenId} The NFT to transfer
            """
        ),
        textwrap.dedent(
            """
            {_from} address of the current token owner.
            {_to} address of the new token owner.
            {_tokenId} ID of the token being transferred.
            This version sets data to "".
            """
        ),
    ]
    sig_desc = """function safeTransferFrom(address _from, address _to, uint256 _tokenId) external;"""
    postconditions = [
        """/// @notice  postcondition ( ( {_ownedTokensCount}[{_from}] ==  __verifier_old_uint ({_ownedTokensCount}[{_from}] ) - 1  &&  {_from}  != {_to} ) || ( {_from} == {_to} )  )""",
        """/// @notice  postcondition ( ( {_ownedTokensCount}[{_to}] ==  __verifier_old_uint ( {_ownedTokensCount}[{_to}] ) + 1  &&  {_from}  != {_to} ) || ( {_from}  == {_to} ) )""",
        """/// @notice  postcondition  {_tokenOwner}[{_tokenId}] == {_to}""",
    ]
    sig_spec = """function safeTransferFrom(address {_from}, address {_to}, uint256 {_tokenId}) external;"""
    params_vars = {
        "_from": ["_from", "currentOwner", "senderAddress"],
        "_to": ["_to", "newOwner", "receiverAddress"],
        "_tokenId": ["_tokenId", "tokenIdentifier", "assetId"],
    }

class SafeTransferFromWithData(FunctionTemplate):
    name = "safeTransferFrom" # Solidity name
    template_name_suffix_for_generation = "WithData" # Distinguishes from SafeTransferFrom for Python class name

    descriptions = [
        r"@notice Transfers the ownership of an NFT from one address to another address",
        r"Safely transfers an NFT with additional data. If `_to` is a contract, calls `onERC721Received` with the data.",
        r"Securely moves an NFT, passing data to the receiver if it's a contract.",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @param {_from} The current owner of the NFT
            @param {_to} The new owner
            @param {_tokenId} The NFT to transfer
            @param {_data} Additional data with no specified format, sent in call to `{_to}`
            """
        ),
        textwrap.dedent(
            """
            {_from} is the current owner's address.
            {_to} is the recipient's address.
            {_tokenId} is the token's ID.
            {_data} is the additional data to send with the transfer.
            """
        ),
    ]
    sig_desc = """function safeTransferFrom(address _from, address _to, uint256 _tokenId, bytes memory _data) external;"""
    postconditions = [
        """/// @notice  postcondition ( ( {_ownedTokensCount}[{_from}] ==  __verifier_old_uint ({_ownedTokensCount}[{_from}] ) - 1  &&  {_from}  != {_to} ) || ( {_from} == {_to} )  )""",
        """/// @notice  postcondition ( ( {_ownedTokensCount}[{_to}] ==  __verifier_old_uint ( {_ownedTokensCount}[{_to}] ) + 1  &&  {_from}  != {_to} ) || ( {_from}  == {_to} ) )""",
        """/// @notice  postcondition  {_tokenOwner}[{_tokenId}] == {_to}""",
    ]
    sig_spec = """function safeTransferFrom(address {_from}, address {_to}, uint256 {_tokenId}, bytes memory {_data}) external;"""
    params_vars = {
        "_from": ["_from", "ownerOfToken", "source"],
        "_to": ["_to", "receiverOfToken", "destination"],
        "_tokenId": ["_tokenId", "theTokenId", "specificNftId"],
        "_data": ["_data", "payload", "additionalInfo"],
    }

contractERC721 = ContractTemplate(
    """
    Given the state variables:
        mapping(address => uint256) private {_ownedTokensCount};
        mapping(uint256 => address) private {_tokenOwner};
        mapping(uint256 => address) private {_tokenApprovals};
        mapping(address => mapping(address => bool)) private {_operatorApprovals};
    """,
    {
        "_ownedTokensCount": ["_ownedTokensCount", "balances", "numTokensOfOwner"],
        "_tokenOwner": ["_tokenOwner", "ownerOfToken", "tokenIdToOwnerMap"],
        "_tokenApprovals": ["_tokenApprovals", "approvedOperators", "tokenToApprovedAddress"],
        "_operatorApprovals": ["_operatorApprovals", "userOperatorApprovals", "ownerToOperatorApprovalStatus"],
    },
    [
        BalanceOf,
        OwnerOf,
        Approve,
        GetApproved,
        SetApprovalForAll,
        IsApprovedForAll,
        TransferFrom,
        SafeTransferFrom,
        SafeTransferFromWithData,
    ],
)

if __name__ == "__main__":
    all_possible_entries = contractERC721.entries()
    random.seed(42)
    
    if len(all_possible_entries) > 1000:
       sampled_entries = random.sample(all_possible_entries, 1000)
    else:
       sampled_entries = all_possible_entries
       # Optionally, shuffle if the order matters and count is < 1000
       # random.shuffle(sampled_entries) 

    output_file_path = "llm_spec/fine_tuning/erc721/dataset.jsonl"
    with open(output_file_path, 'w') as f:
        for entry in sampled_entries:
            f.write(json.dumps(entry) + '\n')
    
    print(f"Successfully generated {len(sampled_entries)} entries to {output_file_path}") 