import pandas as pd
import os
import collections

# --- Configuration Constants (adapted from analyse_refinement.py) ---
OUTPUT_WIDE_FORMAT_BASE_DIR = './comparison_results_wide_format'
# Add INPUT_RESULTS_BASE_DIR to help locate original verifier input summary files
INPUT_RESULTS_BASE_DIR = './refinement_check_results'
OUTPUT_MARKDOWN_FILE = 'refinement_summary.md' # File to save markdown output
SOURCE_CONTRACT_FILES_BASE_DIR = 'experiments' # Directory containing CSVs with annotated contracts

RESULT_TYPES_FOR_PROCESSING = [
    'results_entire_contract_base_full_context',
    'results_entire_contract_fine_tuning',
    'results_func_by_func_base_full_context',
    'results_func_by_func_fine_tuning',
]

# Define the order of demonstration contexts for table rows
DEMONSTRATION_CONTEXTS_ORDER = [
    'none', 'erc20', 'erc721', 'erc1155',
    'erc20_erc721', 'erc20_erc1155', 'erc721_erc1155',
    'erc20_erc721_erc1155'
]

# Define the order of fine-tuned models for table rows
MODELS_FOR_FINETUNING_ORDER = [
    'erc-20-001-5-16',
    'erc-721-001-5-16',
    'erc-1155-001-5-16',
    'erc-20-721-001-5-16',
    'erc-20-1155-001-5-16',
    'erc-721-1155-001-5-16',
    'erc-20-721-1155-001-5-16'
]
MODEL_FOR_BASE = '4o-mini' # This is the model name used for base_full_context runs

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

# TOKEN_CONTEXTS is used for iterating through input files
TOKEN_CONTEXTS = DEMONSTRATION_CONTEXTS_ORDER # Align with defined order
# MODELS_FOR_FINETUNING is used for iterating through input files
MODELS_FOR_FINETUNING_INPUT_ITERATION = MODELS_FOR_FINETUNING_ORDER

# --- End Configuration Constants ---

def get_allowed_function_names_for_standard(standard):
    """Get the allowed full function names for a given ERC standard."""
    function_stems = ERC_STANDARDS_CONFIG[standard]['function_stems']
    return sorted([f"{stem}_{suffix}" for stem in function_stems for suffix in ["post"]])

def classify_specification_quality(ref_to_gen_status, gen_to_ref_status):
    """
    Classifies the quality of a generated specification based on two checks.
    ref_to_gen_status: Status of (Reference Spec -> Generated Spec) check.
    gen_to_ref_status: Status of (Generated Spec -> Reference Spec) check.
    """
    # Handle trivial specifications
    if ref_to_gen_status == 'TRIVIAL' or gen_to_ref_status == 'TRIVIAL':
        return 'trivial'
    
    if ref_to_gen_status == 'N/A' or gen_to_ref_status == 'N/A':
        return 'not_comparable'

    is_ref_to_gen_ok = (ref_to_gen_status == 'OK')
    is_gen_to_ref_ok = (gen_to_ref_status == 'OK')

    if is_ref_to_gen_ok and is_gen_to_ref_ok:
        return 'equivalent'
    elif is_ref_to_gen_ok and not is_gen_to_ref_ok:
        return 'weaker'  # Generated spec is weaker
    elif not is_ref_to_gen_ok and is_gen_to_ref_ok:
        return 'stronger'  # Generated spec is stronger
    elif not is_ref_to_gen_ok and not is_gen_to_ref_ok: # Both are ERROR
        return 'not_comparable'
    
    # Should not be reached if inputs are only 'OK', 'ERROR', 'N/A', 'TRIVIAL'
    print(f"Warning: Unhandled status combination: Ref->Gen: {ref_to_gen_status}, Gen->Ref: {gen_to_ref_status}")
    return 'unknown_classification'

