## Refinement Quality Statistics for Entire Contract Mode

_Note: Trivial specifications (e.g., `@postcondition true`) are excluded from quality analysis and not counted in totals._

### ERC20 Functions

#### Base Model (4o-mini) with Few-Shot Learning - ERC20

| Dem. Context         | Total Comp. | Weaker (≤) | Stronger (≥) | Equivalent (≡) | Not Comp. (\|\|) |
| :------------------- | ----------: | ---------: | -----------: | -------------: | ---------------: |
| epsilon              |          24 |   0 (0.0%) |     0 (0.0%) |     12 (50.0%) |       12 (50.0%) |
| erc20                |          60 |   0 (0.0%) |     0 (0.0%) |    60 (100.0%) |         0 (0.0%) |
| erc721               |          12 |   0 (0.0%) |     0 (0.0%) |      6 (50.0%) |        6 (50.0%) |
| erc1155              |          12 |   0 (0.0%) |     0 (0.0%) |      6 (50.0%) |        6 (50.0%) |
| erc20_erc721         |          54 |   2 (3.7%) |     1 (1.9%) |     50 (92.6%) |         1 (1.9%) |
| erc20_erc1155        |          60 |   0 (0.0%) |     0 (0.0%) |    60 (100.0%) |         0 (0.0%) |
| erc721_erc1155       |          12 |   0 (0.0%) |     0 (0.0%) |      6 (50.0%) |        6 (50.0%) |
| erc20_erc721_erc1155 |          60 |   0 (0.0%) |     0 (0.0%) |    60 (100.0%) |         0 (0.0%) |

#### Fine-Tuned Models - ERC20

| Model                    | Total Comp. | Weaker (≤) | Stronger (≥) | Equivalent (≡) | Not Comp. (\|\|) |
| :----------------------- | ----------: | ---------: | -----------: | -------------: | ---------------: |
| erc-20-001-5-16          |          18 |   0 (0.0%) |    4 (22.2%) |      9 (50.0%) |        5 (27.8%) |
| erc-721-001-5-16         |           6 |   0 (0.0%) |     0 (0.0%) |      3 (50.0%) |        3 (50.0%) |
| erc-1155-001-5-16        |          12 |   0 (0.0%) |     0 (0.0%) |      6 (50.0%) |        6 (50.0%) |
| erc-20-721-001-5-16      |          36 |   0 (0.0%) |     0 (0.0%) |     18 (50.0%) |       18 (50.0%) |
| erc-20-1155-001-5-16     |          24 |   1 (4.2%) |     1 (4.2%) |     12 (50.0%) |       10 (41.7%) |
| erc-721-1155-001-5-16    |          12 |   0 (0.0%) |     0 (0.0%) |      6 (50.0%) |        6 (50.0%) |
| erc-20-721-1155-001-5-16 |          36 |   1 (2.8%) |     0 (0.0%) |     18 (50.0%) |       17 (47.2%) |

### ERC721 Functions

#### Base Model (4o-mini) with Few-Shot Learning - ERC721

| Dem. Context         | Total Comp. | Weaker (≤) | Stronger (≥) | Equivalent (≡) | Not Comp. (\|\|) |
| :------------------- | ----------: | ---------: | -----------: | -------------: | ---------------: |
| epsilon              |           0 |   0 (0.0%) |     0 (0.0%) |       0 (0.0%) |         0 (0.0%) |
| erc20                |          40 | 19 (47.5%) |     0 (0.0%) |     11 (27.5%) |       10 (25.0%) |
| erc721               |          80 |   0 (0.0%) |     0 (0.0%) |     70 (87.5%) |       10 (12.5%) |
| erc1155              |           8 |  2 (25.0%) |    1 (12.5%) |      2 (25.0%) |        3 (37.5%) |
| erc20_erc721         |          80 |   0 (0.0%) |     0 (0.0%) |     70 (87.5%) |       10 (12.5%) |
| erc20_erc1155        |          32 |  8 (25.0%) |     3 (9.4%) |     15 (46.9%) |        6 (18.8%) |
| erc721_erc1155       |          80 |   0 (0.0%) |     0 (0.0%) |     70 (87.5%) |       10 (12.5%) |
| erc20_erc721_erc1155 |          80 |   0 (0.0%) |     0 (0.0%) |     70 (87.5%) |       10 (12.5%) |

#### Fine-Tuned Models - ERC721

| Model                    | Total Comp. | Weaker (≤) | Stronger (≥) | Equivalent (≡) | Not Comp. (\|\|) |
| :----------------------- | ----------: | ---------: | -----------: | -------------: | ---------------: |
| erc-20-001-5-16          |           8 |  4 (50.0%) |    1 (12.5%) |      1 (12.5%) |        2 (25.0%) |
| erc-721-001-5-16         |          24 | 15 (62.5%) |     0 (0.0%) |      5 (20.8%) |        4 (16.7%) |
| erc-1155-001-5-16        |          16 |  9 (56.2%) |     0 (0.0%) |      4 (25.0%) |        3 (18.8%) |
| erc-20-721-001-5-16      |          32 | 19 (59.4%) |     0 (0.0%) |      9 (28.1%) |        4 (12.5%) |
| erc-20-1155-001-5-16     |          16 |  8 (50.0%) |     0 (0.0%) |      6 (37.5%) |        2 (12.5%) |
| erc-721-1155-001-5-16    |          32 | 17 (53.1%) |     0 (0.0%) |       0 (0.0%) |       15 (46.9%) |
| erc-20-721-1155-001-5-16 |          56 | 31 (55.4%) |     0 (0.0%) |     15 (26.8%) |       10 (17.9%) |

