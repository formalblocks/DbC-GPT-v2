
## Refinement Quality Statistics for Entire Contract Mode (ERC1155 Functions)

*Note: Trivial specifications (e.g., `@postcondition true`) are excluded from quality analysis but shown in brackets when present.*


### Base Model (4o-mini) with Few-Shot Learning

| Dem. Context | Total Comp. | Weaker (≤) | Stronger (≥) | Equivalent (≡) | Not Comp. (\|\|) |
|:---|---:|---:|---:|---:|---:|
| epsilon | 0 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| erc20 | 0 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) |
| erc721 | 6 | 1 (16.7%) | 1 (16.7%) | 4 (66.7%) | 0 (0.0%) |
| erc1155 | 48 | 8 (16.7%) | 8 (16.7%) | 32 (66.7%) | 0 (0.0%) |
| erc20\_erc721 | 24 | 4 (16.7%) | 1 (4.2%) | 16 (66.7%) | 3 (12.5%) |
| erc20\_erc1155 | 54 | 9 (16.7%) | 4 (7.4%) | 36 (66.7%) | 5 (9.3%) |
| erc721\_erc1155 | 60 | 10 (16.7%) | 10 (16.7%) | 40 (66.7%) | 0 (0.0%) |
| erc20\_erc721\_erc1155 | 60 | 10 (16.7%) | 9 (15.0%) | 40 (66.7%) | 1 (1.7%) |


### Fine-Tuned Models

| Model | Total Comp. | Weaker (≤) | Stronger (≥) | Equivalent (≡) | Not Comp. (\|\|) |
|:---|---:|---:|---:|---:|---:|
| 4o-mini | 6 | 1 (16.7%) | 0 (0.0%) | 4 (66.7%) | 1 (16.7%) |
| erc-20-001-5-16 | 6 | 1 (16.7%) | 0 (0.0%) | 4 (66.7%) | 1 (16.7%) |
| erc-721-001-5-16 | 6 | 1 (16.7%) | 1 (16.7%) | 4 (66.7%) | 0 (0.0%) |
| erc-1155-001-5-16 | 30 | 6 (20.0%) | 3 (10.0%) | 20 (66.7%) | 1 (3.3%) |
| erc-20-721-001-5-16 | 18 | 2 (11.1%) | 0 (0.0%) | 8 (44.4%) | 8 (44.4%) |
| erc-20-1155-001-5-16 | 36 | 3 (8.3%) | 0 (0.0%) | 8 (22.2%) | 25 (69.4%) |
| erc-721-1155-001-5-16 | 30 | 5 (16.7%) | 1 (3.3%) | 20 (66.7%) | 4 (13.3%) |
| erc-20-721-1155-001-5-16 | 42 | 2 (4.8%) | 1 (2.4%) | 3 (7.1%) | 36 (85.7%) |


## Refinement Quality Statistics for Func By Func Mode (ERC1155 Functions)

*Note: Trivial specifications (e.g., `@postcondition true`) are excluded from quality analysis but shown in brackets when present.*


### Base Model (4o-mini) with Few-Shot Learning

| Dem. Context | Total Comp. | Weaker (≤) | Stronger (≥) | Equivalent (≡) | Not Comp. (\|\|) |
|:---|---:|---:|---:|---:|---:|
| epsilon | 60 | 12 (20.0%) | 0 (0.0%) | 18 (30.0%) | 30 (50.0%) |
| erc20 | 60 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 60 (100.0%) |
| erc721 | 60 | 20 (33.3%) | 0 (0.0%) | 40 (66.7%) | 0 (0.0%) |
| erc1155 | 60 | 10 (16.7%) | 10 (16.7%) | 40 (66.7%) | 0 (0.0%) |
| erc20\_erc721 | 60 | 17 (28.3%) | 3 (5.0%) | 40 (66.7%) | 0 (0.0%) |
| erc20\_erc1155 | 60 | 9 (15.0%) | 9 (15.0%) | 36 (60.0%) | 6 (10.0%) |
| erc721\_erc1155 | 60 | 9 (15.0%) | 9 (15.0%) | 36 (60.0%) | 6 (10.0%) |
| erc20\_erc721\_erc1155 | 60 | 9 (15.0%) | 9 (15.0%) | 36 (60.0%) | 6 (10.0%) |


### Fine-Tuned Models

| Model | Total Comp. | Weaker (≤) | Stronger (≥) | Equivalent (≡) | Not Comp. (\|\|) |
|:---|---:|---:|---:|---:|---:|
| 4o-mini | 60 | 9 (15.0%) | 0 (0.0%) | 15 (25.0%) | 36 (60.0%) |
| erc-20-001-5-16 | 60 | 1 (1.7%) | 1 (1.7%) | 4 (6.7%) | 54 (90.0%) |
| erc-721-001-5-16 | 60 | 3 (5.0%) | 3 (5.0%) | 12 (20.0%) | 42 (70.0%) |
| erc-1155-001-5-16 | 60 | 2 (3.3%) | 1 (1.7%) | 3 (5.0%) | 54 (90.0%) |
| erc-20-721-001-5-16 | 60 | 0 (0.0%) | 0 (0.0%) | 0 (0.0%) | 60 (100.0%) |
| erc-20-1155-001-5-16 | 60 | 8 (13.3%) | 7 (11.7%) | 27 (45.0%) | 18 (30.0%) |
| erc-721-1155-001-5-16 | 60 | 10 (16.7%) | 9 (15.0%) | 35 (58.3%) | 6 (10.0%) |
| erc-20-721-1155-001-5-16 | 60 | 4 (6.7%) | 2 (3.3%) | 6 (10.0%) | 48 (80.0%) |



