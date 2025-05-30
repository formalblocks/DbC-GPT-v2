
import textwrap
import random

from ..template import ContractTemplate, FunctionTemplate

class Transfer(FunctionTemplate):

    name = "transfer"
    descriptions = [
        r"@notice Transfer tokens from the sender's account to another account.",
        r"@notice Moves a specified amount of tokens from the sender's account to the recipient's account.",
        r"Transfers tokens from the sender's address to a specified recipient address.",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @param {_to}     The address of the recipient
            @param {_value}  The amount of tokens to transfer
            @return          Boolean indicating whether the operation was successful
            """
        ),
        textwrap.dedent(
            """
            {_to} is the recipient's address
            {_value} is the amount of tokens to transfer
            It returns true if the transfer was successful
            """
        ),
        textwrap.dedent(
            """
            @return Boolean indicating success of the transfer.
            @param {_to} Address of the recipient.
            @param {_value} Amount of tokens to transfer.
            """
        ),
    ]
    sig_desc = """function transfer(address {_to}, uint256 {_value}) external returns (bool);"""

    postconditions = [
        """/// @notice postcondition ( {_balances}[msg.sender] == __verifier_old_uint({_balances}[msg.sender]) - {_value} && msg.sender != {_to} ) || ({_balances}[msg.sender] == __verifier_old_uint({_balances}[msg.sender]) && msg.sender == {_to})
           /// @notice postcondition ({_balances}[msg.sender] == __verifier_old_uint({_balances}[msg.sender]) && msg.sender == {_to}) || ( {_balances}[msg.sender] == __verifier_old_uint({_balances}[msg.sender]) - {_value} && msg.sender != {_to} )
        """,
        """/// @notice postcondition ( {_balances}[{_to}] == __verifier_old_uint({_balances}[{_to}]) + {_value} && msg.sender != {_to} ) || ({_balances}[{_to}] == __verifier_old_uint({_balances}[{_to}]) && msg.sender == {_to})',
          /// @notice postcondition ( msg.sender != {_to} && {_balances}[{_to}] == __verifier_old_uint({_balances}[{_to}]) + {_value} ) || ( msg.sender == {_to} && {_balances}[{_to}] == __verifier_old_uint({_balances}[{_to}]) )

        """,
    ]
    sig_spec = """function transfer(address {_to}, uint256 {_value}) external returns (bool {success});"""

    params_vars = {
        "_to": ["_to", "to"],
        "_value": ["_value", "value"],
        "success": ["success", "ok"],
    }


class TransferFrom(FunctionTemplate):

    name = "transferFrom"
    descriptions = [
        r"@notice Transfer tokens from one address to another using an allowance mechanism.",
        r"@notice Transfers tokens from one address to another if the sender has sufficient allowance.",
        r"Allows for transferring tokens on behalf of another address with an allowance.",
        r"The `transferFrom` method is used for a withdraw workflow, allowing contracts to transfer tokens on your behalf.",
        r"The `transferFrom` function gives rise to a withdraw workflow, which allows contracts to transfer tokens on your behalf."
    ]
    param_docs = [
        textwrap.dedent(
            """
            @param {_from}    The address of the sender
            @param {_to}      The address of the recipient
            @param {_value}   The amount of tokens to transfer
            @return           Boolean indicating whether the operation was successful
            """
        ),
        textwrap.dedent(
            """
            {_from} is the sender's address
            {_to} is the recipient's address
            {_value} is the amount of tokens to transfer
            It returns true if the transfer was successful
            """
        ),
        textwrap.dedent(
            """
            @return Boolean indicating success of the transfer.
            @param {_from} Address: sender.
            @param {_to} Address: recipient.
            @param {_value} Number of tokens to transfer.
            """
        ),
    ]
    sig_desc = """function transferFrom(address {_from}, address {_to}, uint256 {_value}) external returns (bool);"""

    postconditions = [
        """/// @notice postcondition ( {_balances}[{_from}] == __verifier_old_uint({_balances}[{_from}]) - {_value} && {_from} != {_to} ) || ({_balances}[{_from}] == __verifier_old_uint({_balances}[{_from}]) && {_from} == {_to})
           /// @notice postcondition ({_balances}[{_from}] == __verifier_old_uint({_balances}[{_from}]) && {_from} == {_to}) || ( {_balances}[{_from}] == __verifier_old_uint({_balances}[{_from}]) - {_value} && {_from} != {_to} ) 
           /// @notice postcondition ({_allowances}[{_from}][msg.sender] == __verifier_old_uint({_allowances}[{_from}][msg.sender]) - {_value} && {success}) || ({_allowances}[{_from}][msg.sender] == __verifier_old_uint({_allowances}[{_from}][msg.sender]) && !{success}) || {_from} == msg.sender
            /// @notice postcondition {_allowances}[{_from}][msg.sender] <= __verifier_old_uint({_allowances}[{_from}][msg.sender]) || {_from} == msg.sender
        """,
        """/// @notice postcondition ( {_balances}[{_to}] == __verifier_old_uint({_balances}[{_to}]) + {_value} && {_from} != {_to} ) || ({_balances}[{_to}] == __verifier_old_uint({_balances}[{_to}]) && {_from} == {_to})',
          /// @notice postcondition ( {_from} != {_to} && {_balances}[{_to}] == __verifier_old_uint({_balances}[{_to}]) + {_value} ) || ( {_from} == {_to} && {_balances}[{_to}] == __verifier_old_uint({_balances}[{_to}]) )
          /// @notice postcondition ({_allowances}[{_from}][msg.sender] == __verifier_old_uint({_allowances}[{_from}][msg.sender]) - {_value} && {success}) || ({_allowances}[{_from}][msg.sender] == __verifier_old_uint({_allowances}[{_from}][msg.sender]) && !{success}) || {_from} == msg.sender
        /// @notice postcondition {_allowances}[{_from}][msg.sender] <= __verifier_old_uint({_allowances}[{_from}][msg.sender]) || {_from} == msg.sender

        """,
    ]
    sig_spec = """function transferFrom(address {_from}, address {_to}, uint256 {_value}) external returns (bool {success});"""

    params_vars = {
        "_from": ["_from", "fromAddress"],
        "_to": ["_to", "recipient"],
        "_value": ["_value", "val"],
        "success": ["success", "ok"],
    }


class Approve(FunctionTemplate):

    name = "approve"
    descriptions = [
        r"@notice Approve an address to spend tokens on behalf of the sender.",
        r"@notice Sets an allowance for a specified address to spend tokens on behalf of the sender.",
        r"Approves a specified address to spend a certain amount of tokens.",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @param {_spender} The address to be approved
            @param {_value}   The amount of tokens to approve
            @return           Boolean indicating whether the operation was successful
            """
        ),
        textwrap.dedent(
            """
            {_spender} is the address to be approved
            {_value} is the amount of tokens to approve
            It returns true if the approval was successful
            """
        ),
        textwrap.dedent(
            """
            @return Boolean indicating success of the approval.
            @param {_spender} Address to be approved.
            @param {_value} Amount of tokens to approve.
            """
        ),
    ]
    sig_desc = """function approve(address {_spender}, uint256 {_value}) external returns (bool);"""

    postconditions = [
        """({_allowances}[msg.sender][{_spender}] == {_value} && {success}) || ({_allowances}[msg.sender][{_spender}] == __verifier_old_uint({_allowances}[msg.sender][{_spender}]) && !{success})""",
    ]
    sig_spec = """function approve(address {_spender}, uint256 {_value}) external returns (bool {success});"""

    params_vars = {
        "_spender": ["_spender", "spender"],
        "_value": ["_value", "value"],
        "success": ["success", "ok"],
    }