def get_markdown_table_row(label, stats, classification_order):
    escaped_label = label.replace('_', '\\_') # Escape underscores for Markdown
    row_parts = [f"| {escaped_label} "] # Use the escaped label here
    
    # Calculate total comparisons excluding trivial specifications
    total_comparisons = sum(stats.get(key, 0) for key in classification_order)
    
    row_parts.append(f" {str(total_comparisons)} ")
    for quality_key in classification_order:
        count = stats.get(quality_key, 0)
        percentage = (count / total_comparisons * 100) if total_comparisons > 0 else 0
        row_parts.append(f" {count} ({percentage:.1f}%) ")
    
    # Add trivial count as additional info (not included in percentages)
    trivial_count = stats.get('trivial', 0)
    if trivial_count > 0:
        row_parts.append(f" [{trivial_count} trivial] ")
    
    return "|".join(row_parts) + "|"

def generate_markdown_summary_tables(stats_data):
    md_output_parts = [] # Changed from md_output to avoid conflict
    classification_order = ['weaker', 'stronger', 'equivalent', 'not_comparable']
    column_headers_map = {
        'weaker': 'Weaker (≤)',
        'stronger': 'Stronger (≥)',
        'equivalent': 'Equivalent (≡)',
        'not_comparable': 'Not Comp. (\|\|)'
    }
    header_row_names = ['Dem. Context' if cat_key == 'base_models' else 'Model' for cat_key in ['base_models', 'fine_tuning_models']]

    for mode in ['entire_contract', 'func_by_func']:
        if mode not in stats_data or not stats_data[mode]:
            md_output_parts.append(f"\n## No data for mode: {mode}\n")
            continue

        mode_title = mode.replace("_", " ").title()
        md_output_parts.append(f"\n## Refinement Quality Statistics for {mode_title} Mode\n")
        md_output_parts.append("*Note: Trivial specifications (e.g., `@postcondition true`) are excluded from quality analysis but shown in brackets when present.*\n")

        # Process each ERC standard
        for standard in ['erc20', 'erc721', 'erc1155']:
            standard_title = standard.upper()
            md_output_parts.append(f"\n### {standard_title} Functions\n")

            # Base Models (Few-Shot)
            md_output_parts.append(f"\n#### Base Model ({MODEL_FOR_BASE}) with Few-Shot Learning - {standard_title}\n")
            md_output_parts.append(f"| {header_row_names[0]} | Total Comp. | " + " | ".join([column_headers_map[key] for key in classification_order]) + " |")
            md_output_parts.append("|:---|---:|---:|---:|---:|---:|")
            if 'base_models' in stats_data[mode] and standard in stats_data[mode]['base_models']:
                for dem_ctx in DEMONSTRATION_CONTEXTS_ORDER:
                    ctx_stats = stats_data[mode]['base_models'][standard].get(dem_ctx, collections.defaultdict(int))
                    md_output_parts.append(get_markdown_table_row(dem_ctx if dem_ctx != 'none' else "epsilon", ctx_stats, classification_order))
            else:
                md_output_parts.append("| No data available for base models. | | | | | |")
            md_output_parts.append("")

            # Fine-Tuning Models
            md_output_parts.append(f"\n#### Fine-Tuned Models - {standard_title}\n")
            md_output_parts.append(f"| {header_row_names[1]} | Total Comp. | " + " | ".join([column_headers_map[key] for key in classification_order]) + " |")
            md_output_parts.append("|:---|---:|---:|---:|---:|---:|")
            if 'fine_tuning_models' in stats_data[mode] and standard in stats_data[mode]['fine_tuning_models']:
                for model_name in MODELS_FOR_FINETUNING_ORDER:
                    model_stats = stats_data[mode]['fine_tuning_models'][standard].get(model_name, collections.defaultdict(int))
                    md_output_parts.append(get_markdown_table_row(model_name, model_stats, classification_order))
            else:
                md_output_parts.append("| No data available for fine-tuned models. | | | | | |")
            md_output_parts.append("")
    
    return "\n".join(md_output_parts)

