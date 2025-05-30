import textwrap
import random

from ..template import ContractTemplate, FunctionTemplate

class BalanceOf(FunctionTemplate):

    name = "balanceOf"
    descriptions = [
        r"@notice Get the balance of an account's tokens.",
        r"@notice Returns the number of tokens owned by a given account.",
        r"Retrieves the token balance of a specific account.",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @param {_owner}  The address of the token holder
            @param {_id}     ID of the token
            @return        The {_owner}'s balance of the token type requested
            """
        ),
        textwrap.dedent(
            """
            {_owner} is the account that owns the tokens
            {_id} is the token's ID
            It returns the {_owner}'s amount of the specified token held
            """
        ),
        textwrap.dedent(
            """
            @return The balance of the specified token ID owned by `{_owner}`.
            @param {_owner} Address of the token holder.
            @param {_id} ID of the token type.
            """
        ),
    ]
    sig_desc = """function balanceOf(address {_owner}, uint256 {_id}) external view returns (uint256);"""

    postconditions = [
        """/// @notice postcondition {_balances}[{_id}][{_owner}] == {balance}""",
        """/// @notice postcondition {balance} == {_balances}[{_id}][{_owner}]""",
    ]
    sig_spec = """function balanceOf(address {_owner}, uint256 {_id}) external view returns (uint256 {balance});"""

    params_vars = {
        "_owner": ["_owner", "owner"],
        "_id": ["_id", "id"],
        "balance": ["balance", "bal"],
    }


class BalanceOfBatch(FunctionTemplate):

    name = "balanceOfBatch"
    descriptions = [
        r"@notice Get the balance of multiple account/token pairs",
        r"Retrieve balances for several combinations of accounts and tokens.",
        r"Fetch the balances corresponding to multiple account and token pairs",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @param {_owners} The addresses of the token holders
            @param {_ids}    ID of the tokens
            @return        The {_owners}'s balance of the token types requested (i.e. balance for each (owner, id) pair)
            """
        ),
        textwrap.dedent(
            """
            {_owners} The list of addresses whose token balances are being queried
            {_ids}    The list of token IDs for which balances are requested
            It returns the balances associated with each address and token ID combination
            """
        ),
        textwrap.dedent(
            """
            @param {_ids} Token identifiers to look up for each corresponding owner.
            @return Balances representing the number of tokens held by each provided address for the given token IDs.
            @param {_owners} Addresses whose token holdings will be retrieved.
            """
        ),
    ]
    sig_desc = """function balanceOfBatch(address[] memory {_owners}, uint256[] memory {_ids}) external view returns (uint256[] memory);"""

    postconditions = [
        textwrap.dedent(
            """/// @notice postcondition {batchBalances}.length == {_owners}.length
            /// @notice postcondition {batchBalances}.length == {_ids}.length
            /// @notice postcondition forall (uint x) !(0 <= x && x < {batchBalances}.length) || {batchBalances}[x] == {_balances}[{_ids}[x]][{_owners}[x]]
            """
        ),
        textwrap.dedent(
            """/// @notice postcondition {_owners}.length == {batchBalances}.length
            /// @notice postcondition  {_ids}.length == {batchBalances}.length
            /// @notice postcondition forall (uint y) !(0 <= y && y < {batchBalances}.length) || {batchBalances}[y] == {_balances}[{_ids}[y]][{_owners}[y]]
            """
        ),
        textwrap.dedent(
            """/// @notice postcondition {_owners}.length == {batchBalances}.length
            /// @notice postcondition forall (uint y) !(0 <= y && y < {batchBalances}.length) || {batchBalances}[y] == {_balances}[{_ids}[y]][{_owners}[y]]
            /// @notice postcondition  {_ids}.length == {batchBalances}.length
            """
        ),
        textwrap.dedent(
            """/// @notice postcondition forall (uint y)  {batchBalances}[y] == {_balances}[{_ids}[y]][{_owners}[y]] || !(0 <= y && y < {batchBalances}.length)
            /// @notice postcondition {_owners}.length == {batchBalances}.length
            /// @notice postcondition  {batchBalances}.length == {_ids}.length
            """
        ),
    ]
    sig_spec = """function balanceOfBatch(address[] memory {_owners}, uint256[] memory {_ids}) external view returns (uint256[] memory {batchBalances});"""
    params_vars = {
        "_owners": ["_owners", "_holders"],
        "_ids": ["_ids", "token_Ids"],
        "batchBalances": ["batchBalances", "bat_bals"],
    }


class SetApprovalForAll(FunctionTemplate):
    name: str = "setApprovalForAll"
    descriptions = [
        """@notice Enable or disable approval for a third party ("operator") to manage all of the caller's tokens.""",
        """Grant or revoke permission for an operator to handle all tokens owned by the caller""",
        """Authorize or deauthorize a third-party operator to manage the caller's entire token holdings.""",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @dev MUST emit the ApprovalForAll event on success.
            @param {_operator}  Address to add to the set of authorized operators
            @param {_approved}  True if the operator is approved, false to revoke approval
            """
        ),
        textwrap.dedent(
            """
            @param {_operator}  The address designated as the operator to manage the caller's tokens
            {_approved}  A boolean indicating whether to approve (true) or revoke (false) the operator's permissions
            """
        ),
        textwrap.dedent(
            """
            {_approved} Boolean flag: true to authorize {_operator}, false to revoke authorization.
            {_operator} The address being granted or revoked permission to act on behalf of the caller.
            """
        ),
    ]
    sig_desc = """function setApprovalForAll(address {_operator}, bool {_approved}) external;"""

    postconditions = [
        """/// @notice postcondition {_operatorApprovals}[msg.sender][{_operator}] == {_approved}""",
        """/// @notice postcondition {_approved} == {_operatorApprovals}[msg.sender][{_operator}]""",
    ]

    sig_spec = sig_desc

    params_vars = {
        "_operator": ["_operator", "proxy"],
        "_approved": ["_approved", "authorized"],
    }