### ERC1155 Functions

#### Base Model (4o-mini) with Few-Shot Learning - ERC1155

| Dem. Context         | Total Comp. | Weaker (≤) | Stronger (≥) | Equivalent (≡) | Not Comp. (\|\|) |
| :------------------- | ----------: | ---------: | -----------: | -------------: | ---------------: |
| epsilon              |           0 |   0 (0.0%) |     0 (0.0%) |       0 (0.0%) |         0 (0.0%) |
| erc20                |           0 |   0 (0.0%) |     0 (0.0%) |       0 (0.0%) |         0 (0.0%) |
| erc721               |           6 |  2 (33.3%) |    2 (33.3%) |      2 (33.3%) |         0 (0.0%) |
| erc1155              |          48 |  8 (16.7%) |   16 (33.3%) |     24 (50.0%) |         0 (0.0%) |
| erc20_erc721         |          24 |  8 (33.3%) |     1 (4.2%) |     12 (50.0%) |        3 (12.5%) |
| erc20_erc1155        |          54 |  9 (16.7%) |     4 (7.4%) |     36 (66.7%) |         5 (9.3%) |
| erc721_erc1155       |          60 | 10 (16.7%) |   10 (16.7%) |     40 (66.7%) |         0 (0.0%) |
| erc20_erc721_erc1155 |          60 | 10 (16.7%) |    9 (15.0%) |     40 (66.7%) |         1 (1.7%) |

#### Fine-Tuned Models - ERC1155

| Model                    | Total Comp. | Weaker (≤) | Stronger (≥) | Equivalent (≡) | Not Comp. (\|\|) |
| :----------------------- | ----------: | ---------: | -----------: | -------------: | ---------------: |
| erc-20-001-5-16          |           6 |  2 (33.3%) |     0 (0.0%) |      3 (50.0%) |        1 (16.7%) |
| erc-721-001-5-16         |           6 |  2 (33.3%) |    1 (16.7%) |      3 (50.0%) |         0 (0.0%) |
| erc-1155-001-5-16        |          30 | 11 (36.7%) |    3 (10.0%) |     15 (50.0%) |         1 (3.3%) |
| erc-20-721-001-5-16      |          18 |  4 (22.2%) |     0 (0.0%) |      6 (33.3%) |        8 (44.4%) |
| erc-20-1155-001-5-16     |          36 |  5 (13.9%) |     0 (0.0%) |      6 (16.7%) |       25 (69.4%) |
| erc-721-1155-001-5-16    |          30 | 10 (33.3%) |     1 (3.3%) |     15 (50.0%) |        4 (13.3%) |
| erc-20-721-1155-001-5-16 |          42 |   3 (7.1%) |     1 (2.4%) |       2 (4.8%) |       36 (85.7%) |

## Refinement Quality Statistics for Func By Func Mode

_Note: Trivial specifications (e.g., `@postcondition true`) are excluded from quality analysis and not counted in totals._

### ERC20 Functions

#### Base Model (4o-mini) with Few-Shot Learning - ERC20

| Dem. Context         | Total Comp. | Weaker (≤) | Stronger (≥) | Equivalent (≡) | Not Comp. (\|\|) |
| :------------------- | ----------: | ---------: | -----------: | -------------: | ---------------: |
| epsilon              |          31 |   0 (0.0%) |   10 (32.3%) |     20 (64.5%) |         1 (3.2%) |
| erc20                |          60 |   0 (0.0%) |     0 (0.0%) |    60 (100.0%) |         0 (0.0%) |
| erc721               |          41 |   0 (0.0%) |     4 (9.8%) |     24 (58.5%) |       13 (31.7%) |
| erc1155              |          35 |   1 (2.9%) |    4 (11.4%) |     17 (48.6%) |       13 (37.1%) |
| erc20_erc721         |          60 |   0 (0.0%) |     0 (0.0%) |     58 (96.7%) |         2 (3.3%) |
| erc20_erc1155        |          60 |   1 (1.7%) |     1 (1.7%) |     56 (93.3%) |         2 (3.3%) |
| erc721_erc1155       |          44 |   0 (0.0%) |    5 (11.4%) |     25 (56.8%) |       14 (31.8%) |
| erc20_erc721_erc1155 |          60 |   1 (1.7%) |     2 (3.3%) |     54 (90.0%) |         3 (5.0%) |

#### Fine-Tuned Models - ERC20

| Model                    | Total Comp. | Weaker (≤) | Stronger (≥) | Equivalent (≡) | Not Comp. (\|\|) |
| :----------------------- | ----------: | ---------: | -----------: | -------------: | ---------------: |
| erc-20-001-5-16          |          55 |   0 (0.0%) |     4 (7.3%) |     30 (54.5%) |       21 (38.2%) |
| erc-721-001-5-16         |          38 |   0 (0.0%) |   10 (26.3%) |     20 (52.6%) |        8 (21.1%) |
| erc-1155-001-5-16        |          50 |   0 (0.0%) |     3 (6.0%) |     27 (54.0%) |       20 (40.0%) |
| erc-20-721-001-5-16      |          58 |   0 (0.0%) |    7 (12.1%) |     30 (51.7%) |       21 (36.2%) |
| erc-20-1155-001-5-16     |          56 |   0 (0.0%) |    7 (12.5%) |     28 (50.0%) |       21 (37.5%) |
| erc-721-1155-001-5-16    |          57 |   0 (0.0%) |     5 (8.8%) |     26 (45.6%) |       26 (45.6%) |
| erc-20-721-1155-001-5-16 |          58 |   0 (0.0%) |    6 (10.3%) |     30 (51.7%) |       22 (37.9%) |