if __name__ == "__main__":
    # Initialize stats structure to ensure all contexts/models/standards appear in tables
    overall_stats = {
        'entire_contract': {
            'base_models': {
                standard: {tc: collections.defaultdict(int) for tc in DEMONSTRATION_CONTEXTS_ORDER}
                for standard in ERC_STANDARDS_CONFIG.keys()
            },
            'fine_tuning_models': {
                standard: {mn: collections.defaultdict(int) for mn in MODELS_FOR_FINETUNING_ORDER}
                for standard in ERC_STANDARDS_CONFIG.keys()
            }
        },
        'func_by_func': {
            'base_models': {
                standard: {tc: collections.defaultdict(int) for tc in DEMONSTRATION_CONTEXTS_ORDER}
                for standard in ERC_STANDARDS_CONFIG.keys()
            },
            'fine_tuning_models': {
                standard: {mn: collections.defaultdict(int) for mn in MODELS_FOR_FINETUNING_ORDER}
                for standard in ERC_STANDARDS_CONFIG.keys()
            }
        }
    }

    print(f"Starting analysis of CSV files in: {OUTPUT_WIDE_FORMAT_BASE_DIR} for Markdown output...")

    stronger_spec_occurrences = []

    # Process each ERC standard
    for target_erc_standard in ERC_STANDARDS_CONFIG.keys():
        print(f"Processing {target_erc_standard.upper()} standard...")
        
        # Get allowed function names for this standard
        allowed_full_function_names = get_allowed_function_names_for_standard(target_erc_standard)
        
        # No need to prepare column names - we'll use the actual column names from CSV files

        for res_type in RESULT_TYPES_FOR_PROCESSING:
            current_mode = ""
            if "entire_contract" in res_type:
                current_mode = "entire_contract"
            elif "func_by_func" in res_type:
                current_mode = "func_by_func"
            else:
                print(f"Warning: Unknown mode in result type: {res_type}. Skipping.")
                continue

            current_model_category_key = ""
            models_to_iterate_for_input = []
            if "base_full_context" in res_type:
                current_model_category_key = "base_models"
                models_to_iterate_for_input = [MODEL_FOR_BASE]
            elif "fine_tuning" in res_type:
                current_model_category_key = "fine_tuning_models"
                models_to_iterate_for_input = MODELS_FOR_FINETUNING_INPUT_ITERATION
            else:
                print(f"Warning: Unknown model category in result type: {res_type}. Skipping.")
                continue
            
            res_type_input_dir = os.path.join(OUTPUT_WIDE_FORMAT_BASE_DIR, res_type)

            for model_name_in_path in models_to_iterate_for_input:
                model_input_dir = os.path.join(res_type_input_dir, model_name_in_path)
                if not os.path.isdir(model_input_dir):
                    # This can happen if analyse_refinement.py didn't produce output for this combination
                    # print(f"Info: Model directory not found, skipping: {model_input_dir}")
                    continue

                for token_ctx in TOKEN_CONTEXTS:
                    csv_filename = f"comparison_{target_erc_standard}_{token_ctx}.csv"
                    full_csv_path = os.path.join(model_input_dir, csv_filename)

                    if not os.path.exists(full_csv_path):
                        # print(f"Info: CSV file not found, skipping: {full_csv_path}")
                        continue
                    
                    try:
                        # Read CSV without skipping rows - the files don't have 3 header rows
                        df = pd.read_csv(full_csv_path, na_filter=False)
                        
                        if df.empty:
                            # print(f"Info: Empty CSV, skipping: {full_csv_path}")
                            continue

                        for index, row in df.iterrows():
                            for func_name in allowed_full_function_names:
                                status_ref_gen_col = f"{func_name}_base_llm"
                                status_gen_ref_col = f"{func_name}_llm_base"

                                # Ensure columns exist in the DataFrame (should always, due to analyse_refinement.py)
                                if status_ref_gen_col not in df.columns or status_gen_ref_col not in df.columns:
                                    # print(f"Warning: Missing columns for {func_name} in {full_csv_path}. Skipping function.")
                                    continue
                                    
                                status_ref_gen = row[status_ref_gen_col]
                                status_gen_ref = row[status_gen_ref_col]
                                
                                classification = classify_specification_quality(status_ref_gen, status_gen_ref)
                                
                                identifier_key = token_ctx if current_model_category_key == "base_models" else model_name_in_path
                                
                                if classification != 'unknown_classification':
                                    overall_stats[current_mode][current_model_category_key][target_erc_standard][identifier_key][classification] += 1
                                
                                if classification == 'stronger':
                                    # Path to the CSV file containing the annotated contract
                                    # Example: experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721/erc1155_[erc721].csv
                                    source_contract_csv_path = os.path.join(
                                        SOURCE_CONTRACT_FILES_BASE_DIR,
                                        res_type,
                                        model_name_in_path,
                                        target_erc_standard, # e.g., "erc1155" as a sub-directory
                                        token_ctx,               # e.g., "erc721" or "none" as a sub-directory
                                        f"{target_erc_standard}_[{token_ctx}].csv" # e.g., "erc1155_[erc721].csv"
                                    )
                                    stronger_spec_occurrences.append({
                                        'mode': current_mode,
                                        'model_category': current_model_category_key,
                                        'identifier': identifier_key,
                                        'standard': target_erc_standard,
                                        'token_context_file': token_ctx, # The token_ctx part of the CSV filename
                                        'run_id': row['run'],
                                        'function': func_name,
                                        'source_contract_csv_path': source_contract_csv_path # Updated key and path
                                    })
                    except pd.errors.EmptyDataError:
                        # print(f"Info: EmptyDataError for CSV, skipping: {full_csv_path}")
                        continue
                    except Exception as e:
                        print(f"Error processing file {full_csv_path}: {e}")
                        continue
    
    # Generate Markdown content
    markdown_summary_tables_content = generate_markdown_summary_tables(overall_stats)
    
    stronger_specs_md_parts = []
    if stronger_spec_occurrences:
        stronger_specs_md_parts.append("\n\n--- Stronger Specification Occurrences (Pointers for Manual Review) ---")
        stronger_specs_md_parts.append("The following are instances where the LLM-generated specification was found to be stronger than the reference.")
        stronger_specs_md_parts.append("To view the actual LLM-generated specification text, you need to trace back to the original raw LLM output/")
        stronger_specs_md_parts.append("thread files (e.g., from 'experiments/threads...') that were used as input to 'refinement_verifier.py' for the corresponding run.")
        stronger_specs_md_parts.append("The 'Annotated Contract CSV' column below points to the CSV file containing the full contract source with the LLM-generated annotations for the specific run.\\n")
        # Shorter headers for this table
        stronger_specs_md_parts.append("| Mode | Category | Identifier | Standard | Token Ctx | Run ID | Function | Annotated Contract CSV |")
        stronger_specs_md_parts.append("|:---|:---|:---|:---|:---|:---|:---|:---|")
        for item in stronger_spec_occurrences:
            # Escape pipe characters within the CSV path if they were to ever occur, though unlikely for paths
            escaped_csv_path = item['source_contract_csv_path'].replace("|", "\\\\|") # Updated key
            stronger_specs_md_parts.append(f"| {item['mode']} | {item['model_category']} | {item['identifier']} | {item['standard']} | {item['token_context_file']} | {item['run_id']} | {item['function']} | {escaped_csv_path} |")
    else:
        stronger_specs_md_parts.append("\n\n--- No Stronger Specification Occurrences Found ---")
    
    full_markdown_output = markdown_summary_tables_content + "\n" + "\n".join(stronger_specs_md_parts)

    # Save to file
    try:
        with open(OUTPUT_MARKDOWN_FILE, 'w') as f:
            f.write(full_markdown_output)
        print(f"\nMarkdown output successfully saved to: {OUTPUT_MARKDOWN_FILE}")
    except IOError as e:
        print(f"\nError saving Markdown output to file: {e}")

    print(f"\nFinished. Markdown output is in {OUTPUT_MARKDOWN_FILE}.") 