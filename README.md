# DbC-GPT-v2: Extracting Formal Smart-Contract Specifications from Natural Language with LLMs

This repository contains a comprehensive research project that leverages Large Language Models (LLMs), particularly ChatGPT, to automatically generate formal postcondition specifications for smart contract functions implemented in Solidity. The project addresses a critical gap in software development where developers often neglect to provide formal specifications for their code.

## Project Overview

**DbC-GPT** (Design-by-Contract GPT) is a framework that automatically infers formal specifications from natural language descriptions of smart contract behavior. The system focuses on three major Ethereum token standards:

- **ERC-20**: Fungible tokens
- **ERC-721**: Non-fungible tokens (NFTs) 
- **ERC-1155**: Multi-token standard

## Key Components

### 1. **Verification Systems**
- `experiments/loop_contract_verifier.py`: Full-contract iterative verification
- `experiments/func_by_func_verifier.py`: Function-by-function verification

### 2. **Smart Contract Templates**
The `experiments/solc_verify_generator/` contains:
- Contract implementations for ERC-20, ERC-721, and ERC-1155
- Specification templates
- Integration with solc-verify tool for formal verification

### 3. **Analysis and Comparison Tools**
- `compare_assistants.py`: Performance comparison across different GPT models
- `compare_contexts.py`: Context combination analysis

## Research Methodology

### **Two Verification Approaches:**

1. **Entire Contract Verification**: Generates specifications for complete smart contracts in an iterative process
2. **Function-by-Function Verification**: Processes individual functions independently for more granular analysis

### **Model Comparison:**
The project evaluates multiple approaches:
- Base GPT models (4o-mini)
- Fine-tuned models on specific ERC standards
- Context-enhanced models using multiple ERC specifications
- Hybrid approaches combining different token standards

### **Evaluation Metrics:**
- **Verification Rate**: Percentage of successful formal verifications
- **Average Iterations**: Number of refinement cycles needed
- **Processing Time**: Efficiency measurements
- **Function-Level Success**: Granular analysis of individual function verification

## Technical Architecture

### **Integration with solc-verify:**
The system uses solc-verify, a formal verification tool for Solidity, to:
- Check syntax correctness of generated specifications
- Verify conformance between implementations and specifications
- Provide feedback for iterative refinement

### **Parallel Processing:**
Both verification systems support parallel execution for efficient batch processing of multiple contracts and experimental runs.

### **Data Management:**
Comprehensive result tracking with:
- CSV output for quantitative analysis
- Detailed logging and error handling
- Visualization tools for performance comparison

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

### Assistant Performance Comparison

Analyze the performance of different assistants in verifying smart contracts:

```bash
python compare_assistants.py
```

The script generates several visualizations:

1. **Summary Table**: A CSV and HTML table with detailed metrics for each assistant
2. **Verification Rate Bar Chart**: Overall performance of each assistant
3. **Parameter-Specific Plots**: Box plots showing verification rates by:
   - Learning rate
   - Number of epochs
   - Batch size
4. **Heatmaps**: Visualization of verification rates across learning rates and epochs for each batch size
5. **Function-Level Verification**: Heatmap showing which functions are successfully verified by which assistants

## Project Structure

```
.
├── .devcontainer/
├── .gitignore
├── Dockerfile
├── README.md
├── analyse_refinement.py
├── assets/
│   └── file_search/
├── assistant_comparison_report/
├── compare_assistants.py
├── compare_contexts.py
├── data/
│   ├── analytics/
│   └── datasets/
├── experiments/
│   ├── loop_contract_verifier.py
│   ├── func_by_func_verifier.py
│   ├── results_entire_contract_base_full_context/
│   ├── results_func_by_func_base_full_context/
│   ├── solc_verify_generator/
│   └── threads_*/
├── refinement_check_results/
├── requirements.txt
└── utils/
```

## Key Features

- **Automated Specification Generation**: Converts natural language descriptions into formal postconditions
- **Multi-Standard Support**: Handles ERC-20, ERC-721, and ERC-1155 token standards
- **Iterative Refinement**: Improves specifications through feedback loops
- **Comprehensive Evaluation**: Multiple metrics and comparison methodologies
- **Reproducible Research**: Detailed experimental setup and result tracking

## Understanding the Results

- **Verification Rate**: Percentage of runs where the contract (or all functions) was fully verified
- **Average Time**: Average time taken for verification attempts
- **Average Iterations**: Average number of iterations needed
- **Min/Max Iterations**: Minimum/maximum number of iterations to achieve a successful verification
- **Function Verification Rates**: (func_by_func mode) Success rate for each individual function across contexts

## Research Impact

This project contributes to:
- **Automated Software Verification**: Reducing manual effort in formal specification writing
- **Smart Contract Security**: Improving reliability through formal verification
- **LLM Applications**: Demonstrating practical use of language models in software engineering
- **Design-by-Contract**: Promoting formal specification practices in blockchain development

The repository represents a significant advancement in applying AI to formal verification, specifically targeting the critical domain of smart contract security and correctness.

## Data Sources

The analysis is based on verification result data from experimental runs located in:

- `experiments/results_entire_contract_base_full_context/`
- `experiments/results_func_by_func_base_full_context/`

These directories contain CSV files with verification results for different smart contract types and context combinations.

## Visualization Types

- **Markdown Tables**: Summarize verification rates, average time, iterations, and more for each context.
- **Heatmaps** (function-by-function mode): Show per-function verification rates across context combinations.

---

For more details on the methodology and findings, please see the full paper and the generated reports in the `context_comparison_report` and `assistant_comparison_report` directories.