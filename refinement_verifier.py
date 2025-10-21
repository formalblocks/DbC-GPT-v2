import logging
import sys
import pandas as pd
from dataclasses import dataclass
from typing import List
import os
import re
import tempfile
import shutil

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Initialize the global verification status
# verification_status = [] # This was unused, can be removed or kept if intended for future use.

# --- Configuration Constants ---
VERIFICATION_OPTIONS = ['llm_base', 'base_llm']

# Define ERC standards to process
# ERC_STANDARDS = ['erc20', 'erc721', 'erc1155']
ERC_STANDARDS = ['erc1155']

RESULT_TYPES = [
    # 'results_entire_contract_base_full_context',
    # 'results_entire_contract_fine_tuning',
    'results_func_by_func_base_full_context',
    'results_func_by_func_fine_tuning',
]

MODELS_FOR_FINETUNING = [
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
    SOLC_VERIFY_TIMEOUT = int(os.getenv("SOLC_VERIFY_TIMEOUT", "120"))

    # Template and merge paths for different ERC standards
    TEMPLATE_PATHS = {
        'erc20': {
            'base_llm': './experiments/solc_verify_generator/ERC20/templates/spec_refinement_base_llm.template',
            'llm_base': './experiments/solc_verify_generator/ERC20/templates/spec_refinement_llm_base.template'
        },
        'erc721': {
            'base_llm': './experiments/solc_verify_generator/ERC721/templates/spec_refinement_base_llm.template',
            'llm_base': './experiments/solc_verify_generator/ERC721/templates/spec_refinement_llm_base.template'
        },
        'erc1155': {
            'base_llm': './experiments/solc_verify_generator/ERC1155/templates/spec_refinement_base_llm.template',
            'llm_base': './experiments/solc_verify_generator/ERC1155/templates/spec_refinement_llm_base.template'
        }
    }

    MERGE_PATHS = {
        'erc20': './experiments/solc_verify_generator/ERC20/imp/ERC20_merge.sol',
        'erc721': './experiments/solc_verify_generator/ERC721/imp/ERC721_merge.sol',
        'erc1155': './experiments/solc_verify_generator/ERC1155/imp/ERC1155_merge.sol'
    }

    @classmethod
    def call_solc(cls, file_path) -> VerificationResult:
        from subprocess import PIPE, run, TimeoutExpired
        timeout = cls.SOLC_VERIFY_TIMEOUT
        # Pass --timeout to solc-verify and also enforce Python-level kill
        command = [
            cls.SOLC_VERIFY_CMD,
            "--timeout", str(timeout),
            "--show-warnings",
            file_path
        ]
        logging.info(f"Invoking solc-verify: {' '.join(command)}")

        try:
            result = run(
                command,
                stdout=PIPE, stderr=PIPE,
                universal_newlines=True,
                check=False,
                timeout=timeout + 10
            )
            return VerificationResult(result.returncode, result.stdout + result.stderr)
        except FileNotFoundError:
            logging.error(f"Command not found: {cls.SOLC_VERIFY_CMD}. Make sure solc-verify.py is installed and in PATH.")
            return VerificationResult(-1, f"Command not found: {cls.SOLC_VERIFY_CMD}")
        except TimeoutExpired:
            logging.error(f"solc-verify timed out after {timeout}s")
            return VerificationResult(-1, f"solc-verify TIMEOUT after {timeout}s")
        except Exception as e:
            logging.error(f"Error running solc-verify: {e} on file {file_path}")
            return VerificationResult(-1, f"Error running solc-verify: {e}")
    
    @classmethod
    def verify(cls, solidity_spec_str: str, option: str, erc_standard: str) -> VerificationResult:
        """
        Parameters
            solidity_spec_str: Solidity code with only the function signatures
            annotated with solc-verify conditions
            option: 'llm_base' or 'base_llm'
            erc_standard: 'erc20', 'erc721', or 'erc1155'
        """
        # Get template and merge paths for the specified ERC standard
        if erc_standard not in cls.TEMPLATE_PATHS:
            logging.error(f"Unsupported ERC standard: {erc_standard}")
            return VerificationResult(-1, f"Unsupported ERC standard: {erc_standard}")
        
        if option not in cls.TEMPLATE_PATHS[erc_standard]:
            logging.error(f"Invalid option '{option}' for ERC standard '{erc_standard}'. Cannot find template.")
            return VerificationResult(-1, f"Invalid option '{option}' for ERC standard '{erc_standard}'. Template not found.")

        template_path = cls.TEMPLATE_PATHS[erc_standard][option]
        original_merge_file_path = cls.MERGE_PATHS[erc_standard]

        if not os.path.exists(template_path):
            logging.error(f"Template file not found at path: {template_path} for option '{option}' and ERC standard '{erc_standard}'.")
            return VerificationResult(-1, f"Template file not found for option '{option}' and ERC standard '{erc_standard}': {template_path}")

        dependency_source_dir = os.path.dirname(original_merge_file_path)
        if not os.path.isdir(dependency_source_dir):
            logging.warning(f"Dependency source directory not found or not a directory: {dependency_source_dir}")

        workdir = None
        try:
            workdir = tempfile.mkdtemp(prefix="solc_verify_refinement_")
            spec_file_in_workdir = os.path.join(workdir, "spec.sol")
            merge_file_basename = os.path.basename(original_merge_file_path)

            Utils.save_string_to_file(spec_file_in_workdir, solidity_spec_str)

            # Create temp directory for AST output
            os.makedirs(os.path.join(workdir, "temp"), exist_ok=True)

            # Copy dependencies from source directory
            if os.path.isdir(dependency_source_dir):
                for item_name in os.listdir(dependency_source_dir):
                    source_item_path = os.path.join(dependency_source_dir, item_name)
                    dest_item_path = os.path.join(workdir, item_name)
                    
                    if os.path.isdir(source_item_path):
                        shutil.copytree(source_item_path, dest_item_path)
                    elif item_name.endswith(".sol") or os.path.isfile(source_item_path):
                        shutil.copy2(source_item_path, dest_item_path)
                logging.debug(f"Copied dependencies from {dependency_source_dir} to {workdir}")

            from experiments.solc_verify_generator.main import generate_merge
            
            original_cwd = os.getcwd()
            os.chdir(workdir)
            try:
                absolute_template_path = os.path.abspath(os.path.join(original_cwd, template_path))
                if not os.path.exists(absolute_template_path):
                    logging.error(f"Template file not found: {absolute_template_path}")
                    return VerificationResult(-1, f"Template file not found: {absolute_template_path}")

                generate_merge(
                    "spec.sol",
                    absolute_template_path, 
                    merge_file_basename,
                    option,
                    prefix='con'
                )
            except RuntimeError as e:
                logging.error(f"Error during generate_merge: {e}")
                return VerificationResult(e.args[0] if len(e.args) > 0 else -1, str(e.args[1] if len(e.args) > 1 else e))
            except Exception as e:
                logging.error(f"Unexpected error during generate_merge: {e}")
                return VerificationResult(-1, f"Unexpected error during generate_merge: {e}")
            finally:
                os.chdir(original_cwd)
            
            # Execute solc-verify in the working directory
            os.chdir(workdir)
            try:
                verification_result = cls.call_solc(merge_file_basename)
            finally:
                os.chdir(original_cwd)
            
            return verification_result
        except Exception as e:
            logging.error(f"Verification error: {e}")
            return VerificationResult(-1, f"Verification error: {e}")
        finally:
            # Enhanced cleanup with multiple attempts
            if workdir and os.path.exists(workdir):
                try:
                    # First attempt at cleanup
                    shutil.rmtree(workdir, ignore_errors=True)
                except Exception as cleanup_error:
                    logging.warning(f"First cleanup attempt failed: {cleanup_error}")
                    try:
                        # Second attempt with more aggressive cleanup
                        import stat
                        def handle_remove_readonly(func, path, exc):
                            if os.path.exists(path):
                                os.chmod(path, stat.S_IWRITE)
                                func(path)
                        shutil.rmtree(workdir, onerror=handle_remove_readonly)
                    except Exception as second_cleanup_error:
                        logging.warning(f"Second cleanup attempt failed: {second_cleanup_error}")
                
                # Force garbage collection after cleanup
                try:
                    import gc
                    gc.collect()
                except Exception as gc_error:
                    logging.debug(f"Garbage collection failed: {gc_error}")

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
        result_df = pd.DataFrame(filtered_df[['run', 'annotated_contract']])
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

    @staticmethod
    def has_mixed_trivial_specifications(solidity_code: str) -> bool:
        """
        Check if the Solidity code contains a mix of trivial and meaningful specifications
        Returns True if some specs are trivial and others are meaningful, False otherwise
        """
        # Find all postcondition and precondition specifications
        postcondition_pattern = r'///\s*@notice\s+postcondition\s+(.+)'
        precondition_pattern = r'///\s*@notice\s+precondition\s+(.+)'

        postconditions = re.findall(postcondition_pattern, solidity_code, re.IGNORECASE)
        preconditions = re.findall(precondition_pattern, solidity_code, re.IGNORECASE)

        all_conditions = postconditions + preconditions

        # If no conditions found, not mixed
        if not all_conditions:
            return False

        trivial_count = 0
        meaningful_count = 0

        # Count trivial vs meaningful conditions
        for condition in all_conditions:
            condition_clean = condition.strip().lower()
            if condition_clean in ['true', '1', 'true;']:
                trivial_count += 1
            else:
                meaningful_count += 1

        # Mixed if we have both trivial and meaningful specifications
        return trivial_count > 0 and meaningful_count > 0

    @staticmethod
    def get_trivial_specification_ratio(solidity_code: str) -> float:
        """
        Calculate the ratio of trivial specifications to total specifications
        Returns a float between 0.0 and 1.0
        """
        # Find all postcondition and precondition specifications
        postcondition_pattern = r'///\s*@notice\s+postcondition\s+(.+)'
        precondition_pattern = r'///\s*@notice\s+precondition\s+(.+)'

        postconditions = re.findall(postcondition_pattern, solidity_code, re.IGNORECASE)
        preconditions = re.findall(precondition_pattern, solidity_code, re.IGNORECASE)

        all_conditions = postconditions + preconditions

        # If no conditions found, return 1.0 (all trivial)
        if not all_conditions:
            return 1.0

        trivial_count = 0

        # Count trivial conditions
        for condition in all_conditions:
            condition_clean = condition.strip().lower()
            if condition_clean in ['true', '1', 'true;']:
                trivial_count += 1

        return trivial_count / len(all_conditions)

def run_refinement_verification_process(result_type: str, model_name: str, token_context: str, option: str, main_erc_standard_dir: str, output_dir_for_csv: str):
    file_prefix = ""
    if "func_by_func" in result_type:
        file_prefix = "fbf_"

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
        solidity_code = str(row['annotated_contract'])

        # Check if the specifications are trivial
        if Utils.has_trivial_specifications(solidity_code):
            verification_results.append({
                'run': run_number,
                'status': 'TRIVIAL',
                'output': 'Trivial specification detected (e.g., @postcondition true)'
            })
            continue

        # Check for mixed trivial/meaningful specifications
        has_mixed_trivial = Utils.has_mixed_trivial_specifications(solidity_code)
        trivial_ratio = Utils.get_trivial_specification_ratio(solidity_code)

        try:
            verification_result = SolcVerifyWrapper.verify(solidity_code, option, main_erc_standard_dir)
        except Exception as e:
            print(f"An error occurred during verification for run {run_number}: {e}")
            verification_results.append({
                'run': run_number,
                'status': -1,
                'output': str(e)
            })
            continue

        # Interpret results based on trivial specification content
        if verification_result.status == 0 and has_mixed_trivial:
            # Success with mixed trivial specs likely means LLM specs are weaker
            if trivial_ratio >= 0.5:  # More than half are trivial
                verification_results.append({
                    'run': run_number,
                    'status': 'LLM_WEAKER',
                    'output': f'LLM specifications are weaker (trivial ratio: {trivial_ratio:.2f}). Base specs are stronger. Original: {verification_result.output}'
                })
            else:
                verification_results.append({
                    'run': run_number,
                    'status': 'MIXED_TRIVIAL',
                    'output': f'Mixed trivial/meaningful specifications (trivial ratio: {trivial_ratio:.2f}). Original: {verification_result.output}'
                })
        elif verification_result.status == 0 and trivial_ratio > 0:
            # Success with some trivial specs
            verification_results.append({
                'run': run_number,
                'status': 'PARTIALLY_TRIVIAL',
                'output': f'Success with {trivial_ratio:.2f} trivial specifications. Original: {verification_result.output}'
            })
        else:
            # Standard result
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
    # Ensure temp directory exists for compatibility
    os.makedirs('./temp', exist_ok=True)
    os.makedirs(OUTPUT_BASE_DIR, exist_ok=True)

    for res_type in RESULT_TYPES:
        models_to_iterate = []
        if "fine_tuning" in res_type:
            models_to_iterate = MODELS_FOR_FINETUNING
        elif "base" in res_type:
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
            
            # Process each ERC standard
            for erc_standard in ERC_STANDARDS:
                # Check if the target ERC standard directory exists for this model and result type
                # e.g. ./experiments/results_entire_contract_fine_tuning/erc-XYZ-model/erc1155/
                target_erc_path_check = os.path.join(model_experiment_path_check, erc_standard)
                if not os.path.isdir(target_erc_path_check):
                    logging.info(f"Target ERC standard directory {target_erc_path_check} not found. Skipping {erc_standard} for model {model} under {res_type}.")
                    continue

                for token_ctx in TOKEN_CONTEXTS:
                    # Check if the specific token context directory exists
                    # e.g. ./experiments/results_entire_contract_fine_tuning/erc-XYZ-model/erc1155/none/
                    token_context_path_check = os.path.join(target_erc_path_check, token_ctx)
                    if not os.path.isdir(token_context_path_check):
                        logging.info(f"Token context directory {token_context_path_check} not found. Skipping context {token_ctx} for model {model}, type {res_type}.")
                        continue

                    for ver_option in VERIFICATION_OPTIONS:
                        logging.info(f"Running verification for: type={res_type}, model={model}, context={token_ctx}, option={ver_option}, standard={erc_standard}")
                        run_refinement_verification_process(
                            result_type=res_type,
                            model_name=model,
                            token_context=token_ctx,
                            option=ver_option,
                            main_erc_standard_dir=erc_standard,
                            output_dir_for_csv=model_output_dir
                        )
    logging.info("Refinement verification process finished.")