class Allowance(FunctionTemplate):

    name = "allowance"
    descriptions = [
        r"@notice Get the amount of tokens approved for spending by a specified address.",
        r"@notice Returns the amount of tokens that an owner allowed to a spender.",
        r"Retrieves the allowance of a specified address to spend tokens on behalf of another address.",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @param {_owner}   The address of the token owner
            @param {_spender} The address of the spender
            @return           The amount of tokens approved
            """
        ),
        textwrap.dedent(
            """
            {_owner} is the token owner's address
            {_spender} is the spender's address
            It returns the amount of tokens approved
            """
        ),
        textwrap.dedent(
            """
            @return The amount of tokens approved.
            @param {_owner} Address of the token owner.
            @param {_spender} Address of the spender.
            """
        ),
    ]
    sig_desc = """function allowance(address {_owner}, address {_spender}) external view returns (uint256);"""

    postconditions = [
        """/// @notice postcondition {_allowances}[{_owner}][{_spender}] == {allowance}""",
    ]
    sig_spec = """function allowance(address {_owner}, address {_spender}) external view returns (uint256 {allowance});"""

    params_vars = {
        "_owner": ["_owner", "owner"],
        "_spender": ["_spender", "spender"],
        "allowance": ["allowance", "remaining"],
    }


class TotalSupply(FunctionTemplate):

    name = "totalSupply"
    descriptions = [
        r"@notice Get the total supply of tokens.",
        r"@notice Returns the total amount of tokens in existence.",
        r"Retrieves the total supply of tokens.",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @return The total supply of tokens
            """
        ),
        textwrap.dedent(
            """
            It returns the total supply of tokens
            """
        ),
        textwrap.dedent(
            """
            @return The total supply of tokens.
            """
        ),
    ]
    sig_desc = """function totalSupply() external view returns (uint256);"""

    postconditions = [
        """/// @notice postcondition {_totalSupply} == {totalSupply}""",
    ]
    sig_spec = """function totalSupply() external view returns (uint256 {totalSupply});"""

    params_vars = {
        "totalSupply": ["totalSupply", "supply"],
    }

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
            @param {_owner} The address of the token holder
            @return         The balance of the tokens owned by the account
            """
        ),
        textwrap.dedent(
            """
            {_owner} is the account that owns the tokens
            It returns the balance of tokens owned by the account
            """
        ),
        textwrap.dedent(
            """
            @return The balance of tokens owned by the specified account.
            @param {_owner} Address of the token holder.
            """
        ),
    ]
    sig_desc = """function balanceOf(address {_owner}) external view returns (uint256);"""

    postconditions = [
        """/// @notice postcondition {_balances}[{_owner}] == {balance}""",
        """/// @notice postcondition {balance} == {_balances}[{_owner}]""",
    ]
    sig_spec = """function balanceOf(address {_owner}) external view returns (uint256 {balance});"""

    params_vars = {
        "_owner": ["_owner", "owner"],
        "balance": ["balance", "bal"],
    }

