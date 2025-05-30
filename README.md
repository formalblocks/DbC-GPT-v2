# Extracting Formal Smart-Contract Specifications from Natural Language with LLMs

This repository contains the implementation and experiments for the paper "Extracting formal smart-contract specifications from natural language with LLMs". The project leverages Large Language Models (LLMs), particularly ChatGPT, to automatically infer formal postcondition specifications for smart contract functions implemented in Solidity.

## Introduction

Developers often hesitate to provide formal specifications for software components, even well-established design-by-contract (DbC) properties like invariants, pre- and postconditions are neglected. This project employs state-of-the-art Natural Language (NL) processing technologies using LLMs to automatically infer formal specifications from component textual behavioral descriptions.

We implemented a framework, DbC-GPT, which generates postcondition specifications for smart contract functions implemented in Solidity. The framework uses the solc-verify tool to check the syntax and verify the reference implementation's conformance to the generated specifications.

## Project Structure

```
.
├── .devcontainer
├── .vscode
├── assets
│   ├── file_search
│   ├── fine-tuning
│   └── solc_verify_examples
├── experiments
│   ├── loop_contract_verifier.py
│   ├── func_by_func_verifier.py
│   ├── results_entire_contract_base_full_context
│   ├── results_func_by_func_base_full_context
│   ├── context_comparison_report
│   └── outputs
├── solc_verify_generator
│   ├── ERC1155
│   │   ├── imp
│   │   └── templates
│   ├── ERC20
│   │   ├── imp
│   │   │   └── math
│   │   └── templates
│   ├── ERC721
│   │   ├── imp
│   │   └── templates
│   └── __pycache__
└── temp
```

- `experiments/loop_contract_verifier.py`: Script for running full-contract iterative verification experiments.
- `experiments/func_by_func_verifier.py`: Script for running function-by-function verification experiments.
- `experiments/results_entire_contract_base_full_context/`: Results from full-contract verification runs, organized by assistant, contract, and context.
- `experiments/results_func_by_func_base_full_context/`: Results from function-by-function verification runs, organized similarly.
- `experiments/context_comparison_report/`: Contains generated markdown tables and heatmaps comparing context performance.
- `.env`: Environment variables (to be created by the user).
- `requirements.txt`: List of dependencies.

## Setup

1. **Clone the repository:**
    ```bash
    git clone https://github.com/formalblocks/DbC-GPT.git
    cd DbC-GPT
    ```

2. **Create and activate a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate 
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**
Create a .env file in the root directory and add your OpenAI API key.

    ```bash
    OPENAI_API_KEY=your_openai_api_key
    ```

# Smart Contract Verification Experiments

## Overview

This repository contains tools and results for analyzing the verification status of smart contracts. The analysis focuses on examining how well different contract types (ERC20, ERC721, ERC1155) can be formally verified, both at the contract and function level, and how different context combinations affect verification success.

## Running Experiments

### 1. Full-Contract Verification

Run the iterative, contract-level verification process with:

```bash
python experiments/loop_contract_verifier.py --assistant 4o-mini --requested erc1155 --context all
```

- `--assistant`: The assistant/model to use (e.g., 4o-mini).
- `--requested`: The contract type to verify (erc20, erc721, erc1155).
- `--context`: Comma-separated list of context contract types (e.g., "erc20,erc721,erc1155" or "all").
- `--runs`: Number of verification runs (default: 10).
- `--max-iterations`: Maximum number of iterations per run (default: 10).

Results are saved in `experiments/results_entire_contract_base_full_context/`.

### 2. Function-by-Function Verification

Run the function-by-function verification process with:

```bash
python experiments/func_by_func_verifier.py --assistant 4o-mini --requested erc1155 --context all
```

- Same arguments as above.
- Results are saved in `experiments/results_func_by_func_base_full_context/`.

## Analyzing Results

### Context Comparison

After running experiments, generate a markdown summary table (and, for function-by-function, a heatmap) comparing context combinations:

```bash
python compare_contexts.py --mode entire_contract --contract erc1155
python compare_contexts.py --mode func_by_func --contract erc1155
```

- `--mode`: `entire_contract` for full-contract analysis, `func_by_func` for function-level analysis.
- `--contract`: Contract type to analyze (erc20, erc721, erc1155).

The script will output:

- A markdown table summarizing verification rates, average iterations, and other metrics for each context combination.
- For function-by-function mode, a heatmap image showing per-function verification rates across contexts.

Reports are saved in `experiments/context_comparison_report/entire_contract/<contract>/` and `experiments/context_comparison_report/func_by_func/<contract>/`.

## Data Sources

The analysis is based on verification result data from experimental runs located in:

- `experiments/results_entire_contract_base_full_context/`
- `experiments/results_func_by_func_base_full_context/`

These directories contain CSV files with verification results for different smart contract types and context combinations.

## Visualization Types

- **Markdown Tables**: Summarize verification rates, average time, iterations, and more for each context.
- **Heatmaps** (function-by-function mode): Show per-function verification rates across context combinations.

## Understanding the Results

- **Verification Rate**: Percentage of runs where the contract (or all functions) was fully verified.
- **Average Time**: Average time taken for verification attempts.
- **Average Iterations**: Average number of iterations needed.
- **Min/Max Iterations**: Minimum/maximum number of iterations to achieve a successful verification.
- **Function Verification Rates**: (func_by_func mode) Success rate for each individual function across contexts.

## Sample Report

A complete report is generated in Markdown format with embedded images at `experiments/context_comparison_report/`.

---

For more details on the methodology and findings, please see the full paper and the generated reports in the `context_comparison_report` directory.

# Assistant Performance Comparison Tool

This tool analyzes the performance of different assistants in verifying smart contracts using the results generated by `func_by_func_verifier.py`.

## Requirements

```
pip install pandas matplotlib seaborn
```

## Usage

Simply run the script and it will:
1. Find all result files in the `results_*` directories
2. Analyze the performance metrics
3. Generate visualizations and comparison tables
4. Create a comprehensive report in the `assistant_comparison_report` directory

```bash
python compare_assistants.py
```

## Output

The script generates several visualizations:

1. **Summary Table**: A CSV and HTML table with detailed metrics for each assistant
2. **Verification Rate Bar Chart**: Overall performance of each assistant
3. **Parameter-Specific Plots**: Box plots showing verification rates by:
   - Learning rate
   - Number of epochs
   - Batch size
4. **Heatmaps**: Visualization of verification rates across learning rates and epochs for each batch size
5. **Function-Level Verification**: Heatmap showing which functions are successfully verified by which assistants

## Understanding the Results

- **Verification Rate**: Percentage of runs where the contract was fully verified
- **Average Time**: Average time taken for verification attempts
- **Average Iterations**: Average number of iterations needed
- **Function Verification Rates**: Success rate for each individual function

The hyperparameter analysis (learning rate, epochs, batch size) helps identify the optimal configuration for training.

## Sample Report

A complete report is generated in Markdown format with embedded images at `assistant_comparison_report/report.md`.