### ERC721 Functions

#### Base Model (4o-mini) with Few-Shot Learning - ERC721

| Dem. Context         | Total Comp. | Weaker (≤) | Stronger (≥) | Equivalent (≡) | Not Comp. (\|\|) |
| :------------------- | ----------: | ---------: | -----------: | -------------: | ---------------: |
| epsilon              |          36 |  4 (11.1%) |   10 (27.8%) |      7 (19.4%) |       15 (41.7%) |
| erc20                |          53 | 10 (18.9%) |     2 (3.8%) |     22 (41.5%) |       19 (35.8%) |
| erc721               |          80 |   0 (0.0%) |   15 (18.8%) |     55 (68.8%) |       10 (12.5%) |
| erc1155              |          52 |   4 (7.7%) |   23 (44.2%) |     21 (40.4%) |         4 (7.7%) |
| erc20_erc721         |          77 |   4 (5.2%) |     0 (0.0%) |     62 (80.5%) |       11 (14.3%) |
| erc20_erc1155        |          55 | 10 (18.2%) |   21 (38.2%) |     21 (38.2%) |         3 (5.5%) |
| erc721_erc1155       |          80 |   0 (0.0%) |   24 (30.0%) |     46 (57.5%) |       10 (12.5%) |
| erc20_erc721_erc1155 |          80 |   0 (0.0%) |     2 (2.5%) |     58 (72.5%) |       20 (25.0%) |

#### Fine-Tuned Models - ERC721

| Model                    | Total Comp. | Weaker (≤) | Stronger (≥) | Equivalent (≡) | Not Comp. (\|\|) |
| :----------------------- | ----------: | ---------: | -----------: | -------------: | ---------------: |
| erc-20-001-5-16          |          48 | 22 (45.8%) |     0 (0.0%) |      8 (16.7%) |       18 (37.5%) |
| erc-721-001-5-16         |          62 | 21 (33.9%) |     1 (1.6%) |     24 (38.7%) |       16 (25.8%) |
| erc-1155-001-5-16        |          59 | 15 (25.4%) |     5 (8.5%) |     13 (22.0%) |       26 (44.1%) |
| erc-20-721-001-5-16      |          57 | 22 (38.6%) |    8 (14.0%) |      9 (15.8%) |       18 (31.6%) |
| erc-20-1155-001-5-16     |          52 | 18 (34.6%) |     4 (7.7%) |     16 (30.8%) |       14 (26.9%) |
| erc-721-1155-001-5-16    |          54 | 14 (25.9%) |   14 (25.9%) |       5 (9.3%) |       21 (38.9%) |
| erc-20-721-1155-001-5-16 |          64 | 22 (34.4%) |     1 (1.6%) |     22 (34.4%) |       19 (29.7%) |

### ERC1155 Functions

#### Base Model (4o-mini) with Few-Shot Learning - ERC1155

| Dem. Context         | Total Comp. | Weaker (≤) | Stronger (≥) | Equivalent (≡) | Not Comp. (\|\|) |
| :------------------- | ----------: | ---------: | -----------: | -------------: | ---------------: |
| epsilon              |          60 | 17 (28.3%) |     0 (0.0%) |     13 (21.7%) |       30 (50.0%) |
| erc20                |          60 |   0 (0.0%) |     0 (0.0%) |       0 (0.0%) |      60 (100.0%) |
| erc721               |          60 | 31 (51.7%) |     2 (3.3%) |     27 (45.0%) |         0 (0.0%) |
| erc1155              |          60 | 12 (20.0%) |   10 (16.7%) |     38 (63.3%) |         0 (0.0%) |
| erc20_erc721         |          60 | 24 (40.0%) |     3 (5.0%) |     33 (55.0%) |         0 (0.0%) |
| erc20_erc1155        |          60 | 10 (16.7%) |    9 (15.0%) |     35 (58.3%) |        6 (10.0%) |
| erc721_erc1155       |          60 | 10 (16.7%) |   11 (18.3%) |     39 (65.0%) |         0 (0.0%) |
| erc20_erc721_erc1155 |          60 |  9 (15.0%) |    9 (15.0%) |     36 (60.0%) |        6 (10.0%) |

#### Fine-Tuned Models - ERC1155

| Model                    | Total Comp. | Weaker (≤) | Stronger (≥) | Equivalent (≡) | Not Comp. (\|\|) |
| :----------------------- | ----------: | ---------: | -----------: | -------------: | ---------------: |
| erc-20-001-5-16          |          60 |   2 (3.3%) |     1 (1.7%) |       3 (5.0%) |       54 (90.0%) |
| erc-721-001-5-16         |          60 |  6 (10.0%) |     3 (5.0%) |      9 (15.0%) |       42 (70.0%) |
| erc-1155-001-5-16        |          60 |   3 (5.0%) |     1 (1.7%) |       2 (3.3%) |       54 (90.0%) |
| erc-20-721-001-5-16      |          60 |   0 (0.0%) |     0 (0.0%) |       0 (0.0%) |      60 (100.0%) |
| erc-20-1155-001-5-16     |          60 | 16 (26.7%) |    7 (11.7%) |     19 (31.7%) |       18 (30.0%) |
| erc-721-1155-001-5-16    |          60 | 19 (31.7%) |    9 (15.0%) |     26 (43.3%) |        6 (10.0%) |
| erc-20-721-1155-001-5-16 |          60 |  6 (10.0%) |     2 (3.3%) |       4 (6.7%) |       48 (80.0%) |