class IncreaseAllowance(FunctionTemplate):

    name = "increaseAllowance"
    descriptions = [
        r"@notice Increase the amount of tokens that a spender is allowed to spend on behalf of the owner.",
        r"@notice Increases the allowance of a specified address to spend tokens on behalf of the owner.",
        r"Allows increasing the allowance for a spender to transfer tokens from the owner's account.",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @param {_spender} The address of the spender
            @param {_addedValue} The additional amount of tokens to allow
            @return            Boolean indicating whether the operation was successful
            """
        ),
        textwrap.dedent(
            """
            {_spender} is the address of the spender
            {_addedValue} is the additional amount of tokens to allow
            It returns true if the increase was successful
            """
        ),
        textwrap.dedent(
            """
            @return Boolean indicating success of the increase.
            @param {_spender} Address of the spender.
            @param {_addedValue} Additional amount of tokens to allow.
            """
        ),
    ]
    sig_desc = """function increaseAllowance(address {_spender}, uint256 {_addedValue}) external returns (bool);"""

    postconditions = [
        """/// @notice postcondition {_allowances}[msg.sender][{_spender}] == __verifier_old_uint({_allowances}[msg.sender][{_spender}]) + {_addedValue}""",
    ]
    sig_spec = """function increaseAllowance(address {_spender}, uint256 {_addedValue}) external returns (bool {success});"""

    params_vars = {
        "_spender": ["_spender", "spender"],
        "_addedValue": ["_addedValue", "plus"],
        "success": ["success", "ok"],
    }

class DecreaseAllowance(FunctionTemplate):

    name = "decreaseAllowance"
    descriptions = [
        r"@notice Decrease the amount of tokens that a spender is allowed to spend on behalf of the owner.",
        r"@notice Decreases the allowance of a specified address to spend tokens on behalf of the owner.",
        r"Allows decreasing the allowance for a spender to transfer tokens from the owner's account.",
    ]
    param_docs = [
        textwrap.dedent(
            """
            @param {_spender}    The address of the spender
            @param {_subtractedValue} The amount of tokens to subtract from the allowance
            @return               Boolean indicating whether the operation was successful
            """
        ),
        textwrap.dedent(
            """
            {_spender} is the address of the spender
            {_subtractedValue} is the amount of tokens to subtract from the allowance
            It returns true if the decrease was successful
            """
        ),
        textwrap.dedent(
            """
            @return Boolean indicating success of the decrease.
            @param {_spender} Address of the spender.
            @param {_subtractedValue} Amount of tokens to subtract from the allowance.
            """
        ),
    ]
    sig_desc = """function decreaseAllowance(address {_spender}, uint256 {_subtractedValue}) external returns (bool);"""

    postconditions = [
        """/// @notice postcondition {_allowances}[msg.sender][{_spender}] == __verifier_old_uint({_allowances}[msg.sender][{_spender}]) - {_subtractedValue}""",
    ]
    sig_spec = """function decreaseAllowance(address {_spender}, uint256 {_subtractedValue}) external returns (bool {success});"""

    params_vars = {
        "_spender": ["_spender", "spender"],
        "_subtractedValue": ["_subtractedValue", "sub"],
        "success": ["success", "ok"],
    }


contractERC20 = ContractTemplate(
    """
    Given the state variables:
        mapping (address => uint256) private {_balances};
        mapping (address => mapping (address => uint256)) private {_allowances};
        uint256 private {_totalSupply};
    """,
    {
        "_balances": ["_balances", "balances"],
        "_allowances": ["_allowances", "allowed"],
        "_totalSupply": ["_totalSupply", "total"],
    },
    [
        Approve,
        Allowance,
        TotalSupply,
        Transfer,
        TransferFrom,
        IncreaseAllowance,
        DecreaseAllowance,
        BalanceOf
    ],
)

entries = contractERC20.entries()
import json
random.seed(42)
entries = random.sample(entries, 1000)

output_file_path = "llm_spec/fine_tuning/erc20/dataset.jsonl"
with open(output_file_path, 'w') as f:
    for entry in entries:
        f.write(json.dumps(entry) + '\n')
print(f"Wrote {len(entries)} records to {output_file_path}")