class SafeTransferFrom(FunctionTemplate):
    name: str = "safeTransferFrom"
    descriptions = [
        """@notice Transfers `{_value}` amount of an `{_id}` from the `{_from}` address to the `{_to}` address specified (with safety call).""",
        """Transfer a specific amount of a token from one address to another, performing safety checks and invoking hooks if necessary.""",
        """Securely move tokens of a given ID and amount from a source address to a destination address, ensuring contract compliance.""",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @dev Caller must be approved to manage the tokens being transferred out of the `{_from}` account.
            MUST revert if `{_to}` is the zero address.
            MUST revert if balance of holder for token `{_id}` is lower than the `{_value}` sent.
            MUST emit the TransferSingle event.
            If `{_to}` is a contract, it MUST call `onERC1155Received` on `{_to}`.
            @param {_from}   Source address
            @param {_to}     Target address
            @param {_id}     ID of the token type
            @param {_value}  Transfer amount
            @param {_data}   Additional data, must be passed unchanged to `onERC1155Received`
            """
        ),
        textwrap.dedent(
            """
            @dev The caller must be authorized to operate on behalf of {_from}.
            Reverts if {_to} is the zero address.
            Reverts if {_from} lacks sufficient balance of token {_id} for the transfer amount {_value}.
            A TransferSingle event must be emitted.
            If {_to} is a smart contract, it must implement `onERC1155Received` and be successfully called.
            @param {_from}   Address from which the tokens will be transferred
            @param {_to}     Recipient address
            @param {_id}     Token ID to transfer
            @param {_value}  Amount of tokens to transfer
            @param {_data}   Arbitrary data forwarded in the recipient's hook call
            """
        ),
        textwrap.dedent(
            """
            The caller must have delegated rights to move tokens on behalf of {_from}.
            {_to} is the recipient address.
            Transaction fails if {_to} is the zero address.
            {_from} is the account sending the tokens.
            Transaction fails if {_from} does not have enough of token {_id} to cover {_value}.
            {_data} is arbitrary data to pass along, forwarded as-is to {_to} if it is a contract.
            If {_to} is a contract, it must respond correctly to `onERC1155Received`.
            {_value} is the number of tokens to send.
            {_id} is the specific token type to be transferred.
            """
        ),
    ]

    sig_desc = (
        "function safeTransferFrom(address {_from}, address {_to}, uint256 {_id}, "
        "uint256 {_value}, bytes memory {_data}) external;"
    )

    postconditions = [
       textwrap.dedent(
            """/// @notice postcondition {_to} != address(0)
            /// @notice postcondition {_operatorApprovals}[{_from}][msg.sender] || {_from} == msg.sender
            /// @notice postcondition __verifier_old_uint({_balances}[{_id}][{_from}]) >= {_value}    
            /// @notice postcondition {_from} == {_to} || {_balances}[{_id}][{_from}] == __verifier_old_uint({_balances}[{_id}][{_from}]) - {_value}
            /// @notice postcondition {_from} != {_to} || {_balances}[{_id}][{_from}] == __verifier_old_uint({_balances}[{_id}][{_from}])
            /// @notice postcondition {_from} == {_to} || {_balances}[{_id}][{_to}] == __verifier_old_uint({_balances}[{_id}][{_to}]) + {_value}
            /// @notice postcondition {_from} != {_to} || {_balances}[{_id}][{_to}] == __verifier_old_uint({_balances}[{_id}][{_to}])
            """
        ),
        textwrap.dedent(
            """/// @notice postcondition address(0) != {_to}
            /// @notice postcondition {_value} <= __verifier_old_uint({_balances}[{_id}][{_from}])
            /// @notice postcondition {_from} == msg.sender || {_operatorApprovals}[{_from}][msg.sender]
            /// @notice postcondition {_from} == {_to} || __verifier_old_uint({_balances}[{_id}][{_from}]) - {_value} == {_balances}[{_id}][{_from}]
            /// @notice postcondition {_balances}[{_id}][{_to}] == __verifier_old_uint({_balances}[{_id}][{_to}]) + {_value} || {_from} == {_to}
            /// @notice postcondition {_from} != {_to} || {_balances}[{_id}][{_from}] == __verifier_old_uint({_balances}[{_id}][{_from}])
            /// @notice postcondition __verifier_old_uint({_balances}[{_id}][{_to}]) == {_balances}[{_id}][{_to}] || {_from} != {_to}
            """
        ),
        textwrap.dedent(
            """/// @notice postcondition {_from} != {_to} || {_balances}[{_id}][{_from}] == __verifier_old_uint({_balances}[{_id}][{_from}])
            /// @notice postcondition {_to} != address(0)
            /// @notice postcondition  {_operatorApprovals}[{_from}][msg.sender] || {_from} == msg.sender
            /// @notice postcondition {_value} <= __verifier_old_uint({_balances}[{_id}][{_from}])
            /// @notice postcondition {_from} == {_to} || __verifier_old_uint({_balances}[{_id}][{_from}]) - {_value} == {_balances}[{_id}][{_from}]
            /// @notice postcondition {_balances}[{_id}][{_to}] == __verifier_old_uint({_balances}[{_id}][{_to}]) + {_value} || {_from} == {_to}
            /// @notice postcondition __verifier_old_uint({_balances}[{_id}][{_to}]) == {_balances}[{_id}][{_to}] || {_from} != {_to}
            """
        ),
        textwrap.dedent(
            """/// @notice postcondition __verifier_old_uint({_balances}[{_id}][{_to}]) == {_balances}[{_id}][{_to}] || {_from} != {_to}
            /// @notice postcondition {_balances}[{_id}][{_to}] == __verifier_old_uint({_balances}[{_id}][{_to}]) + {_value} ||  {_to} == {_from}
            /// @notice postcondition  {_operatorApprovals}[{_from}][msg.sender] || msg.sender == {_from}
            /// @notice postcondition {_value} <= __verifier_old_uint({_balances}[{_id}][{_from}])
            /// @notice postcondition {_to} == {_from} || __verifier_old_uint({_balances}[{_id}][{_from}]) - {_value} == {_balances}[{_id}][{_from}]
            /// @notice postcondition {_to} != {_from} || {_balances}[{_id}][{_from}] == __verifier_old_uint({_balances}[{_id}][{_from}])
            /// @notice postcondition {_to} != address(0)
            """
        )
    ]
    sig_spec = sig_desc

    params_vars = {
        "_from": ["_from", "sender"],
        "_to": ["_to", "recipient"],
        "_id": ["_id", "tokenId"],
        "_value": ["_value", "amount"],
        "_data": ["_data", "metadata"],
    }


class IsApprovedForAll(FunctionTemplate):
    name: str = "isApprovedForAll"
    descriptions = [
        """@notice Queries the approval status of an operator for a given owner.""",
        """Check whether an operator is authorized to manage all of an owner's tokens.""",
        """Returns true if the operator is approved to transfer the owner's tokens, false otherwise.""",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @param {_owner}     The owner of the tokens
            @param {_operator}  Address of authorized operator
            @return             True if the operator is approved, false if not
            """
        ),
        textwrap.dedent(
            """
            @param {_owner}     Address whose operator approval is being queried
            @param {_operator}  Address of the operator being checked
            @return             Boolean indicating whether the operator is approved
            """
        ),
        textwrap.dedent(
            """
            {_owner} The address holding the tokens.
            Returns true if the operator is authorized, false otherwise.
            {_operator} The address of the operator granted approval.
            """
        ),
    ]

    sig_desc = (
        "function isApprovedForAll(address {_owner}, address {_operator}) "
        "external view returns (bool {approved});"
    )

    postconditions = [
        "/// @notice postcondition {_operatorApprovals}[{_owner}][{_operator}] == {approved}",
        "/// @notice postcondition {approved} == {_operatorApprovals}[{_owner}][{_operator}]",
    ]

    sig_spec = sig_desc

    params_vars = {
        "_owner": ["_owner", "proxy"],
        "_operator": ["_operator", "operator"],
        "approved": ["approved", "allowed"],
    }


class SafeBatchTransferFrom(FunctionTemplate):
    name: str = "safeBatchTransferFrom"
    descriptions = [
        """@notice Transfers `{_values}` amount(s) of `{_ids}` from the `{_from}` address to the `{_to}` address specified (with safety call).""",
        """Batch transfer multiple token types and amounts from one address to another, with required safety checks.""",
        """Execute multiple token transfers from a single source to a target address, ensuring safe receipt and validity.""",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @dev Caller must be approved to manage the tokens being transferred out of the `{_from}` account.
            MUST revert if `{_to}` is the zero address.
            MUST revert if length of `{_ids}` != length of `{_values}`.
            MUST revert if any token balance is insufficient.
            MUST emit `TransferBatch` or `TransferSingle` event(s).
            If `{_to}` is a contract, MUST call the ERC1155TokenReceiver hook(s) on `{_to}`.
            @param {_from}    Source address
            @param {_to}      Target address
            @param {_ids}     Array of token type IDs
            @param {_values}  Array of token amounts to transfer
            @param {_data}    Additional data to forward to the receiver hook(s)
            """
        ),
        textwrap.dedent(
            """
            The caller must be authorized to manage tokens from the `{_from}` account.
            The `{_to}` address cannot be the zero address.
            The `{_ids}` and `{_values}` arrays must have the same length.
            The `{_from}` account must have sufficient balance for each token ID.
            @param {_from}    Address to transfer tokens from
            @param {_to}      Address to transfer tokens to
            @param {_ids}     List of token IDs to transfer
            @param {_values}  Corresponding list of amounts for each token ID
            @param {_data}    Arbitrary data forwarded to receiver contracts
            """
        ),
        textwrap.dedent(
            """
            The caller must have permission to transfer tokens on behalf of the source address.
            Reverts if the recipient is the zero address.
            Reverts if the lengths of ids and values do not match.
            Reverts if any token balance is insufficient for the transfer.
            A `TransferBatch` or `TransferSingle` event(s) must be emitted.
            If the recipient is a contract, it must call the appropriate ERC1155 receiver hook(s) on the recipient address.
            @param {_from} The source address sending the tokens.
            @param {_to} The recipient address.
            @param {_ids} List of token type IDs to transfer.
            @param {_values} List of amounts for each token type to be transferred.
            @param {_data} Some data to forward to the recipient's hook(s).
            """
        ),
    ]

    sig_desc = (
        "function safeBatchTransferFrom(address {_from}, address {_to}, "
        "uint256[] memory {_ids}, uint256[] memory {_values}, bytes memory {_data}) external;"
    )

    postconditions = [
        textwrap.dedent(
            """/// @notice postcondition {_to} != address(0)
            /// @notice postcondition {_operatorApprovals}[{_from}][msg.sender] || {_from} == msg.sender
            /// @notice postcondition {_ids}.length == {_values}.length
            /// @notice postcondition forall (uint x) !(0 <= x && x < {_ids}.length) || (__verifier_old_uint({_balances}[{_ids}[x]][{_from}]) >= {_values}[x])
            /// @notice postcondition forall (uint x) !(0 <= x && x < {_ids}.length) || ({_from} == {_to}) || ({_balances}[{_ids}[x]][{_to}] == __verifier_old_uint({_balances}[{_ids}[x]][{_to}]) + {_values}[x])
            /// @notice postcondition forall (uint x) {_from} != {_to} || {_balances}[{_ids}[x]][{_to}] == __verifier_old_uint({_balances}[{_ids}[x]][{_to}])
            /// @notice postcondition forall (uint x) !(0 <= x && x < {_ids}.length) || ({_from} == {_to}) || ( {_balances}[{_ids}[x]][{_from}] == __verifier_old_uint({_balances}[{_ids}[x]][{_from}]) - {_values}[x])
            /// @notice postcondition forall (uint x) {_from} != {_to} || {_balances}[{_ids}[x]][{_from}] == __verifier_old_uint({_balances}[{_ids}[x]][{_from}])
            """
        ),
        textwrap.dedent(
            """/// @notice postcondition address(0) != {_to}
            /// @notice postcondition msg.sender == {_from} || {_operatorApprovals}[{_from}][msg.sender]
            /// @notice postcondition {_values}.length == {_ids}.length
            /// @notice postcondition forall (uint a) (__verifier_old_uint({_balances}[{_ids}[a]][{_from}]) >= {_values}[a]) || !(0 <= a && a < {_ids}.length)
            /// @notice postcondition forall (uint d) ({_from} == {_to}) || ({_balances}[{_ids}[d]][{_to}] == __verifier_old_uint({_balances}[{_ids}[d]][{_to}]) + {_values}[d]) || !(0 <= d && d < {_ids}.length)
            /// @notice postcondition forall (uint c) !(0 <= c && c < {_ids}.length) || ({_from} == {_to}) || ( {_balances}[{_ids}[c]][{_from}] == __verifier_old_uint({_balances}[{_ids}[c]][{_from}]) - {_values}[c])
            /// @notice postcondition forall (uint h) {_balances}[{_ids}[h]][{_to}] == __verifier_old_uint({_balances}[{_ids}[h]][{_to}]) || {_from} != {_to}
            /// @notice postcondition forall (uint x) {_from} != {_to} || {_balances}[{_ids}[x]][{_from}] == __verifier_old_uint({_balances}[{_ids}[x]][{_from}])
            """
        ),
        textwrap.dedent(
            """/// @notice postcondition msg.sender == {_from} || {_operatorApprovals}[{_from}][msg.sender]
            /// @notice postcondition address(0) != {_to}
            /// @notice postcondition forall (uint a) (__verifier_old_uint({_balances}[{_ids}[a]][{_from}]) >= {_values}[a]) || !(0 <= a && a < {_ids}.length)
            /// @notice postcondition {_values}.length == {_ids}.length
            /// @notice postcondition forall (uint x) {_to} != {_from} || {_balances}[{_ids}[x]][{_from}] == __verifier_old_uint({_balances}[{_ids}[x]][{_from}])
            /// @notice postcondition forall (uint c) !(0 <= c && c < {_ids}.length) || ({_from} == {_to}) || ( {_balances}[{_ids}[c]][{_from}] == __verifier_old_uint({_balances}[{_ids}[c]][{_from}]) - {_values}[c])
            /// @notice postcondition forall (uint h) __verifier_old_uint({_balances}[{_ids}[h]][{_to}]) == {_balances}[{_ids}[h]][{_to}] || {_from} != {_to}
            /// @notice postcondition forall (uint d) ({_from} == {_to}) || (__verifier_old_uint({_balances}[{_ids}[d]][{_to}]) + {_values}[d] == {_balances}[{_ids}[d]][{_to}]) || !(d < {_ids}.length && 0 <= d)
            """
        ),
        textwrap.dedent(
            """/// @notice postcondition msg.sender == {_from} || {_operatorApprovals}[{_from}][msg.sender]
            /// @notice postcondition forall (uint x) {_to} != {_from} || {_balances}[{_ids}[x]][{_from}] == __verifier_old_uint({_balances}[{_ids}[x]][{_from}])
            /// @notice postcondition forall (uint h) __verifier_old_uint({_balances}[{_ids}[h]][{_to}]) == {_balances}[{_ids}[h]][{_to}] || {_from} != {_to}
            /// @notice postcondition forall (uint a) (__verifier_old_uint({_balances}[{_ids}[a]][{_from}]) >= {_values}[a]) || !(0 <= a && a < {_ids}.length)
            /// @notice postcondition forall (uint d) ({_from} == {_to}) || (__verifier_old_uint({_balances}[{_ids}[d]][{_to}]) + {_values}[d] == {_balances}[{_ids}[d]][{_to}]) || !(d < {_ids}.length && 0 <= d)
            /// @notice postcondition {_values}.length == {_ids}.length
            /// @notice postcondition forall (uint c) !(0 <= c && c < {_ids}.length) || ({_from} == {_to}) || ( {_balances}[{_ids}[c]][{_from}] == __verifier_old_uint({_balances}[{_ids}[c]][{_from}]) - {_values}[c])
            /// @notice postcondition address(0) != {_to}
            """
        ),
        textwrap.dedent(
            """/// @notice postcondition msg.sender == {_from} || {_operatorApprovals}[{_from}][msg.sender]
            /// @notice postcondition forall (uint x) {_from} != {_to} || {_balances}[{_ids}[x]][{_from}] == __verifier_old_uint({_balances}[{_ids}[x]][{_from}])
            /// @notice postcondition forall (uint h) __verifier_old_uint({_balances}[{_ids}[h]][{_to}]) == {_balances}[{_ids}[h]][{_to}] || {_to} != {_from}
            /// @notice postcondition forall (uint a) ({_values}[a] <= __verifier_old_uint({_balances}[{_ids}[a]][{_from}])) || !(0 <= a && a < {_ids}.length)
            /// @notice postcondition forall (uint d) ({_from} == {_to}) || (__verifier_old_uint({_balances}[{_ids}[d]][{_to}]) + {_values}[d] == {_balances}[{_ids}[d]][{_to}]) || !(d < {_ids}.length && 0 <= d)
            /// @notice postcondition {_ids}.length == {_values}.length
            /// @notice postcondition forall (uint c) ( {_balances}[{_ids}[c]][{_from}] == __verifier_old_uint({_balances}[{_ids}[c]][{_from}]) - {_values}[c]) || ({_from} == {_to})  || !(0 <= c && c < {_ids}.length)
            /// @notice postcondition address(0) != {_to}
            """
        )

    ]

    sig_spec = sig_desc

    params_vars = {
        "_from": ["_from", "sender"],
        "_to": ["_to", "recipient"],
        "_ids": ["_ids", "tokenIds"],
        "_values": ["_values", "amounts"],
        "_data": ["_data","metadata"],
    }


# ---------------------------------------------------------------------------------------------------------------- #


contractERC1155 = ContractTemplate(
    """
    Given state variables:
        mapping (uint256 => mapping(address => uint256)) private {_balances};
        mapping (address => mapping(address => bool)) private {_operatorApprovals};
    """,
    {
        "_balances": ["_balances", "balances"],
        "_operatorApprovals": ["_operatorApprovals", "operatorApprovals"],
    },
    [
        BalanceOf,
        BalanceOfBatch,
        SetApprovalForAll,
        SafeTransferFrom,
        IsApprovedForAll,
        SafeBatchTransferFrom,
    ],
)

entries = contractERC1155.entries()
import json
random.seed(42)
entries = random.sample(entries, 1000)

output_path = "llm_spec/fine_tuning/erc1155/dataset.jsonl"
with open(output_path, "w") as f:
    for entry in entries:
        f.write(json.dumps(entry) + "\n")
print(f"Wrote {len(entries)} records to {output_path}")