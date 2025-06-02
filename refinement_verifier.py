import logging
import sys
import pandas as pd
from dataclasses import dataclass
from typing import List
import os
import re

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Initialize the global verification status
# verification_status = [] # This was unused, can be removed or kept if intended for future use.

# --- Configuration Constants ---
VERIFICATION_OPTIONS = ['llm_base', 'base_llm']
TARGET_ERC_STANDARD_DIR = "erc1155"  # This script is tailored for ERC1155 verification

RESULT_TYPES = [
    'results_entire_contract_base_full_context',
    'results_entire_contract_fine_tuning',
    'results_func_by_func_base_full_context',
    'results_func_by_func_fine_tuning'
]

MODELS_FOR_FINETUNING = [
    '4o-mini', 
    'erc-20-001-5-16', 
    'erc-721-001-5-16', 
    'erc-1155-001-5-16', 
    'erc-20-721-001-5-16', 
    'erc-20-1155-001-5-16', 
    'erc-721-1155-001-5-16', 
    'erc-20-721-1155-001-5-16'
]
MODEL_FOR_BASE = '4o-mini'

TOKEN_CONTEXTS = [
    'none', 'erc20', 'erc721', 'erc1155', 
    'erc20_erc721', 'erc20_erc1155', 'erc721_erc1155', 
    'erc20_erc721_erc1155'
]
OUTPUT_BASE_DIR = './refinement_check_results'
# --- End Configuration Constants ---

@dataclass
class VerificationResult:
    status: int
    output: str

class SolcVerifyWrapper:

    SOLC_VERIFY_CMD = "solc-verify.py"
    SPEC_FILE_PATH = './temp/spec.sol'

    ERC1155_TEMPLATE_PATH_BASE_LLM = './solc_verify_generator/ERC1155/templates/spec_refinement_base_llm.template'
    ERC1155_TEMPLATE_PATH_LLM_BASE = './solc_verify_generator/ERC1155/templates/spec_refinement_llm_base.template'
    # ERC1155_TEMPLATE_PATH = './solc_verify_generator/ERC1155/templates/spec_refinement_trivial.template'

    ERC1155_MERGE_PATH = './solc_verify_generator/ERC1155/imp/ERC1155_merge.sol'

    @classmethod
    def call_solc(cls, file_path) -> VerificationResult:
        from subprocess import PIPE, run
        command = [cls.SOLC_VERIFY_CMD, file_path]
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        return VerificationResult(result.returncode, result.stdout + result.stderr)
    
    @classmethod
    def verify(cls, solidity_spec_str: str, option: str) -> VerificationResult:
        """
        Parameters
            solidity_spec_str: Solidity code with only the function signatures
            annotated with solc-verify conditions
        """
        Utils.save_string_to_file(cls.SPEC_FILE_PATH, solidity_spec_str)
        from solc_verify_generator.main import generate_merge
        
        template_path = ""
        if option == 'llm_base':
            template_path = cls.ERC1155_TEMPLATE_PATH_LLM_BASE
        elif option == 'base_llm':
            template_path = cls.ERC1155_TEMPLATE_PATH_BASE_LLM
        else:
            logging.error(f"Invalid option '{option}' for template path selection. Cannot find template.")
            return VerificationResult(-1, f"Invalid option '{option}' for template path selection. Template not found.")

        if not os.path.exists(template_path):
            logging.error(f"Template file not found at path: {template_path} for option '{option}'.")
            return VerificationResult(-1, f"Template file not found for option '{option}': {template_path}")

        try:
            generate_merge(cls.SPEC_FILE_PATH, template_path, cls.ERC1155_MERGE_PATH, option, prefix='con')
        except RuntimeError as e:
            return VerificationResult(*e.args)
        return cls.call_solc(cls.ERC1155_MERGE_PATH)

class Utils:

    @staticmethod
    def save_string_to_file(file_name, content):
        try:
            with open(file_name, 'w') as file:
                file.write(content)
            print(f"Content successfully saved to {file_name}")
        except IOError as e:
            print(f"An error occurred while writing to the file: {e}")

    @staticmethod
    def save_results_to_csv(file_name: str, results: List[dict]):
        # Convert list of dictionaries to pandas DataFrame
        df = pd.DataFrame(results)
        
        try:
            # Save DataFrame to CSV
            df.to_csv(file_name, index=False)
            print(f"Results successfully saved to {file_name}")
        except IOError as e:
            print(f"An error occurred while writing to the file: {e}")
    
    @staticmethod
    def extract_annotated_code_from_csv(csv_file: str) -> pd.DataFrame:
        # Read the CSV file
        df = pd.read_csv(csv_file)

        # Filter rows where 'annotated_contract' column has a value
        filtered_df = df[df['annotated_contract'].notna()]

        # Create a new DataFrame with 'run' and 'annotated_contract' columns
        result_df = filtered_df[['run', 'annotated_contract']]
        return result_df

    @staticmethod
    def has_trivial_specifications(solidity_code: str) -> bool:
        """
        Check if the Solidity code contains only trivial specifications like '@postcondition true'
        Returns True if all specifications are trivial, False otherwise
        """
        # Find all postcondition and precondition specifications
        postcondition_pattern = r'///\s*@notice\s+postcondition\s+(.+)'
        precondition_pattern = r'///\s*@notice\s+precondition\s+(.+)'
        
        postconditions = re.findall(postcondition_pattern, solidity_code, re.IGNORECASE)
        preconditions = re.findall(precondition_pattern, solidity_code, re.IGNORECASE)
        
        all_conditions = postconditions + preconditions
        
        # If no conditions found, consider it trivial
        if not all_conditions:
            return True
            
        # Check if all conditions are trivial (true, True, or variations)
        for condition in all_conditions:
            condition_clean = condition.strip().lower()
            if condition_clean not in ['true', '1', 'true;']:
                return False
        
        return True