--- Stronger Specification Occurrences (Pointers for Manual Review) ---
The following are instances where the LLM-generated specification was found to be stronger than the reference.
To view the actual LLM-generated specification text, you need to trace back to the original raw LLM output/
thread files (e.g., from 'experiments/threads...') that were used as input to 'refinement_verifier.py' for the corresponding run.
The 'Annotated Contract CSV' column below points to the CSV file containing the full contract source with the LLM-generated annotations for the specific run.\n
| Mode | Category | Identifier | Token Ctx | Run ID | Function | Annotated Contract CSV |
|:---|:---|:---|:---|:---|:---|:---|
| entire_contract | base_models | erc721 | erc721 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721/erc1155_[erc721].csv |
| entire_contract | base_models | erc1155 | erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155_[erc1155].csv |
| entire_contract | base_models | erc1155 | erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155_[erc1155].csv |
| entire_contract | base_models | erc1155 | erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155_[erc1155].csv |
| entire_contract | base_models | erc1155 | erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155_[erc1155].csv |
| entire_contract | base_models | erc1155 | erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155_[erc1155].csv |
| entire_contract | base_models | erc1155 | erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155_[erc1155].csv |
| entire_contract | base_models | erc1155 | erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155_[erc1155].csv |
| entire_contract | base_models | erc1155 | erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155_[erc1155].csv |
| entire_contract | base_models | erc20_erc721 | erc20_erc721 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc721/erc1155_[erc20_erc721].csv |
| entire_contract | base_models | erc20_erc1155 | erc20_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155_[erc20_erc1155].csv |
| entire_contract | base_models | erc20_erc1155 | erc20_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155_[erc20_erc1155].csv |
| entire_contract | base_models | erc20_erc1155 | erc20_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155_[erc20_erc1155].csv |
| entire_contract | base_models | erc20_erc1155 | erc20_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155_[erc20_erc1155].csv |
| entire_contract | base_models | erc721_erc1155 | erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155_[erc721_erc1155].csv |
| entire_contract | base_models | erc721_erc1155 | erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155_[erc721_erc1155].csv |
| entire_contract | base_models | erc721_erc1155 | erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155_[erc721_erc1155].csv |
| entire_contract | base_models | erc721_erc1155 | erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155_[erc721_erc1155].csv |
| entire_contract | base_models | erc721_erc1155 | erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155_[erc721_erc1155].csv |
| entire_contract | base_models | erc721_erc1155 | erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155_[erc721_erc1155].csv |
| entire_contract | base_models | erc721_erc1155 | erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155_[erc721_erc1155].csv |
| entire_contract | base_models | erc721_erc1155 | erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155_[erc721_erc1155].csv |
| entire_contract | base_models | erc721_erc1155 | erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155_[erc721_erc1155].csv |
| entire_contract | base_models | erc721_erc1155 | erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155_[erc721_erc1155].csv |
| entire_contract | base_models | erc20_erc721_erc1155 | erc20_erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155_[erc20_erc721_erc1155].csv |
| entire_contract | base_models | erc20_erc721_erc1155 | erc20_erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155_[erc20_erc721_erc1155].csv |
| entire_contract | base_models | erc20_erc721_erc1155 | erc20_erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155_[erc20_erc721_erc1155].csv |
| entire_contract | base_models | erc20_erc721_erc1155 | erc20_erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155_[erc20_erc721_erc1155].csv |
| entire_contract | base_models | erc20_erc721_erc1155 | erc20_erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155_[erc20_erc721_erc1155].csv |
| entire_contract | base_models | erc20_erc721_erc1155 | erc20_erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155_[erc20_erc721_erc1155].csv |
| entire_contract | base_models | erc20_erc721_erc1155 | erc20_erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155_[erc20_erc721_erc1155].csv |
| entire_contract | base_models | erc20_erc721_erc1155 | erc20_erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155_[erc20_erc721_erc1155].csv |
| entire_contract | base_models | erc20_erc721_erc1155 | erc20_erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155_[erc20_erc721_erc1155].csv |
| entire_contract | fine_tuning_models | erc-721-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_entire_contract_fine_tuning/erc-721-001-5-16/erc1155/none/erc1155_[none].csv |
| entire_contract | fine_tuning_models | erc-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_entire_contract_fine_tuning/erc-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| entire_contract | fine_tuning_models | erc-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_entire_contract_fine_tuning/erc-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| entire_contract | fine_tuning_models | erc-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_entire_contract_fine_tuning/erc-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| entire_contract | fine_tuning_models | erc-721-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_entire_contract_fine_tuning/erc-721-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| entire_contract | fine_tuning_models | erc-20-721-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_entire_contract_fine_tuning/erc-20-721-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | base_models | erc1155 | erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/erc1155_[erc1155].csv |
| func_by_func | base_models | erc1155 | erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/erc1155_[erc1155].csv |
| func_by_func | base_models | erc1155 | erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/erc1155_[erc1155].csv |
| func_by_func | base_models | erc1155 | erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/erc1155_[erc1155].csv |
| func_by_func | base_models | erc1155 | erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/erc1155_[erc1155].csv |
| func_by_func | base_models | erc1155 | erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/erc1155_[erc1155].csv |
| func_by_func | base_models | erc1155 | erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/erc1155_[erc1155].csv |
| func_by_func | base_models | erc1155 | erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/erc1155_[erc1155].csv |
| func_by_func | base_models | erc1155 | erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/erc1155_[erc1155].csv |
| func_by_func | base_models | erc1155 | erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/erc1155_[erc1155].csv |
| func_by_func | base_models | erc20_erc721 | erc20_erc721 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721/erc1155_[erc20_erc721].csv |
| func_by_func | base_models | erc20_erc721 | erc20_erc721 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721/erc1155_[erc20_erc721].csv |
| func_by_func | base_models | erc20_erc721 | erc20_erc721 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721/erc1155_[erc20_erc721].csv |
| func_by_func | base_models | erc20_erc1155 | erc20_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155_[erc20_erc1155].csv |
| func_by_func | base_models | erc20_erc1155 | erc20_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155_[erc20_erc1155].csv |
| func_by_func | base_models | erc20_erc1155 | erc20_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155_[erc20_erc1155].csv |
| func_by_func | base_models | erc20_erc1155 | erc20_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155_[erc20_erc1155].csv |
| func_by_func | base_models | erc20_erc1155 | erc20_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155_[erc20_erc1155].csv |
| func_by_func | base_models | erc20_erc1155 | erc20_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155_[erc20_erc1155].csv |
| func_by_func | base_models | erc20_erc1155 | erc20_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155_[erc20_erc1155].csv |
| func_by_func | base_models | erc20_erc1155 | erc20_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155_[erc20_erc1155].csv |
| func_by_func | base_models | erc20_erc1155 | erc20_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155_[erc20_erc1155].csv |
| func_by_func | base_models | erc721_erc1155 | erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155_[erc721_erc1155].csv |
| func_by_func | base_models | erc721_erc1155 | erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155_[erc721_erc1155].csv |
| func_by_func | base_models | erc721_erc1155 | erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155_[erc721_erc1155].csv |
| func_by_func | base_models | erc721_erc1155 | erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155_[erc721_erc1155].csv |
| func_by_func | base_models | erc721_erc1155 | erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155_[erc721_erc1155].csv |
| func_by_func | base_models | erc721_erc1155 | erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155_[erc721_erc1155].csv |
| func_by_func | base_models | erc721_erc1155 | erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155_[erc721_erc1155].csv |
| func_by_func | base_models | erc721_erc1155 | erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155_[erc721_erc1155].csv |
| func_by_func | base_models | erc721_erc1155 | erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155_[erc721_erc1155].csv |
| func_by_func | base_models | erc20_erc721_erc1155 | erc20_erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155_[erc20_erc721_erc1155].csv |
| func_by_func | base_models | erc20_erc721_erc1155 | erc20_erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155_[erc20_erc721_erc1155].csv |
| func_by_func | base_models | erc20_erc721_erc1155 | erc20_erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155_[erc20_erc721_erc1155].csv |
| func_by_func | base_models | erc20_erc721_erc1155 | erc20_erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155_[erc20_erc721_erc1155].csv |
| func_by_func | base_models | erc20_erc721_erc1155 | erc20_erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155_[erc20_erc721_erc1155].csv |
| func_by_func | base_models | erc20_erc721_erc1155 | erc20_erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155_[erc20_erc721_erc1155].csv |
| func_by_func | base_models | erc20_erc721_erc1155 | erc20_erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155_[erc20_erc721_erc1155].csv |
| func_by_func | base_models | erc20_erc721_erc1155 | erc20_erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155_[erc20_erc721_erc1155].csv |
| func_by_func | base_models | erc20_erc721_erc1155 | erc20_erc721_erc1155 | OK | balanceOfBatch_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155_[erc20_erc721_erc1155].csv |
| func_by_func | fine_tuning_models | erc-20-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-20-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-721-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-721-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-721-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-721-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-721-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-721-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-20-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-20-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-20-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-20-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-20-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-20-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-20-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-721-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-721-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-721-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-721-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-721-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-721-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-721-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-721-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-721-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-20-721-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-20-721-1155-001-5-16/erc1155/none/erc1155_[none].csv |
| func_by_func | fine_tuning_models | erc-20-721-1155-001-5-16 | none | OK | balanceOfBatch_post | experiments/results_func_by_func_fine_tuning/erc-20-721-1155-001-5-16/erc1155/none/erc1155_[none].csv |