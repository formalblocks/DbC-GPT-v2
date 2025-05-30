
import itertools
import textwrap

class ContractTemplate:

    system_msg = {
        "role": "system",
        "content": "You are a coding assistant specialized in generating formal postconditions for ERC interface with solc-verify postconditions annotations.",
    }

    def __init__(self, state_vars_msg, state_vars, function_templates):
        """
        state_vars_msg: string container the declaration of state variables, e.g.
        ------------------------------------------------------------------------------------
            Given state variables:
                mapping (uint256 => mapping(address => uint256)) private {_balances};
                mapping (address => mapping(address => bool)) private {_operatorApprovals};
        ------------------------------------------------------------------------------------

        state_vars: dict of state variable names and its variations, e.g.
            {
                "_balances": ["_balances", "balances"],
                "_operatorApprovals": ["_operatorApprovals", "approvals"],
                ...
            }
        function_templates: list of FunctionTemplate subclasses
        """
        self.state_vars_msg = state_vars_msg
        self.state_vars = state_vars
        self.function_templates = [fn(self) for fn in function_templates]

    def entries(self):
        entries = []
        for template in self.function_templates:
            entries.extend(template.entries())
        return entries


class FunctionTemplate:

    name: str
    sig_desc: str
    sig_spec: str
    descriptions: list[str]
    param_docs: list[str]
    postconditions: list[str]
    params_vars: dict[str, list[str]]

    def __init__(self, contract: ContractTemplate) -> None:
        self.contract = contract

    def user_msg(self, chosen_desc, chosen_param_docs):
        return textwrap.dedent(
            f"""
            {self.contract.state_vars_msg}
            Generate a solc-verify specification for the function `{self.name}` documented as follows:
            /**
            {chosen_desc}
            {chosen_param_docs}
            **/
            {self.sig_desc}
        """
        )

    def assistant_msg(self, post):
        return "{post}\n{spec}".format(post=post, spec=self.sig_spec)

    @property
    def var_combinations(self):
        vars = self.params_vars | self.contract.state_vars
        keys = list(vars.keys())
        values = [vars[k] for k in keys]
        combos = list(itertools.product(*values))
        return [dict(zip(keys, combo)) for combo in combos]

    def entries(self):
        results = []
        for chosen_description, chosen_post, chosen_param_doc in itertools.product(
            self.descriptions, self.postconditions, self.param_docs
        ):
            for comb_kwargs in self.var_combinations:
                user_msg = self.user_msg(chosen_description, chosen_param_doc).format(
                    **comb_kwargs
                )
                assistant_msg = self.assistant_msg(chosen_post).format(**comb_kwargs)
                entry = {
                    "messages": [
                        self.contract.system_msg,
                        {"role": "user", "content": user_msg},
                        {"role": "assistant", "content": assistant_msg},
                    ]
                }
                results.append(entry)
        return results