def run_refinement_verification_process(result_type: str, model_name: str, token_context: str, option: str, main_erc_standard_dir: str, output_dir_for_csv: str):
    file_prefix = ""
    if "func_by_func" in result_type:
        file_prefix = "fbf_"
    elif "entire_contract" in result_type:
        file_prefix = ""  # Assuming empty prefix for entire_contract
    else:
        logging.warning(f"Unknown or unhandled result_type pattern for file prefix: {result_type}. Skipping.")
        return

    input_csv_path = f"./experiments/{result_type}/{model_name}/{main_erc_standard_dir}/{token_context}/{file_prefix}{main_erc_standard_dir}_[{token_context}].csv"

    if not os.path.exists(input_csv_path):
        logging.warning(f"Input CSV not found, skipping: {input_csv_path}")
        return

    try:
        annotated_code_df = Utils.extract_annotated_code_from_csv(input_csv_path)
    except FileNotFoundError:
        logging.warning(f"Input CSV not found (FileNotFoundError), skipping: {input_csv_path}")
        return
    except Exception as e:
        logging.error(f"Error reading or processing CSV {input_csv_path}: {e}")
        return
        
    if annotated_code_df.empty:
        logging.info(f"No annotated contracts found or DataFrame is empty in {input_csv_path}. Skipping.")
        return
    
    verification_results = []

    for index, row in annotated_code_df.iterrows():
        run_number = row['run']
        solidity_code = row['annotated_contract']

        # Check if the specifications are trivial
        if Utils.has_trivial_specifications(solidity_code):
            verification_results.append({
                'run': run_number,
                'status': 'TRIVIAL',
                'output': 'Trivial specification detected (e.g., @postcondition true)'
            })
            continue

        try:
            verification_result = SolcVerifyWrapper.verify(solidity_code, option)
        except Exception as e:
            print(f"An error occurred during verification for run {run_number}: {e}")
            verification_results.append({
                'run': run_number,
                'status': -1,
                'output': str(e)
            })
            continue

        verification_results.append({
            'run': run_number,
            'status': verification_result.status,
            'output': verification_result.output
        })

    # Save all results to a CSV file
    output_csv_filename = f"{main_erc_standard_dir}_{token_context}_{option}.csv"
    full_output_csv_path = os.path.join(output_dir_for_csv, output_csv_filename)
    Utils.save_results_to_csv(full_output_csv_path, verification_results)

# --- Main Execution Logic ---
if __name__ == "__main__":
    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)

    for res_type in RESULT_TYPES:
        models_to_iterate = []
        if "fine_tuning" in res_type:
            models_to_iterate = MODELS_FOR_FINETUNING
        elif "base_full_context" in res_type:
            models_to_iterate = [MODEL_FOR_BASE]
        else:
            logging.warning(f"Unknown result type pattern: {res_type}. Skipping this result type.")
            continue

        res_type_output_dir = os.path.join(OUTPUT_BASE_DIR, res_type)
        os.makedirs(res_type_output_dir, exist_ok=True)

        for model in models_to_iterate:
            model_output_dir = os.path.join(res_type_output_dir, model)
            os.makedirs(model_output_dir, exist_ok=True)

            # Check if the model directory exists in the experiments path
            # e.g. ./experiments/results_entire_contract_fine_tuning/erc-XYZ-model/
            model_experiment_path_check = f"./experiments/{res_type}/{model}"
            if not os.path.isdir(model_experiment_path_check):
                logging.info(f"Model directory {model_experiment_path_check} not found. Skipping model {model} for {res_type}.")
                continue
            
            # Check if the target ERC standard directory exists for this model and result type
            # e.g. ./experiments/results_entire_contract_fine_tuning/erc-XYZ-model/erc1155/
            target_erc_path_check = os.path.join(model_experiment_path_check, TARGET_ERC_STANDARD_DIR)
            if not os.path.isdir(target_erc_path_check):
                logging.info(f"Target ERC standard directory {target_erc_path_check} not found. Skipping {TARGET_ERC_STANDARD_DIR} for model {model} under {res_type}.")
                continue


            for token_ctx in TOKEN_CONTEXTS:
                # Check if the specific token context directory exists
                # e.g. ./experiments/results_entire_contract_fine_tuning/erc-XYZ-model/erc1155/none/
                token_context_path_check = os.path.join(target_erc_path_check, token_ctx)
                if not os.path.isdir(token_context_path_check):
                    logging.info(f"Token context directory {token_context_path_check} not found. Skipping context {token_ctx} for model {model}, type {res_type}.")
                    continue

                for ver_option in VERIFICATION_OPTIONS:
                    logging.info(f"Running verification for: type={res_type}, model={model}, context={token_ctx}, option={ver_option}")
                    run_refinement_verification_process(
                        result_type=res_type,
                        model_name=model,
                        token_context=token_ctx,
                        option=ver_option,
                        main_erc_standard_dir=TARGET_ERC_STANDARD_DIR,
                        output_dir_for_csv=model_output_dir
                    )
    logging.info("Refinement verification process finished.")