--- Stronger Specification Occurrences (Pointers for Manual Review) ---
The following are instances where the LLM-generated specification was found to be stronger than the reference.
To view the actual LLM-generated specification text, you need to trace back to the original raw LLM output/
thread files (e.g., from 'experiments/threads...') that were used as input to 'refinement*verifier.py' for the corresponding run.
The 'Annotated Contract CSV' column below points to the CSV file containing the full contract source with the LLM-generated annotations for the specific run.\n
| Mode | Category | Identifier | Standard | Token Ctx | Run ID | Function | Annotated Contract CSV |
|:---|:---|:---|:---|:---|:---|:---|:---|
| entire_contract | base_models | erc20_erc721 | erc20 | erc20_erc721 | 1 | transfer_post | experiments/results_entire_contract_base_full_context/4o-mini/erc20/erc20_erc721/erc20*[erc20_erc721].csv |
| entire*contract | fine_tuning_models | erc-20-001-5-16 | erc20 | none | 5 | approve_post | experiments/results_entire_contract_fine_tuning/erc-20-001-5-16/erc20/none/erc20*[none].csv |
| entire*contract | fine_tuning_models | erc-20-001-5-16 | erc20 | none | 5 | transfer_post | experiments/results_entire_contract_fine_tuning/erc-20-001-5-16/erc20/none/erc20*[none].csv |
| entire*contract | fine_tuning_models | erc-20-001-5-16 | erc20 | none | 6 | approve_post | experiments/results_entire_contract_fine_tuning/erc-20-001-5-16/erc20/none/erc20*[none].csv |
| entire*contract | fine_tuning_models | erc-20-001-5-16 | erc20 | none | 6 | transfer_post | experiments/results_entire_contract_fine_tuning/erc-20-001-5-16/erc20/none/erc20*[none].csv |
| entire*contract | fine_tuning_models | erc-20-1155-001-5-16 | erc20 | none | 9 | transfer_post | experiments/results_entire_contract_fine_tuning/erc-20-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | base_models | none | erc20 | none | 1 | approve_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/none/erc20*[none].csv |
| func*by_func | base_models | none | erc20 | none | 2 | approve_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/none/erc20*[none].csv |
| func*by_func | base_models | none | erc20 | none | 3 | approve_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/none/erc20*[none].csv |
| func*by_func | base_models | none | erc20 | none | 4 | approve_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/none/erc20*[none].csv |
| func*by_func | base_models | none | erc20 | none | 5 | approve_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/none/erc20*[none].csv |
| func*by_func | base_models | none | erc20 | none | 6 | approve_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/none/erc20*[none].csv |
| func*by_func | base_models | none | erc20 | none | 7 | approve_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/none/erc20*[none].csv |
| func*by_func | base_models | none | erc20 | none | 8 | approve_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/none/erc20*[none].csv |
| func*by_func | base_models | none | erc20 | none | 9 | approve_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/none/erc20*[none].csv |
| func*by_func | base_models | none | erc20 | none | 10 | approve_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/none/erc20*[none].csv |
| func*by_func | base_models | erc721 | erc20 | erc721 | 2 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/erc721/erc20*[erc721].csv |
| func*by_func | base_models | erc721 | erc20 | erc721 | 3 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/erc721/erc20*[erc721].csv |
| func*by_func | base_models | erc721 | erc20 | erc721 | 4 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/erc721/erc20*[erc721].csv |
| func*by_func | base_models | erc721 | erc20 | erc721 | 6 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/erc721/erc20*[erc721].csv |
| func*by_func | base_models | erc1155 | erc20 | erc1155 | 2 | approve_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/erc1155/erc20*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc20 | erc1155 | 6 | approve_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/erc1155/erc20*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc20 | erc1155 | 7 | approve_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/erc1155/erc20*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc20 | erc1155 | 9 | approve_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/erc1155/erc20*[erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc20 | erc20_erc1155 | 2 | transfer_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/erc20_erc1155/erc20*[erc20_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc20 | erc721_erc1155 | 1 | allowance_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/erc721_erc1155/erc20*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc20 | erc721_erc1155 | 3 | allowance_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/erc721_erc1155/erc20*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc20 | erc721_erc1155 | 4 | allowance_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/erc721_erc1155/erc20*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc20 | erc721_erc1155 | 6 | allowance_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/erc721_erc1155/erc20*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc20 | erc721_erc1155 | 8 | allowance_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/erc721_erc1155/erc20*[erc721_erc1155].csv |
| func*by_func | base_models | erc20_erc721_erc1155 | erc20 | erc20_erc721_erc1155 | 1 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/erc20_erc721_erc1155/erc20*[erc20_erc721_erc1155].csv |
| func*by_func | base_models | erc20_erc721_erc1155 | erc20 | erc20_erc721_erc1155 | 8 | approve_post | experiments/results_func_by_func_base_full_context/4o-mini/erc20/erc20_erc721_erc1155/erc20*[erc20_erc721_erc1155].csv |
| func*by_func | fine_tuning_models | erc-20-001-5-16 | erc20 | none | 3 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-001-5-16 | erc20 | none | 4 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-001-5-16 | erc20 | none | 5 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-001-5-16 | erc20 | none | 7 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-721-001-5-16 | erc20 | none | 1 | approve_post | experiments/results_func_by_func_fine_tuning/erc-721-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-721-001-5-16 | erc20 | none | 2 | approve_post | experiments/results_func_by_func_fine_tuning/erc-721-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-721-001-5-16 | erc20 | none | 3 | approve_post | experiments/results_func_by_func_fine_tuning/erc-721-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-721-001-5-16 | erc20 | none | 4 | approve_post | experiments/results_func_by_func_fine_tuning/erc-721-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-721-001-5-16 | erc20 | none | 5 | approve_post | experiments/results_func_by_func_fine_tuning/erc-721-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-721-001-5-16 | erc20 | none | 6 | approve_post | experiments/results_func_by_func_fine_tuning/erc-721-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-721-001-5-16 | erc20 | none | 7 | approve_post | experiments/results_func_by_func_fine_tuning/erc-721-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-721-001-5-16 | erc20 | none | 8 | approve_post | experiments/results_func_by_func_fine_tuning/erc-721-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-721-001-5-16 | erc20 | none | 9 | approve_post | experiments/results_func_by_func_fine_tuning/erc-721-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-721-001-5-16 | erc20 | none | 10 | approve_post | experiments/results_func_by_func_fine_tuning/erc-721-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-1155-001-5-16 | erc20 | none | 3 | approve_post | experiments/results_func_by_func_fine_tuning/erc-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-1155-001-5-16 | erc20 | none | 7 | approve_post | experiments/results_func_by_func_fine_tuning/erc-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-1155-001-5-16 | erc20 | none | 10 | approve_post | experiments/results_func_by_func_fine_tuning/erc-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-001-5-16 | erc20 | none | 2 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-721-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-001-5-16 | erc20 | none | 3 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-721-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-001-5-16 | erc20 | none | 4 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-721-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-001-5-16 | erc20 | none | 5 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-721-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-001-5-16 | erc20 | none | 6 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-721-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-001-5-16 | erc20 | none | 7 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-721-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-001-5-16 | erc20 | none | 10 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-721-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-1155-001-5-16 | erc20 | none | 1 | allowance_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-1155-001-5-16 | erc20 | none | 2 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-1155-001-5-16 | erc20 | none | 5 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-1155-001-5-16 | erc20 | none | 6 | allowance_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-1155-001-5-16 | erc20 | none | 6 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-1155-001-5-16 | erc20 | none | 9 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-1155-001-5-16 | erc20 | none | 10 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc20 | none | 2 | allowance_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc20 | none | 3 | allowance_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc20 | none | 3 | approve_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc20 | none | 4 | allowance_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc20 | none | 10 | allowance_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-1155-001-5-16 | erc20 | none | 2 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-721-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-1155-001-5-16 | erc20 | none | 4 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-721-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-1155-001-5-16 | erc20 | none | 5 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-721-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-1155-001-5-16 | erc20 | none | 6 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-721-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-1155-001-5-16 | erc20 | none | 8 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-721-1155-001-5-16/erc20/none/erc20*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-1155-001-5-16 | erc20 | none | 10 | approve_post | experiments/results_func_by_func_fine_tuning/erc-20-721-1155-001-5-16/erc20/none/erc20*[none].csv |
| entire*contract | base_models | erc1155 | erc721 | erc1155 | 1 | balanceOf_post | experiments/results_entire_contract_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| entire*contract | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 3 | balanceOf_post | experiments/results_entire_contract_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| entire*contract | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 9 | safeTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| entire*contract | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 9 | transferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| entire*contract | fine_tuning_models | erc-20-001-5-16 | erc721 | none | 7 | balanceOf_post | experiments/results_entire_contract_fine_tuning/erc-20-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | base_models | none | erc721 | none | 1 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/none/erc721*[none].csv |
| func*by_func | base_models | none | erc721 | none | 2 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/none/erc721*[none].csv |
| func*by_func | base_models | none | erc721 | none | 3 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/none/erc721*[none].csv |
| func*by_func | base_models | none | erc721 | none | 4 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/none/erc721*[none].csv |
| func*by_func | base_models | none | erc721 | none | 5 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/none/erc721*[none].csv |
| func*by_func | base_models | none | erc721 | none | 6 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/none/erc721*[none].csv |
| func*by_func | base_models | none | erc721 | none | 7 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/none/erc721*[none].csv |
| func*by_func | base_models | none | erc721 | none | 8 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/none/erc721*[none].csv |
| func*by_func | base_models | none | erc721 | none | 9 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/none/erc721*[none].csv |
| func*by_func | base_models | none | erc721 | none | 10 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/none/erc721*[none].csv |
| func*by_func | base_models | erc20 | erc721 | erc20 | 3 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20/erc721*[erc20].csv |
| func*by_func | base_models | erc20 | erc721 | erc20 | 7 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20/erc721*[erc20].csv |
| func*by_func | base_models | erc721 | erc721 | erc721 | 1 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721/erc721*[erc721].csv |
| func*by_func | base_models | erc721 | erc721 | erc721 | 2 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721/erc721*[erc721].csv |
| func*by_func | base_models | erc721 | erc721 | erc721 | 3 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721/erc721*[erc721].csv |
| func*by_func | base_models | erc721 | erc721 | erc721 | 4 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721/erc721*[erc721].csv |
| func*by_func | base_models | erc721 | erc721 | erc721 | 4 | setApprovalForAll_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721/erc721*[erc721].csv |
| func*by_func | base_models | erc721 | erc721 | erc721 | 5 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721/erc721*[erc721].csv |
| func*by_func | base_models | erc721 | erc721 | erc721 | 5 | setApprovalForAll_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721/erc721*[erc721].csv |
| func*by_func | base_models | erc721 | erc721 | erc721 | 6 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721/erc721*[erc721].csv |
| func*by_func | base_models | erc721 | erc721 | erc721 | 6 | setApprovalForAll_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721/erc721*[erc721].csv |
| func*by_func | base_models | erc721 | erc721 | erc721 | 7 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721/erc721*[erc721].csv |
| func*by_func | base_models | erc721 | erc721 | erc721 | 7 | setApprovalForAll_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721/erc721*[erc721].csv |
| func*by_func | base_models | erc721 | erc721 | erc721 | 8 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721/erc721*[erc721].csv |
| func*by_func | base_models | erc721 | erc721 | erc721 | 9 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721/erc721*[erc721].csv |
| func*by_func | base_models | erc721 | erc721 | erc721 | 9 | setApprovalForAll_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721/erc721*[erc721].csv |
| func*by_func | base_models | erc721 | erc721 | erc721 | 10 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721/erc721*[erc721].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 1 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 1 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 2 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 2 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 3 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 4 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 4 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 5 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 5 | setApprovalForAll_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 5 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 6 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 6 | setApprovalForAll_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 6 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 7 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 7 | setApprovalForAll_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 7 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 8 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 8 | setApprovalForAll_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 8 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 9 | setApprovalForAll_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 9 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 10 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc721 | erc1155 | 10 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc1155/erc721*[erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 1 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 1 | setApprovalForAll_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 1 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 2 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 2 | setApprovalForAll_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 2 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 3 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 4 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 4 | setApprovalForAll_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 4 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 5 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 5 | isApprovedForAll_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 5 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 6 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 6 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 7 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 7 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 8 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 8 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 9 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc721 | erc20_erc1155 | 10 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc1155/erc721*[erc20_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 1 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 1 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 2 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 3 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 3 | safeTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 3 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 4 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 4 | safeTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 4 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 5 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 5 | safeTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 5 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 6 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 6 | safeTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 6 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 7 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 7 | safeTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 7 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 8 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 9 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 9 | safeTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 9 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 10 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc721 | erc721_erc1155 | 10 | transferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc721_erc1155/erc721*[erc721_erc1155].csv |
| func*by_func | base_models | erc20_erc721_erc1155 | erc721 | erc20_erc721_erc1155 | 1 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc721_erc1155/erc721*[erc20_erc721_erc1155].csv |
| func*by_func | base_models | erc20_erc721_erc1155 | erc721 | erc20_erc721_erc1155 | 4 | isApprovedForAll_post | experiments/results_func_by_func_base_full_context/4o-mini/erc721/erc20_erc721_erc1155/erc721*[erc20_erc721_erc1155].csv |
| func*by_func | fine_tuning_models | erc-721-001-5-16 | erc721 | none | 4 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-721-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-1155-001-5-16 | erc721 | none | 3 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-1155-001-5-16 | erc721 | none | 5 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-1155-001-5-16 | erc721 | none | 8 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-1155-001-5-16 | erc721 | none | 9 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-1155-001-5-16 | erc721 | none | 10 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-001-5-16 | erc721 | none | 1 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-20-721-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-001-5-16 | erc721 | none | 3 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-20-721-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-001-5-16 | erc721 | none | 4 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-20-721-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-001-5-16 | erc721 | none | 5 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-20-721-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-001-5-16 | erc721 | none | 6 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-20-721-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-001-5-16 | erc721 | none | 7 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-20-721-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-001-5-16 | erc721 | none | 8 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-20-721-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-001-5-16 | erc721 | none | 9 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-20-721-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-20-1155-001-5-16 | erc721 | none | 1 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-20-1155-001-5-16 | erc721 | none | 5 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-20-1155-001-5-16 | erc721 | none | 7 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-20-1155-001-5-16 | erc721 | none | 10 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc721 | none | 1 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc721 | none | 2 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc721 | none | 3 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc721 | none | 3 | isApprovedForAll_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc721 | none | 4 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc721 | none | 4 | isApprovedForAll_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc721 | none | 5 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc721 | none | 6 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc721 | none | 6 | isApprovedForAll_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc721 | none | 7 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc721 | none | 8 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc721 | none | 9 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc721 | none | 9 | isApprovedForAll_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc721 | none | 10 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc721/none/erc721*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-1155-001-5-16 | erc721 | none | 3 | balanceOf_post | experiments/results_func_by_func_fine_tuning/erc-20-721-1155-001-5-16/erc721/none/erc721*[none].csv |
| entire*contract | base_models | erc721 | erc1155 | erc721 | 5 | balanceOf_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721/erc1155*[erc721].csv |
| entire*contract | base_models | erc721 | erc1155 | erc721 | 5 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721/erc1155*[erc721].csv |
| entire*contract | base_models | erc1155 | erc1155 | erc1155 | 3 | balanceOf_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| entire*contract | base_models | erc1155 | erc1155 | erc1155 | 3 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| entire*contract | base_models | erc1155 | erc1155 | erc1155 | 4 | balanceOf_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| entire*contract | base_models | erc1155 | erc1155 | erc1155 | 4 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| entire*contract | base_models | erc1155 | erc1155 | erc1155 | 5 | balanceOf_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| entire*contract | base_models | erc1155 | erc1155 | erc1155 | 5 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| entire*contract | base_models | erc1155 | erc1155 | erc1155 | 6 | balanceOf_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| entire*contract | base_models | erc1155 | erc1155 | erc1155 | 6 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| entire*contract | base_models | erc1155 | erc1155 | erc1155 | 7 | balanceOf_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| entire*contract | base_models | erc1155 | erc1155 | erc1155 | 7 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| entire*contract | base_models | erc1155 | erc1155 | erc1155 | 8 | balanceOf_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| entire*contract | base_models | erc1155 | erc1155 | erc1155 | 8 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| entire*contract | base_models | erc1155 | erc1155 | erc1155 | 9 | balanceOf_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| entire*contract | base_models | erc1155 | erc1155 | erc1155 | 9 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| entire*contract | base_models | erc1155 | erc1155 | erc1155 | 10 | balanceOf_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| entire*contract | base_models | erc1155 | erc1155 | erc1155 | 10 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| entire*contract | base_models | erc20_erc721 | erc1155 | erc20_erc721 | 9 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc721/erc1155*[erc20_erc721].csv |
| entire*contract | base_models | erc20_erc1155 | erc1155 | erc20_erc1155 | 2 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155*[erc20_erc1155].csv |
| entire*contract | base_models | erc20_erc1155 | erc1155 | erc20_erc1155 | 5 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155*[erc20_erc1155].csv |
| entire*contract | base_models | erc20_erc1155 | erc1155 | erc20_erc1155 | 7 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155*[erc20_erc1155].csv |
| entire*contract | base_models | erc20_erc1155 | erc1155 | erc20_erc1155 | 8 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155*[erc20_erc1155].csv |
| entire*contract | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 1 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| entire*contract | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 2 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| entire*contract | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 3 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| entire*contract | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 4 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| entire*contract | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 5 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| entire*contract | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 6 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| entire*contract | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 7 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| entire*contract | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 8 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| entire*contract | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 9 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| entire*contract | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 10 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| entire*contract | base_models | erc20_erc721_erc1155 | erc1155 | erc20_erc721_erc1155 | 1 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155*[erc20_erc721_erc1155].csv |
| entire*contract | base_models | erc20_erc721_erc1155 | erc1155 | erc20_erc721_erc1155 | 2 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155*[erc20_erc721_erc1155].csv |
| entire*contract | base_models | erc20_erc721_erc1155 | erc1155 | erc20_erc721_erc1155 | 3 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155*[erc20_erc721_erc1155].csv |
| entire*contract | base_models | erc20_erc721_erc1155 | erc1155 | erc20_erc721_erc1155 | 4 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155*[erc20_erc721_erc1155].csv |
| entire*contract | base_models | erc20_erc721_erc1155 | erc1155 | erc20_erc721_erc1155 | 5 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155*[erc20_erc721_erc1155].csv |
| entire*contract | base_models | erc20_erc721_erc1155 | erc1155 | erc20_erc721_erc1155 | 6 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155*[erc20_erc721_erc1155].csv |
| entire*contract | base_models | erc20_erc721_erc1155 | erc1155 | erc20_erc721_erc1155 | 8 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155*[erc20_erc721_erc1155].csv |
| entire*contract | base_models | erc20_erc721_erc1155 | erc1155 | erc20_erc721_erc1155 | 9 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155*[erc20_erc721_erc1155].csv |
| entire*contract | base_models | erc20_erc721_erc1155 | erc1155 | erc20_erc721_erc1155 | 10 | safeBatchTransferFrom_post | experiments/results_entire_contract_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155*[erc20_erc721_erc1155].csv |
| entire*contract | fine_tuning_models | erc-721-001-5-16 | erc1155 | none | 5 | safeBatchTransferFrom_post | experiments/results_entire_contract_fine_tuning/erc-721-001-5-16/erc1155/none/erc1155*[none].csv |
| entire*contract | fine_tuning_models | erc-1155-001-5-16 | erc1155 | none | 1 | safeBatchTransferFrom_post | experiments/results_entire_contract_fine_tuning/erc-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| entire*contract | fine_tuning_models | erc-1155-001-5-16 | erc1155 | none | 2 | safeBatchTransferFrom_post | experiments/results_entire_contract_fine_tuning/erc-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| entire*contract | fine_tuning_models | erc-1155-001-5-16 | erc1155 | none | 7 | safeBatchTransferFrom_post | experiments/results_entire_contract_fine_tuning/erc-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| entire*contract | fine_tuning_models | erc-721-1155-001-5-16 | erc1155 | none | 2 | safeBatchTransferFrom_post | experiments/results_entire_contract_fine_tuning/erc-721-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| entire*contract | fine_tuning_models | erc-20-721-1155-001-5-16 | erc1155 | none | 3 | safeBatchTransferFrom_post | experiments/results_entire_contract_fine_tuning/erc-20-721-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | base_models | erc721 | erc1155 | erc721 | 2 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721/erc1155*[erc721].csv |
| func*by_func | base_models | erc721 | erc1155 | erc721 | 5 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721/erc1155*[erc721].csv |
| func*by_func | base_models | erc1155 | erc1155 | erc1155 | 1 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc1155 | erc1155 | 2 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc1155 | erc1155 | 3 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc1155 | erc1155 | 4 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc1155 | erc1155 | 5 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc1155 | erc1155 | 6 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc1155 | erc1155 | 7 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc1155 | erc1155 | 8 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc1155 | erc1155 | 9 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| func*by_func | base_models | erc1155 | erc1155 | erc1155 | 10 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc1155/erc1155*[erc1155].csv |
| func*by_func | base_models | erc20_erc721 | erc1155 | erc20_erc721 | 1 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721/erc1155*[erc20_erc721].csv |
| func*by_func | base_models | erc20_erc721 | erc1155 | erc20_erc721 | 3 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721/erc1155*[erc20_erc721].csv |
| func*by_func | base_models | erc20_erc721 | erc1155 | erc20_erc721 | 7 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721/erc1155*[erc20_erc721].csv |
| func*by_func | base_models | erc20_erc1155 | erc1155 | erc20_erc1155 | 1 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc1155 | erc20_erc1155 | 2 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc1155 | erc20_erc1155 | 3 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc1155 | erc20_erc1155 | 4 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc1155 | erc20_erc1155 | 5 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc1155 | erc20_erc1155 | 6 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc1155 | erc20_erc1155 | 8 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc1155 | erc20_erc1155 | 9 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155*[erc20_erc1155].csv |
| func*by_func | base_models | erc20_erc1155 | erc1155 | erc20_erc1155 | 10 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc1155/erc1155*[erc20_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 1 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 2 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 3 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 4 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 5 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 6 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 7 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 8 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 9 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 10 | balanceOf_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| func*by_func | base_models | erc721_erc1155 | erc1155 | erc721_erc1155 | 10 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc721_erc1155/erc1155*[erc721_erc1155].csv |
| func*by_func | base_models | erc20_erc721_erc1155 | erc1155 | erc20_erc721_erc1155 | 1 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155*[erc20_erc721_erc1155].csv |
| func*by_func | base_models | erc20_erc721_erc1155 | erc1155 | erc20_erc721_erc1155 | 2 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155*[erc20_erc721_erc1155].csv |
| func*by_func | base_models | erc20_erc721_erc1155 | erc1155 | erc20_erc721_erc1155 | 3 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155*[erc20_erc721_erc1155].csv |
| func*by_func | base_models | erc20_erc721_erc1155 | erc1155 | erc20_erc721_erc1155 | 4 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155*[erc20_erc721_erc1155].csv |
| func*by_func | base_models | erc20_erc721_erc1155 | erc1155 | erc20_erc721_erc1155 | 5 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155*[erc20_erc721_erc1155].csv |
| func*by_func | base_models | erc20_erc721_erc1155 | erc1155 | erc20_erc721_erc1155 | 6 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155*[erc20_erc721_erc1155].csv |
| func*by_func | base_models | erc20_erc721_erc1155 | erc1155 | erc20_erc721_erc1155 | 7 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155*[erc20_erc721_erc1155].csv |
| func*by_func | base_models | erc20_erc721_erc1155 | erc1155 | erc20_erc721_erc1155 | 8 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155*[erc20_erc721_erc1155].csv |
| func*by_func | base_models | erc20_erc721_erc1155 | erc1155 | erc20_erc721_erc1155 | 10 | safeBatchTransferFrom_post | experiments/results_func_by_func_base_full_context/4o-mini/erc1155/erc20_erc721_erc1155/erc1155*[erc20_erc721_erc1155].csv |
| func*by_func | fine_tuning_models | erc-20-001-5-16 | erc1155 | none | 8 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-20-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-721-001-5-16 | erc1155 | none | 2 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-721-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-721-001-5-16 | erc1155 | none | 9 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-721-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-721-001-5-16 | erc1155 | none | 10 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-721-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-1155-001-5-16 | erc1155 | none | 2 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-20-1155-001-5-16 | erc1155 | none | 1 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-20-1155-001-5-16 | erc1155 | none | 2 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-20-1155-001-5-16 | erc1155 | none | 3 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-20-1155-001-5-16 | erc1155 | none | 4 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-20-1155-001-5-16 | erc1155 | none | 7 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-20-1155-001-5-16 | erc1155 | none | 8 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-20-1155-001-5-16 | erc1155 | none | 9 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-20-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc1155 | none | 1 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc1155 | none | 2 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc1155 | none | 3 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc1155 | none | 4 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc1155 | none | 6 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc1155 | none | 7 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc1155 | none | 8 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc1155 | none | 9 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-721-1155-001-5-16 | erc1155 | none | 10 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-721-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-1155-001-5-16 | erc1155 | none | 3 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-20-721-1155-001-5-16/erc1155/none/erc1155*[none].csv |
| func*by_func | fine_tuning_models | erc-20-721-1155-001-5-16 | erc1155 | none | 5 | safeBatchTransferFrom_post | experiments/results_func_by_func_fine_tuning/erc-20-721-1155-001-5-16/erc1155/none/erc1155*[none].csv |
