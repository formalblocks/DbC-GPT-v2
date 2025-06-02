import pandas as pd
import os
import re
import csv

# --- Configuration Constants (adapted from refinement_verifier.py) ---
TARGET_ERC_STANDARD_DIR = "erc1155" # This script is tailored for ERC1155 verification context from verifier
INPUT_RESULTS_BASE_DIR = './refinement_check_results'
OUTPUT_WIDE_FORMAT_BASE_DIR = './comparison_results_wide_format'

RESULT_TYPES_FOR_PROCESSING = [
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

# Define the main ERC1155 functions to be included
MAIN_ERC1155_FUNCTION_STEMS = [
    "balanceOf",
    "balanceOfBatch",
    "isApprovedForAll",
    "safeBatchTransferFrom",
    "safeTransferFrom",
    "setApprovalForAll"
]

# Generate full function names (e.g., "balanceOf_pre", "balanceOf_post")
# These will be the columns in the output CSV, ensuring consistency.
ALLOWED_FULL_FUNCTION_NAMES = sorted([
    f"{stem}_{suffix}"
    for stem in MAIN_ERC1155_FUNCTION_STEMS
    for suffix in ["pre", "post"]
])
# --- End Configuration Constants ---

def extract_all_function_results_from_output(output_str):
    """
    Extracts ALL function verification results (Refinement::func: RESULT)
    from the 'output' column string.
    Returns a dictionary: {'function_name': 'OK'/'ERROR', ...}
    """
    results = {}
    if pd.isna(output_str):
        return results
    pattern = re.compile(r"Refinement::([^:]+): (OK|ERROR)")
    matches = pattern.findall(str(output_str))
    for func_name, result_status in matches:
        results[func_name.strip()] = result_status.strip()
    return results

# --- Main Execution Logic ---
if __name__ == "__main__":
    os.makedirs(OUTPUT_WIDE_FORMAT_BASE_DIR, exist_ok=True)
    print(f"Starting CSV generation with function filtering. Output will be in: {OUTPUT_WIDE_FORMAT_BASE_DIR}")

    for res_type in RESULT_TYPES_FOR_PROCESSING:
        res_type_output_dir = os.path.join(OUTPUT_WIDE_FORMAT_BASE_DIR, res_type)
        os.makedirs(res_type_output_dir, exist_ok=True)

        models_to_iterate = []
        if "base_full_context" in res_type:
            models_to_iterate = [MODEL_FOR_BASE]
        elif "fine_tuning" in res_type:
            models_to_iterate = MODELS_FOR_FINETUNING
        else:
            print(f"Warning: Unknown result type pattern: {res_type}. Skipping.")
            continue

        for model_name in models_to_iterate:
            model_output_dir = os.path.join(res_type_output_dir, model_name)
            os.makedirs(model_output_dir, exist_ok=True)

            # Check if the model directory exists in the input results path
            model_input_path_check = os.path.join(INPUT_RESULTS_BASE_DIR, res_type, model_name)
            if not os.path.isdir(model_input_path_check):
                # print(f"Info: Input model directory {model_input_path_check} not found. Skipping model {model_name} for {res_type}.")
                continue

            for token_ctx in TOKEN_CONTEXTS:
                file_path_ref_gen = os.path.join(INPUT_RESULTS_BASE_DIR, res_type, model_name, f"{TARGET_ERC_STANDARD_DIR}_{token_ctx}_base_llm.csv")
                file_path_gen_ref = os.path.join(INPUT_RESULTS_BASE_DIR, res_type, model_name, f"{TARGET_ERC_STANDARD_DIR}_{token_ctx}_llm_base.csv")

                if not (os.path.exists(file_path_ref_gen) and os.path.exists(file_path_gen_ref)):
                    # print(f"Info: Skipping. CSVs not found for {res_type}, {model_name}, {token_ctx}")
                    continue
                
                try:
                    df_ref_gen = pd.read_csv(file_path_ref_gen)
                    df_gen_ref = pd.read_csv(file_path_gen_ref)

                    if df_ref_gen.empty or df_gen_ref.empty:
                        # print(f"Info: Skipping. Empty CSV(s) for {res_type}, {model_name}, {token_ctx}")
                        continue
                    if not ({'run', 'output'}.issubset(df_ref_gen.columns) and {'run', 'output'}.issubset(df_gen_ref.columns)):
                        # print(f"Warning: 'run' or 'output' column missing in CSVs for {res_type}, {model_name}, {token_ctx}. Skipping.")
                        continue
                        
                    merged_df = pd.merge(df_ref_gen[['run', 'output']], df_gen_ref[['run', 'output']], on='run', suffixes=('_ref_gen', '_gen_ref'), how='inner')

                    if merged_df.empty:
                        # print(f"Info: Skipping. No common runs for {res_type}, {model_name}, {token_ctx}")
                        continue

                    parsed_runs_data_for_csv = []

                    for _, row in merged_df.iterrows():
                        run_id = row['run']
                        # Extract ALL function results first
                        all_results_ref_gen = extract_all_function_results_from_output(row['output_ref_gen'])
                        all_results_gen_ref = extract_all_function_results_from_output(row['output_gen_ref'])
                        
                        current_run_data_for_row = {'run': run_id}
                        is_fully_equivalent_for_run = True
                        
                        # Determine which of the ALLOWED_FULL_FUNCTION_NAMES were actually reported in this run
                        main_funcs_reported_this_run = set()
                        for func_name in ALLOWED_FULL_FUNCTION_NAMES:
                            if func_name in all_results_ref_gen or func_name in all_results_gen_ref:
                                main_funcs_reported_this_run.add(func_name)

                        if not main_funcs_reported_this_run: # No *main* functions reported for this run
                            is_fully_equivalent_for_run = False

                        for func_name in ALLOWED_FULL_FUNCTION_NAMES: # Iterate over the fixed list for consistent columns
                            # Get result for this specific function, or N/A if not present in this run's output (even if it's an allowed function)
                            res_ref_gen = all_results_ref_gen.get(func_name, 'N/A')
                            res_gen_ref = all_results_gen_ref.get(func_name, 'N/A')
                            
                            current_run_data_for_row[f"{func_name}_base_llm_status"] = res_ref_gen
                            current_run_data_for_row[f"{func_name}_llm_base_status"] = res_gen_ref

                            # For 'refines all', only consider functions that were actually reported in *this* run's output
                            # from the list of main functions
                            if func_name in main_funcs_reported_this_run:
                                if not (res_ref_gen == 'OK' and res_gen_ref == 'OK'):
                                    is_fully_equivalent_for_run = False
                        
                        current_run_data_for_row['refines_all_main_functions'] = 'Yes' if is_fully_equivalent_for_run else 'No'
                        parsed_runs_data_for_csv.append(current_run_data_for_row)
                    
                    if not parsed_runs_data_for_csv: # No runs to process after parsing
                        continue

                    # Prepare headers for the wide CSV
                    header1_function_row = ['function']
                    header2_option_row = ['option']
                    header3_run_placeholder_row = ['run']

                    for func_name in ALLOWED_FULL_FUNCTION_NAMES: # These are already sorted
                        header1_function_row.extend([func_name, func_name])
                        header2_option_row.extend(['base_llm', 'llm_base'])
                        header3_run_placeholder_row.extend(['', ''])
                    
                    header1_function_row.append('refines all')
                    header2_option_row.append('') 
                    header3_run_placeholder_row.append('')

                    # Write to CSV
                    output_csv_filename = f"comparison_{TARGET_ERC_STANDARD_DIR}_{token_ctx}.csv"
                    full_output_csv_path = os.path.join(model_output_dir, output_csv_filename)

                    with open(full_output_csv_path, 'w', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow(header1_function_row)
                        writer.writerow(header2_option_row)
                        writer.writerow(header3_run_placeholder_row)
                        
                        for run_data_dict in parsed_runs_data_for_csv:
                            csv_data_row = [run_data_dict['run']]
                            for func_name in ALLOWED_FULL_FUNCTION_NAMES:
                                csv_data_row.append(run_data_dict.get(f"{func_name}_base_llm_status", 'N/A'))
                                csv_data_row.append(run_data_dict.get(f"{func_name}_llm_base_status", 'N/A'))
                            csv_data_row.append(run_data_dict['refines_all_main_functions'])
                            writer.writerow(csv_data_row)
                    # print(f"Successfully generated/updated: {full_output_csv_path}")

                except pd.errors.EmptyDataError:
                    # print(f"Info: EmptyDataError for one of the input CSVs for {res_type}, {model_name}, {token_ctx}. Skipping.")
                    continue
                except FileNotFoundError: # Should be caught by os.path.exists, but safeguard
                    # print(f"Info: FileNotFoundError during processing for {res_type}, {model_name}, {token_ctx}. Skipping.")
                    continue
                except Exception as e:
                    print(f"Error processing files for {res_type}/{model_name}/{TARGET_ERC_STANDARD_DIR}_{token_ctx}.csv: {e}")
                    continue
    print("Finished CSV generation with function filtering.")