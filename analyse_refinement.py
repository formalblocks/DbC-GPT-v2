import pandas as pd
import os
import re
import csv

# --- Configuration Constants (adapted from refinement_verifier.py) ---
INPUT_RESULTS_BASE_DIR = './refinement_check_results'
OUTPUT_WIDE_FORMAT_BASE_DIR = './comparison_results_wide_format'

RESULT_TYPES_FOR_PROCESSING = [
    'results_entire_contract_base_full_context',
    'results_entire_contract_fine_tuning',
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

# Define ERC standards and their function stems
ERC_STANDARDS_CONFIG = {
    'erc20': {
        'function_stems': [
            "allowance",
            "approve", 
            "balanceOf",
            "totalSupply",
            "transfer",
            "transferFrom"
        ]
    },
    'erc721': {
        'function_stems': [
            "approve",
            "balanceOf",
            "getApproved", 
            "isApprovedForAll",
            "ownerOf",
            "safeTransferFrom",
            "setApprovalForAll",
            "transferFrom"
        ]
    },
    'erc1155': {
        'function_stems': [
            "balanceOf",
            "balanceOfBatch",
            "isApprovedForAll",
            "safeBatchTransferFrom",
            "safeTransferFrom",
            "setApprovalForAll"
        ]
    }
}

# --- End Configuration Constants ---

def get_allowed_function_names_for_standard(standard):
    """Get the allowed full function names for a given ERC standard."""
    function_stems = ERC_STANDARDS_CONFIG[standard]['function_stems']
    return sorted([f"{stem}_{suffix}" for stem in function_stems for suffix in ["pre", "post"]])

def extract_all_function_results_from_output(output_str):
    """
    Extracts ALL function verification results (Refinement::func: RESULT)
    from the 'output' column string.
    Returns a dictionary: {'function_name': 'OK'/'ERROR', ...}
    """
    results = {}
    if pd.isna(output_str):
        return results
    
    # Check if this is a trivial specification case
    if 'Trivial specification detected' in str(output_str):
        # For trivial specifications, mark all functions as ERROR since they don't provide meaningful verification
        # We'll populate this with the standard function names that should be present
        # This will be handled by the calling code that knows which functions to expect
        return {'TRIVIAL': 'ERROR'}
    
    pattern = re.compile(r"Refinement::([^:]+): (OK|ERROR)")
    matches = pattern.findall(str(output_str))
    for func_name, result_status in matches:
        results[func_name.strip()] = result_status.strip()
    return results

# --- Main Execution Logic ---
if __name__ == "__main__":
    os.makedirs(OUTPUT_WIDE_FORMAT_BASE_DIR, exist_ok=True)
    print(f"Starting CSV generation with function filtering. Output will be in: {OUTPUT_WIDE_FORMAT_BASE_DIR}")

    # Process each ERC standard
    for target_erc_standard in ERC_STANDARDS_CONFIG.keys():
        print(f"Processing {target_erc_standard.upper()} standard...")
        
        # Get allowed function names for this standard
        allowed_full_function_names = get_allowed_function_names_for_standard(target_erc_standard)

        for res_type in RESULT_TYPES_FOR_PROCESSING:
            res_type_output_dir = os.path.join(OUTPUT_WIDE_FORMAT_BASE_DIR, res_type)
            os.makedirs(res_type_output_dir, exist_ok=True)

            models_to_iterate = []
            if "base" in res_type:
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
                    file_path_ref_gen = os.path.join(INPUT_RESULTS_BASE_DIR, res_type, model_name, f"{target_erc_standard}_{token_ctx}_base_llm.csv")
                    file_path_gen_ref = os.path.join(INPUT_RESULTS_BASE_DIR, res_type, model_name, f"{target_erc_standard}_{token_ctx}_llm_base.csv")

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
                            
                            # Check if either result is trivial
                            is_trivial_ref_gen = 'TRIVIAL' in all_results_ref_gen
                            is_trivial_gen_ref = 'TRIVIAL' in all_results_gen_ref
                            
                            # Determine which of the allowed_full_function_names were actually reported in this run
                            main_funcs_reported_this_run = set()
                            for func_name in allowed_full_function_names:
                                if func_name in all_results_ref_gen or func_name in all_results_gen_ref:
                                    main_funcs_reported_this_run.add(func_name)

                            # If either result is trivial, mark all functions as ERROR for that direction
                            for func_name in allowed_full_function_names: # Iterate over the fixed list for consistent columns
                                # Handle trivial specifications
                                if is_trivial_ref_gen:
                                    res_ref_gen = 'ERROR'  # Trivial specs are treated as failed verification
                                else:
                                    res_ref_gen = all_results_ref_gen.get(func_name, 'N/A')
                                
                                if is_trivial_gen_ref:
                                    res_gen_ref = 'ERROR'  # Trivial specs are treated as failed verification
                                else:
                                    res_gen_ref = all_results_gen_ref.get(func_name, 'N/A')
                                
                                current_run_data_for_row[f"{func_name}_base_llm"] = res_ref_gen
                                current_run_data_for_row[f"{func_name}_llm_base"] = res_gen_ref

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
                        header = ['run']
                        for func_name in allowed_full_function_names: # These are already sorted
                            header.append(f"{func_name}_base_llm")
                            header.append(f"{func_name}_llm_base")
                        header.append('refines_all_main_functions')

                        # Write to CSV
                        output_csv_filename = f"comparison_{target_erc_standard}_{token_ctx}.csv"
                        full_output_csv_path = os.path.join(model_output_dir, output_csv_filename)

                        with open(full_output_csv_path, 'w', newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow(header)
                            
                            for run_data_dict in parsed_runs_data_for_csv:
                                csv_data_row = [run_data_dict['run']]
                                for func_name in allowed_full_function_names:
                                    csv_data_row.append(run_data_dict.get(f"{func_name}_base_llm", 'N/A'))
                                    csv_data_row.append(run_data_dict.get(f"{func_name}_llm_base", 'N/A'))
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
                        print(f"Error processing files for {res_type}/{model_name}/{target_erc_standard}_{token_ctx}.csv: {e}")
                        continue
    print("Finished CSV generation with function filtering.")