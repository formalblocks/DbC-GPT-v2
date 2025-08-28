#!/usr/bin/env python3
"""
Smart Contract Formal Verification Assistant Performance Comparison Tool

This script analyzes and compares the performance of different GPT models for generating
formal postconditions in smart contract verification. It supports two main comparison modes:
1. Basic fine-tuned model comparison 
2. Context enhancement vs fine-tuning comparison

The script can analyze both entire contract verification and function-by-function verification modes.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import glob
import datetime
import argparse
import ast
from typing import Dict, List, Optional, Tuple, Any

# Configure visualization settings for consistent, professional-looking plots
plt.style.use('ggplot')
sns.set(font_scale=1.2)
sns.set_style("whitegrid")

class AssistantComparer:
    """
    Main class for comparing assistant performance across different fine-tuned models.
    
    This class handles loading, analyzing, and visualizing performance data from
    fine-tuning experiments on smart contract verification tasks.
    """
    
    # ERC-specific function mappings
    ERC_FUNCTIONS = {
        "erc20": [
            "transfer", "transferFrom", "approve", "allowance", 
            "balanceOf", "totalSupply"
        ],
        "erc721": [
            "ownerOf", "approve", "getApproved", "setApprovalForAll", 
            "isApprovedForAll", "transferFrom", "safeTransferFrom", "balanceOf"
        ],
        "erc1155": [
            "balanceOf", "balanceOfBatch", "setApprovalForAll", 
            "isApprovedForAll", "safeTransferFrom", "safeBatchTransferFrom"
        ]
    }
    
    def __init__(self, mode: str = "entire_contract_fine_tuning"):
        """
        Initialize the assistant comparer.
        
        Args:
            mode: Analysis mode determining which data to load:
                - "entire_contract_fine_tuning": Fine-tuned models, entire contract mode
                - "entire_contract_base_full_context": Base model with context, entire contract mode  
                - "func_by_func_fine_tuning": Function-by-function fine-tuned models
                - "func_by_func_base_full_context": Function-by-function base model with context
        """
        self.mode = mode
        
        # Set the directory pattern based on the selected mode
        if mode == "func_by_func_fine_tuning":
            self.results_dir_pattern = "experiments/results_func_by_func_fine_tuning/*"
        elif mode == "func_by_func_base_full_context":
            self.results_dir_pattern = "experiments/results_func_by_func_base_full_context/*"
        elif mode == "entire_contract_fine_tuning":
            self.results_dir_pattern = "experiments/results_entire_contract_fine_tuning/*"
        elif mode == "entire_contract_base_full_context":
            self.results_dir_pattern = "experiments/results_entire_contract_base_full_context/*"
        else:
            raise ValueError("Mode must be 'entire_contract_fine_tuning', 'entire_contract_base_full_context', 'func_by_func_fine_tuning', or 'func_by_func_base_full_context'")
        
        # Data storage
        self.assistant_data: Dict[str, Any] = {}
        self.summary_df: Optional[pd.DataFrame] = None
        
    def extract_assistant_params(self, assistant_name: str) -> Dict[str, Any]:
        """
        Extract hyperparameters from assistant name.
        
        Parses assistant names to extract training parameters like learning rate,
        epochs, and batch size. Handles both base models and fine-tuned models.
        
        Args:
            assistant_name: Name of the assistant (e.g., "erc-20-001-5-16" or "4o-mini")
            
        Returns:
            Dictionary containing extracted parameters
        """
        # Handle base model case
        if assistant_name == "4o-mini":
            return {
                "model": "4o-mini",
                "erc_type": "base",
                "learning_rate": 0,
                "epochs": 0, 
                "batch_size": 0
            }
        
        # Parse fine-tuned model names (format: "erc-{type}-{lr}-{epochs}-{batch}")
        match = re.match(r"erc-(\d+)-(\d+)-(\d+)-(\d+)", assistant_name)
        if match:
            erc_type, lr_str, epochs, batch_size = match.groups()
            # Convert learning rate from string format (e.g., '001' -> 0.01)
            lr = float("0." + lr_str)
            return {
                "model": assistant_name,
                "erc_type": f"erc{erc_type}",
                "learning_rate": lr,
                "epochs": int(epochs),
                "batch_size": int(batch_size)
            }
            
        # Fallback for unrecognized formats
        return {
            "model": assistant_name,
            "erc_type": "unknown",
            "learning_rate": 0,
            "epochs": 0,
            "batch_size": 0
        }
    
    def find_results_files(self) -> List[Dict[str, str]]:
        """
        Find all results CSV files in the experiment directories.
        
        Scans the configured directory pattern for CSV files containing
        experimental results, extracting metadata from file paths.
        
        Returns:
            List of dictionaries containing file information
        """
        results_files = []
        
        for results_dir in glob.glob(self.results_dir_pattern):
            assistant_name = os.path.basename(results_dir)
            
            # Skip non-directories
            if not os.path.isdir(results_dir):
                continue
                
            # Walk through directory structure to find CSV files
            for root, _, files in os.walk(results_dir):
                for file in files:
                    filepath = None
                    
                    # Filter files based on mode
                    if "func_by_func" in self.mode:
                        # Function-by-function files are prefixed with "fbf_"
                        if file.endswith(".csv") and file.startswith("fbf_"):
                            filepath = os.path.join(root, file)
                    else:
                        # Entire contract files don't have the "fbf_" prefix
                        if file.endswith(".csv") and not file.startswith("fbf_"):
                            filepath = os.path.join(root, file)
                    
                    if filepath is not None:
                        # Extract metadata from file path structure
                        path_parts = filepath.split(os.sep)
                        results_dir_idx = path_parts.index(os.path.basename(results_dir))
                        
                        if len(path_parts) > results_dir_idx + 2:
                            requested_type = path_parts[results_dir_idx + 1]  # ERC type
                            context_type = path_parts[results_dir_idx + 2]    # Context configuration
                        else:
                            requested_type = "unknown"
                            context_type = "unknown"
                            
                        results_files.append({
                            "assistant": assistant_name,
                            "filepath": filepath,
                            "requested_type": requested_type,
                            "context_type": context_type
                        })
                        
        print(f"Found {len(results_files)} result files for {self.mode} mode")
        return results_files
    
    def load_and_analyze_data(self) -> pd.DataFrame:
        """
        Load and analyze performance data from all result files.
        
        Processes CSV files to extract verification metrics, performance statistics,
        and function-level success rates for each assistant configuration.
        
        Returns:
            DataFrame containing aggregated performance metrics
        """
        results_files = self.find_results_files()
        
        if not results_files:
            print("No result files found. Please check the directory pattern.")
            return pd.DataFrame()
        
        all_results = []
        
        for file_info in results_files:
            try:
                print(f"Processing {file_info['filepath']}")
                df = pd.read_csv(file_info["filepath"])
                
                # Debug information
                print(f"Columns in {os.path.basename(file_info['filepath'])}: {df.columns.tolist()}")
                
                # Extract assistant parameters
                params = self.extract_assistant_params(file_info["assistant"])
                
                # Validate required columns
                if "verified" not in df.columns:
                    print(f"Warning: 'verified' column not found in {file_info['filepath']}")
                    continue
                
                # Calculate basic verification metrics
                verified_count = df["verified"].sum()
                total_runs = len(df)
                verification_rate = verified_count / total_runs if total_runs > 0 else 0
                
                # Extract optional performance metrics
                avg_time = df["time_taken"].mean() if "time_taken" in df.columns else 0
                avg_iterations = df["iterations"].mean() if "iterations" in df.columns else 0
                
                # Calculate success/failure-specific metrics
                success_df = df[df["verified"] == True]
                fail_df = df[df["verified"] == False]
                
                avg_success_time = success_df["time_taken"].mean() if "time_taken" in df.columns and not success_df.empty else 0
                avg_fail_time = fail_df["time_taken"].mean() if "time_taken" in df.columns and not fail_df.empty else 0
                avg_success_iterations = success_df["iterations"].mean() if "iterations" in df.columns and not success_df.empty else 0
                avg_fail_iterations = fail_df["iterations"].mean() if "iterations" in df.columns and not fail_df.empty else 0
                
                # Analyze function-level verification rates
                function_success_rates = {}
                if "function_status" in df.columns:
                    for i, row in df.iterrows():
                        try:
                            func_status_value = row["function_status"]
                            if isinstance(func_status_value, str):
                                func_status = ast.literal_eval(func_status_value)
                            else:
                                func_status = func_status_value
                            
                            if isinstance(func_status, dict):
                                for func_name, status in func_status.items():
                                    if func_name not in function_success_rates:
                                        function_success_rates[func_name] = {"success": 0, "total": 0}
                                    
                                    function_success_rates[func_name]["total"] += 1
                                    if status == "Verified":
                                        function_success_rates[func_name]["success"] += 1
                        except Exception as e:
                            print(f"Error processing function_status in row {i}: {e}")
                            continue
                
                # Calculate function-level verification rates
                func_verification_rates = {
                    func_name: data["success"] / data["total"] 
                    for func_name, data in function_success_rates.items()
                }
                
                # Create comprehensive result entry
                result = {
                    "assistant": file_info["assistant"],
                    "requested_type": file_info["requested_type"],
                    "context_type": file_info["context_type"],
                    "verification_rate": verification_rate,
                    "verified_count": verified_count,
                    "total_runs": total_runs,
                    "avg_time": avg_time,
                    "avg_iterations": avg_iterations,
                    "avg_success_time": avg_success_time,
                    "avg_fail_time": avg_fail_time,
                    "avg_success_iterations": avg_success_iterations,
                    "avg_fail_iterations": avg_fail_iterations,
                    "function_verification_rates": func_verification_rates,
                    **params  # Include extracted hyperparameters
                }
                
                all_results.append(result)
                
            except Exception as e:
                print(f"Error processing {file_info['filepath']}: {e}")
        
        if not all_results:
            print("No results could be processed. Check the file format.")
            return pd.DataFrame()
            
        # Convert results to DataFrame
        self.summary_df = pd.DataFrame(all_results)
        print(f"Processed {len(all_results)} result files successfully")
        
        # Debug output
        if not self.summary_df.empty:
            print(f"Summary DataFrame columns: {self.summary_df.columns.tolist()}")
            print("First few rows:")
            print(self.summary_df.head())
        
        return self.summary_df
    
    def create_summary_table(self) -> pd.DataFrame:
        """
        Create a comprehensive summary table of performance metrics.
        
        Generates a pivot table showing verification rates and performance metrics
        across different assistant configurations and contexts.
        
        Returns:
            DataFrame with pivot table of metrics
        """
        if self.summary_df is None or self.summary_df.empty:
            print("No data available to create summary table")
            return pd.DataFrame()
            
        # Define columns to include in pivot table
        pivot_columns = ["verification_rate", "avg_time", "avg_iterations"]
        available_columns = [col for col in pivot_columns if col in self.summary_df.columns]
        
        if not available_columns:
            print("No metric columns available for pivot table")
            return self.summary_df
        
        try:
            # Create pivot table with assistants as rows and contexts as columns
            pivot_df = self.summary_df.pivot_table(
                index=["model", "erc_type", "learning_rate", "epochs", "batch_size"],
                columns=["requested_type", "context_type"],
                values=available_columns,
                aggfunc="mean"
            )
            
            # Flatten multi-level columns for readability
            pivot_df.columns = [f"{col[0]}_{col[1]}_{col[2]}" for col in pivot_df.columns]
            pivot_df = pivot_df.reset_index()
            
            # Calculate overall performance metrics
            overall_metrics = {col: "mean" for col in available_columns}
            
            if overall_metrics:
                overall_performance = self.summary_df.groupby(["model"]).agg(overall_metrics).reset_index()
                
                # Rename columns for clarity
                rename_dict = {
                    "verification_rate": "overall_verification_rate",
                    "avg_time": "overall_avg_time",
                    "avg_iterations": "overall_avg_iterations"
                }
                
                rename_cols = {k: v for k, v in rename_dict.items() if k in overall_performance.columns}
                if rename_cols:
                    overall_performance = overall_performance.rename(columns=rename_cols)
                
                # Merge with pivot table
                result_df = pd.merge(pivot_df, overall_performance, on="model")
            else:
                result_df = pivot_df
            
            return result_df
            
        except Exception as e:
            print(f"Error creating summary table: {e}")
            return self.summary_df
    
    def plot_verification_rates(self, output_file: str = "verification_rates.png") -> Optional[str]:
        """
        Generate bar plot of verification rates across different assistant models or contexts.
        
        Args:
            output_file: Path to save the plot
            
        Returns:
            Path to saved plot file, or None if error occurred
        """
        if self.summary_df is None or self.summary_df.empty or "verification_rate" not in self.summary_df.columns:
            print("No verification rate data available for plotting")
            return None
        
        plt.figure(figsize=(12, 8))
        
        try:
            # For base_full_context modes, group by context type
            if "base_full_context" in self.mode:
                # Calculate mean verification rate by context type
                performance_data = self.summary_df.groupby("context_type")["verification_rate"].mean().reset_index()
                performance_data = performance_data.sort_values("verification_rate", ascending=False)
                x_column = "context_type"
                x_label = "Context Type"
                title_prefix = "Overall Verification Rate by Context Type"
            else:
                # Calculate mean verification rate by model
                performance_data = self.summary_df.groupby("model")["verification_rate"].mean().reset_index()
                performance_data = performance_data.sort_values("verification_rate", ascending=False)
                x_column = "model"
                x_label = "Assistant Model"
                title_prefix = "Overall Verification Rate by Assistant Model"
            
            # Create bar plot
            ax = sns.barplot(x=x_column, y="verification_rate", data=performance_data)
            
            # Add value labels on bars
            for i, v in enumerate(performance_data["verification_rate"]):
                ax.text(i, v + 0.01, f"{v:.3f}", ha="center", va="bottom")
            
            # Determine mode display based on the new mode names
            if "func_by_func" in self.mode:
                mode_display = "Function-by-Function"
            else:
                mode_display = "Entire Contract"
            plt.title(f"{title_prefix} ({mode_display} Mode)")
            plt.xlabel(x_label)
            plt.ylabel("Verification Rate")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.savefig(output_file)
            plt.close()
            
            return output_file
            
        except Exception as e:
            print(f"Error plotting verification rates: {e}")
            return None


    
    def plot_function_verification(self, output_file: str = "function_verification.png", 
                                 requested_type: str = None) -> Optional[str]:
        """
        Generate heatmap showing function-level verification rates by assistant.
        
        Creates a heatmap where rows are function names and columns are assistant models,
        showing which functions are most successfully verified by each model.
        
        Args:
            output_file: Path to save the plot
            requested_type: ERC type to filter functions (e.g., "erc20")
            
        Returns:
            Path to saved plot file, or None if error occurred
        """
        if self.summary_df is None or self.summary_df.empty:
            print("No data available for function verification plot")
            return None
            
        try:
            # Get the ERC functions to include based on requested_type
            if requested_type and requested_type in self.ERC_FUNCTIONS:
                allowed_functions = set(self.ERC_FUNCTIONS[requested_type])
                print(f"Filtering functions for {requested_type}: {allowed_functions}")
            else:
                allowed_functions = None
                print("No ERC filtering - showing all functions")
            
            # Collect function verification data
            function_data = []
            for i, row in self.summary_df.iterrows():
                assistant = row["model"]
                context_type = row.get("context_type", "unknown")
                func_rates = row.get("function_verification_rates")
                
                if func_rates is None:
                    continue
                    
                # Parse function rates if stored as string
                if isinstance(func_rates, str):
                    try:
                        func_rates = ast.literal_eval(func_rates)
                    except:
                        print(f"Could not parse function_verification_rates in row {i}")
                        continue
                        
                # Skip empty function rates
                if not func_rates or len(func_rates) == 0:
                    continue
                    
                # Extract function verification rates
                if isinstance(func_rates, dict):
                    for func_name, rate in func_rates.items():
                        # Filter by ERC standard if specified
                        if allowed_functions is None or func_name in allowed_functions:
                            function_data.append({
                                "assistant": assistant,
                                "context_type": context_type,
                                "function": func_name,
                                "verification_rate": rate
                            })
            
            if not function_data:
                print("No function verification data collected")
                return None
                
            func_df = pd.DataFrame(function_data)
            
            # Create pivot table for heatmap
            # Special handling for func_by_func_base_full_context mode
            if self.mode == "func_by_func_base_full_context":
                # For base context mode, use context_type as columns instead of assistant
                pivot_data = func_df.pivot_table(
                    index="function",
                    columns="context_type",
                    values="verification_rate",
                    aggfunc="mean"
                )
            else:
                # For other modes, use assistant as columns
                pivot_data = func_df.pivot_table(
                    index="function",
                    columns="assistant",
                    values="verification_rate",
                    aggfunc="mean"
                )
            
            if pivot_data.empty:
                print("Pivot table for function verification is empty")
                return None
                
            plt.figure(figsize=(14, 10))
            sns.heatmap(pivot_data, annot=True, cmap="YlGnBu", fmt=".2f", linewidths=.5)
            
            # Update title to reflect ERC filtering
            # Determine mode display based on the new mode names
            if "func_by_func" in self.mode:
                mode_display = "Function-by-Function"
            else:
                mode_display = "Entire Contract"
            erc_display = f" ({requested_type.upper()} Functions)" if requested_type else ""
            
            if self.mode == "func_by_func_base_full_context":
                plt.title(f"Function-level Verification Rate by Context ({mode_display} Mode{erc_display})")
                plt.xlabel("Context Type")
            else:
                plt.title(f"Function-level Verification Rate by Assistant ({mode_display} Mode{erc_display})")
                plt.xlabel("Assistant")
            plt.ylabel("Function")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.savefig(output_file)
            plt.close()
            
            return output_file
            
        except Exception as e:
            print(f"Error plotting function verification: {e}")
            return None
    
    def create_markdown_table(self, data: pd.DataFrame, columns: List[str], 
                            index_col: Optional[str] = None, 
                            percentage_cols: Optional[List[str]] = None,
                            sort_col: Optional[str] = None, 
                            sort_ascending: bool = False, 
                            precision: int = 2) -> str:
        """
        Create a markdown-formatted table from a DataFrame.
        
        Args:
            data: DataFrame to convert
            columns: Columns to include in table
            index_col: Column to use as index
            percentage_cols: Columns to format as percentages
            sort_col: Column to sort by
            sort_ascending: Sort order
            precision: Decimal precision for numbers
            
        Returns:
            Markdown formatted table string
        """
        if percentage_cols is None:
            percentage_cols = []
            
        # Create copy to avoid modifying original
        df = data.copy()
        
        # Select and order columns
        if index_col:
            cols_to_use = [index_col] + [c for c in columns if c != index_col]
        else:
            cols_to_use = columns
            
        df = df[cols_to_use]
        
        # Sort if specified
        if sort_col and sort_col in df.columns:
            df = df.sort_values(by=sort_col, ascending=sort_ascending)
            
        # Format percentage columns
        for col in percentage_cols:
            if col in df.columns:
                df[col] = df[col].apply(lambda x: f"{x*100:.{precision}f}" if pd.notnull(x) else "")
        
        # Create markdown table
        header = "| " + " | ".join(df.columns) + " |"
        separator = "| " + " | ".join([":---" for _ in df.columns]) + " |"
        
        rows = []
        for _, row in df.iterrows():
            rows.append("| " + " | ".join([str(v) for v in row.values]) + " |")
            
        return "\n".join([header, separator] + rows)
    
    def generate_detailed_report(self, requested_type: str, output_directory: str, 
                               output_file: str = "detailed_report.md") -> Optional[str]:
        """
        Generate a comprehensive markdown report for a specific ERC type.
        
        Creates a detailed analysis including performance metrics, efficiency analysis,
        hyperparameter impacts, and recommendations.
        
        Args:
            requested_type: ERC type to analyze (e.g., "erc20")
            output_directory: Directory to save the report
            output_file: Name of the output file
            
        Returns:
            Path to generated report, or None if error occurred
        """
        if self.summary_df is None or self.summary_df.empty:
            print("No data available to generate detailed report")
            return None
        
        # Filter data for the requested type
        df = self.summary_df[self.summary_df["requested_type"] == requested_type]
        if df.empty:
            print(f"No data for requested_type {requested_type}")
            return None
        
        os.makedirs(output_directory, exist_ok=True)
        report_path = os.path.join(output_directory, output_file)
        
        try:
            total_runs = df["total_runs"].sum()
            
            # For base_full_context modes, group by context_type instead of model
            if "base_full_context" in self.mode:
                # Group by context type for base model with different contexts
                overall_performance = df.groupby("context_type").agg({
                    "verification_rate": "mean",
                    "verified_count": "sum",
                    "total_runs": "sum",
                    "avg_time": "mean",
                    "avg_iterations": "mean"
                }).reset_index()
                overall_performance = overall_performance.sort_values("verification_rate", ascending=False)
                group_column = "context_type"
                group_label = "Context Type"
            else:
                # Original behavior for fine-tuning modes
                overall_performance = df.groupby("model").agg({
                    "verification_rate": "mean",
                    "verified_count": "sum",
                    "total_runs": "sum"
                }).reset_index()
                overall_performance = overall_performance.sort_values("verification_rate", ascending=False)
                group_column = "model"
                group_label = "Model"
            
            # Calculate efficiency metrics
            if "base_full_context" in self.mode:
                # Group by context type for base model
                efficiency_df = df.groupby("context_type").agg({
                    "avg_success_iterations": "mean",
                    "avg_fail_iterations": "mean",
                    "avg_success_time": "mean",
                    "avg_fail_time": "mean",
                    "verification_rate": lambda x: 1 - x.mean()  # failure rate
                }).reset_index()
            else:
                # Original grouping by model
                efficiency_df = df.groupby("model").agg({
                    "avg_success_iterations": "mean",
                    "avg_fail_iterations": "mean",
                    "avg_success_time": "mean",
                    "avg_fail_time": "mean",
                    "verification_rate": lambda x: 1 - x.mean()  # failure rate
                }).reset_index()
            efficiency_df = efficiency_df.rename(columns={"verification_rate": "fail_rate"})
            
            # Write comprehensive markdown report
            with open(report_path, "w") as f:
                # Determine mode display based on the new mode names
                if "func_by_func" in self.mode:
                    mode_display = "Function-by-Function"
                else:
                    mode_display = "Entire Contract"
                if "base_full_context" in self.mode:
                    f.write(f"# Context Enhancement Performance Analysis for {requested_type.upper()} ({mode_display} Mode)\n\n")
                    f.write(f"This document analyzes context enhancement strategies for formal postcondition generation in smart contracts. Analysis based on {total_runs} total runs.\n\n")
                else:
                    f.write(f"# Assistant Fine-Tuning Performance Analysis for {requested_type.upper()} ({mode_display} Mode)\n\n")
                    f.write(f"This document analyzes fine-tuning experiments for formal postcondition generation in smart contracts. Analysis based on {total_runs} total runs.\n\n")
                
                # Overall Performance Section
                f.write("## Overall Performance Analysis\n\n")
                f.write("Success rates for generating postconditions that pass formal verification.\n\n")
                f.write(f"**Total Runs Analyzed:** {total_runs}\n\n")
                
                # Adjust columns based on mode
                if "base_full_context" in self.mode:
                    table_columns = ["context_type", "verification_rate", "verified_count", "total_runs", "avg_time", "avg_iterations"]
                else:
                    table_columns = ["model", "verification_rate", "verified_count", "total_runs"]
                
                overall_table = self.create_markdown_table(
                    overall_performance,
                    columns=table_columns,
                    percentage_cols=["verification_rate"],
                    sort_col="verification_rate",
                    sort_ascending=False
                )
                f.write(overall_table + "\n\n")
                
                # Key observations
                if not overall_performance.empty:
                    if "base_full_context" in self.mode:
                        best_context = overall_performance.iloc[0]["context_type"]
                        worst_context = overall_performance.iloc[-1]["context_type"]
                        avg_rate = overall_performance["verification_rate"].mean()
                        
                        f.write("**Key Observations:**\n\n")
                        f.write(f"- Best performing context: '{best_context}' with {overall_performance.iloc[0]['verification_rate']*100:.2f}% success rate\n")
                        f.write(f"- Average success rate: {avg_rate*100:.2f}%\n")
                        f.write(f"- Lowest performing context: '{worst_context}' with {overall_performance.iloc[-1]['verification_rate']*100:.2f}% success rate\n\n")
                    else:
                        best_model = overall_performance.iloc[0]["model"]
                        worst_model = overall_performance.iloc[-1]["model"]
                        avg_rate = overall_performance["verification_rate"].mean()
                        
                        f.write("**Key Observations:**\n\n")
                        f.write(f"- Best performing model: '{best_model}' with {overall_performance.iloc[0]['verification_rate']*100:.2f}% success rate\n")
                        f.write(f"- Average success rate: {avg_rate*100:.2f}%\n")
                        f.write(f"- Lowest performing model: '{worst_model}' with {overall_performance.iloc[-1]['verification_rate']*100:.2f}% success rate\n\n")
                
                f.write(f"![Overall Verification Rates](verification_rates.png)\n\n")
                
                # Efficiency Analysis
                f.write("## Efficiency Analysis\n\n")
                f.write("Analysis of iterations and time required for successful vs failed verification attempts.\n\n")
                
                # Adjust columns based on mode
                if "base_full_context" in self.mode:
                    efficiency_columns = ["context_type", "avg_fail_iterations", "avg_success_iterations", "avg_fail_time", "avg_success_time", "fail_rate"]
                else:
                    efficiency_columns = ["model", "avg_fail_iterations", "avg_success_iterations", "avg_fail_time", "avg_success_time", "fail_rate"]
                
                efficiency_table = self.create_markdown_table(
                    efficiency_df,
                    columns=efficiency_columns,
                    percentage_cols=["fail_rate"],
                    sort_col="fail_rate"
                )
                f.write(efficiency_table + "\n\n")
                
                # Function-level Analysis
                f.write("## Function-level Verification Analysis\n\n")
                f.write("Analysis of which specific smart contract functions are most successfully verified.\n\n")
                f.write("![Function Verification Rates](function_verification.png)\n\n")
                
                # Conclusions and Recommendations
                f.write("## Conclusions and Recommendations\n\n")
                
                if not overall_performance.empty:
                    if "base_full_context" in self.mode:
                        top_contexts = overall_performance.head(3)["context_type"].tolist()
                        no_context_data = overall_performance[overall_performance["context_type"] == "none"]
                        
                        f.write("**Key Findings:**\n\n")
                        f.write(f"1. Top performing contexts: {', '.join(f'`{c}`' for c in top_contexts)}\n")
                        
                        if not no_context_data.empty:
                            no_context_rate = no_context_data["verification_rate"].iloc[0] * 100
                            f.write(f"2. Base model without context: {no_context_rate:.2f}%\n")
                        
                        # Calculate improvement from context
                        if not no_context_data.empty and overall_performance.iloc[0]["verification_rate"] > 0:
                            best_rate = overall_performance.iloc[0]["verification_rate"]
                            no_ctx_rate = no_context_data["verification_rate"].iloc[0]
                            if no_ctx_rate > 0:
                                improvement = ((best_rate - no_ctx_rate) / no_ctx_rate * 100)
                                f.write(f"3. Context enhancement improvement: {improvement:.1f}% over no context\n")
                    else:
                        top_models = overall_performance.head(3)["model"].tolist()
                        baseline_data = overall_performance[overall_performance["model"] == "4o-mini"]
                        
                        f.write("**Key Findings:**\n\n")
                        f.write(f"1. Top performing models: {', '.join(f'`{m}`' for m in top_models)}\n")
                        
                        if not baseline_data.empty:
                            baseline_rate = baseline_data["verification_rate"].iloc[0] * 100
                            f.write(f"2. Baseline model (4o-mini) performance: {baseline_rate:.2f}%\n")
                        
                        f.write(f"3. Successful verifications are faster than failed attempts, indicating early success predictors\n")
                
                f.write(f"\n*Report generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
                
            print(f"Detailed report generated at {report_path}")
            return report_path
                
        except Exception as e:
            print(f"Error generating detailed report: {e}")
            return None
            
    def generate_report_for_erc(self, requested_type: str, output_directory: str) -> Optional[str]:
        """
        Generate a comprehensive report for a specific ERC type.
        
        Creates all visualizations and reports for a single ERC type,
        including summary tables, plots, and detailed analysis.
        
        Args:
            requested_type: ERC type to analyze
            output_directory: Directory to save all outputs
            
        Returns:
            Path to output directory, or None if error occurred
        """
        os.makedirs(output_directory, exist_ok=True)
        print(f"Generating report for {requested_type} in {output_directory}...")
        
        # Validate data availability
        if self.summary_df is None or self.summary_df.empty:
            print("No data available to generate report")
            return None
            
        df = self.summary_df[self.summary_df["requested_type"] == requested_type]
        if df.empty:
            print(f"No data for requested_type {requested_type}")
            return None
        
        # Generate summary table
        summary_table = self.create_summary_table()
        if not summary_table.empty:
            summary_table.to_csv(f"{output_directory}/summary_table.csv", index=False)
            
        # Generate all visualizations
        self.plot_verification_rates(f"{output_directory}/verification_rates.png")
        # Pass requested_type to filter functions
        self.plot_function_verification(f"{output_directory}/function_verification.png", requested_type)
        
        # Generate detailed report
        self.generate_detailed_report(requested_type, output_directory)
        
        # Generate simple overview report
        # Determine mode display based on the new mode names
        if "func_by_func" in self.mode:
            mode_display = "Function-by-Function"
        else:
            mode_display = "Entire Contract"
        with open(f"{output_directory}/report.md", "w") as f:
            f.write(f"# Assistant Performance Report - {requested_type.upper()} ({mode_display} Mode)\n\n")
            f.write("## Quick Overview\n\n")
            f.write("This report contains comprehensive analysis of assistant performance for smart contract verification.\n\n")
            f.write("### Contents\n\n")
            f.write("- [Detailed Analysis](detailed_report.md) - Complete performance analysis\n")
            f.write("- [Summary Table](summary_table.csv) - Raw performance metrics\n")
            f.write("- Visualization files: verification_rates.png, function_verification.png\n\n")
            f.write("### Key Visualizations\n\n")
            f.write("![Overall Performance](verification_rates.png)\n\n")
            f.write("![Function-level Analysis](function_verification.png)\n\n")
        
        print(f"Report generated in {output_directory}/")
        return output_directory


class ContextVsFinetuneComparer:
    """
    Compare fine-tuned models (no context) with base model performance across different contexts.
    
    This class analyzes whether context enhancement or fine-tuning provides better
    performance for smart contract formal verification tasks.
    """
    
    def __init__(self, evaluation_mode: str = "entire_contract"):
        """
        Initialize the context vs fine-tuning comparer.
        
        Args:
            evaluation_mode: "entire_contract" or "func_by_func"
        """
        self.evaluation_mode = evaluation_mode
        
        # Set up comparers based on evaluation mode
        if evaluation_mode == "entire_contract":
            self.fine_tuned_comparer = AssistantComparer(mode="entire_contract_fine_tuning")
            self.base_context_comparer = AssistantComparer(mode="entire_contract_base_full_context")
        elif evaluation_mode == "func_by_func":
            self.fine_tuned_comparer = AssistantComparer(mode="func_by_func_fine_tuning")
            self.base_context_comparer = AssistantComparer(mode="func_by_func_base_full_context")
        else:
            raise ValueError("evaluation_mode must be 'entire_contract' or 'func_by_func'")
        
    def load_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Load data from both fine-tuned and base context experiments.
        
        Returns:
            Tuple of (fine_tuned_data, base_context_data)
        """
        print(f"Loading fine-tuned model data for {self.evaluation_mode} mode...")
        ft_data = self.fine_tuned_comparer.load_and_analyze_data()
        
        print(f"Loading base model context data for {self.evaluation_mode} mode...")
        base_data = self.base_context_comparer.load_and_analyze_data()
        
        return ft_data, base_data
    
    def compare_no_context_models(self, ft_data: pd.DataFrame, base_data: pd.DataFrame, 
                                 requested_type: str = "erc20") -> pd.DataFrame:
        """
        Compare fine-tuned models with base model, both using no context.
        
        Args:
            ft_data: Fine-tuned model data
            base_data: Base model data
            requested_type: ERC type to analyze
            
        Returns:
            Combined DataFrame for comparison
        """
        # Filter for no-context comparisons
        ft_no_context = ft_data[
            (ft_data["requested_type"] == requested_type) & 
            (ft_data["context_type"] == "none")
        ].copy()
        
        base_no_context = base_data[
            (base_data["requested_type"] == requested_type) & 
            (base_data["context_type"] == "none") &
            (base_data["model"] == "4o-mini")
        ].copy()
        
        return pd.concat([ft_no_context, base_no_context], ignore_index=True)
    
    def analyze_base_model_contexts(self, base_data: pd.DataFrame, 
                                   requested_type: str = "erc20") -> pd.DataFrame:
        """
        Analyze base model performance across different context configurations.
        
        Args:
            base_data: Base model experiment data
            requested_type: ERC type to analyze
            
        Returns:
            DataFrame with context performance analysis
        """
        # Filter for base model and requested type
        base_filtered = base_data[
            (base_data["requested_type"] == requested_type) & 
            (base_data["model"] == "4o-mini")
        ].copy()
        
        # Aggregate performance by context type
        context_performance = base_filtered.groupby("context_type").agg({
            "verification_rate": "mean",
            "verified_count": "sum",
            "total_runs": "sum",
            "avg_time": "mean",
            "avg_iterations": "mean"
        }).reset_index()
        
        return context_performance.sort_values("verification_rate", ascending=False)
    
    def plot_context_comparison(self, context_performance: pd.DataFrame, 
                              output_file: str = "context_comparison.png") -> str:
        """
        Plot base model performance across different context types.
        
        Args:
            context_performance: Context performance data
            output_file: Output file path
            
        Returns:
            Path to saved plot
        """
        plt.figure(figsize=(12, 8))
        
        # Create bar plot with value labels
        ax = sns.barplot(x="context_type", y="verification_rate", data=context_performance)
        plt.title(f"Base Model (4o-mini) Performance by Context Type ({self.evaluation_mode.replace('_', ' ').title()} Mode)")
        plt.xlabel("Context Type")
        plt.ylabel("Verification Rate")
        plt.xticks(rotation=45, ha="right")
        
        # Add value labels on bars
        for i, v in enumerate(context_performance["verification_rate"]):
            ax.text(i, v + 0.01, f"{v:.3f}", ha="center", va="bottom")
        
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        
        return output_file
    
    def plot_finetune_vs_base_comparison(self, combined_data: pd.DataFrame, 
                                       output_file: str = "finetune_vs_base.png") -> str:
        """
        Plot comparison between fine-tuned models and base model (both no context).
        
        Args:
            combined_data: Combined comparison data
            output_file: Output file path
            
        Returns:
            Path to saved plot
        """
        plt.figure(figsize=(14, 8))
        
        # Calculate performance metrics
        model_performance = combined_data.groupby("model").agg({
            "verification_rate": "mean",
            "verified_count": "sum",
            "total_runs": "sum"
        }).reset_index()
        model_performance = model_performance.sort_values("verification_rate", ascending=False)
        
        # Color code base vs fine-tuned models
        model_performance['model_type'] = model_performance['model'].apply(
            lambda x: 'Base' if x == '4o-mini' else 'Fine-tuned'
        )
        
        # Create bar plot
        ax = sns.barplot(x="model", y="verification_rate", hue="model_type", 
                        data=model_performance, palette={'Base': 'red', 'Fine-tuned': 'blue'}, 
                        legend=False)
        
        plt.title(f"Fine-tuned Models vs Base Model (4o-mini) - No Context ({self.evaluation_mode.replace('_', ' ').title()} Mode)")
        plt.xlabel("Model")
        plt.ylabel("Verification Rate")
        plt.xticks(rotation=45, ha="right")
        
        # Add value labels
        for i, v in enumerate(model_performance["verification_rate"]):
            ax.text(i, v + 0.01, f"{v:.3f}", ha="center", va="bottom")
        
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        
        return output_file
    
    def generate_comparison_report(self, requested_type: str = "all", 
                                 output_directory: str = "context_vs_finetune_comparison") -> Optional[str]:
        """
        Generate comprehensive comparison report between context and fine-tuning approaches.
        
        Args:
            requested_type: ERC type to analyze ("all" for all types)
            output_directory: Directory to save reports
            
        Returns:
            Path to output directory, or None if error occurred
        """
        # Include evaluation mode in output directory name
        output_directory = f"{output_directory}_{self.evaluation_mode}"
        
        # Generate reports for all ERC types or specific type
        if requested_type == "all":
            ft_data, base_data = self.load_data()
            
            if ft_data.empty or base_data.empty:
                print("No data available for comparison")
                return None
            
            # Get all available ERC types
            erc_types = ft_data["requested_type"].unique()
            print(f"Generating reports for ERC types: {erc_types}")
            
            # Generate individual reports
            for erc_type in erc_types:
                print(f"\nGenerating report for {erc_type.upper()}...")
                erc_output_dir = f"{output_directory}/{erc_type}"
                self._generate_single_erc_report(ft_data, base_data, erc_type, erc_output_dir)
            
            # Generate combined summary
            self._generate_combined_summary_report(ft_data, base_data, erc_types, output_directory)
            
            print(f"\nAll comparison reports generated in {output_directory}/")
            return output_directory
        else:
            # Generate report for single ERC type
            ft_data, base_data = self.load_data()
            
            if ft_data.empty or base_data.empty:
                print("No data available for comparison")
                return None
            
            return self._generate_single_erc_report(ft_data, base_data, requested_type, output_directory)
    
    def _generate_single_erc_report(self, ft_data: pd.DataFrame, base_data: pd.DataFrame, 
                                   requested_type: str, output_directory: str) -> str:
        """
        Generate a detailed comparison report for a single ERC type.
        
        Args:
            ft_data: Fine-tuned model data
            base_data: Base model data
            requested_type: ERC type to analyze
            output_directory: Output directory
            
        Returns:
            Path to output directory
        """
        os.makedirs(output_directory, exist_ok=True)
        
        # Perform comparisons
        no_context_comparison = self.compare_no_context_models(ft_data, base_data, requested_type)
        context_performance = self.analyze_base_model_contexts(base_data, requested_type)
        
        # Generate visualizations
        self.plot_context_comparison(context_performance, f"{output_directory}/context_comparison.png")
        self.plot_finetune_vs_base_comparison(no_context_comparison, f"{output_directory}/finetune_vs_base.png")
        
        # For function-level analysis, also generate ERC-specific function heatmap
        if self.evaluation_mode == "func_by_func":
            # Create a temporary AssistantComparer to generate function heatmap
            temp_comparer = AssistantComparer(mode="func_by_func_fine_tuning")
            temp_comparer.summary_df = pd.concat([ft_data, base_data], ignore_index=True)
            temp_comparer.plot_function_verification(f"{output_directory}/function_verification.png", requested_type)
        
        # Generate comprehensive markdown report
        report_path = os.path.join(output_directory, "comparison_report.md")
        
        with open(report_path, "w") as f:
            f.write(f"# Context Enhancement vs Fine-tuning Analysis - {requested_type.upper()}\n")
            f.write(f"## {self.evaluation_mode.replace('_', ' ').title()} Verification Mode\n\n")
            f.write("Comprehensive comparison of fine-tuned models versus base model with context enhancement.\n\n")
            
            # Fine-tuned vs Base (No Context) Analysis
            f.write("## Fine-tuned Models vs Base Model (No Context)\n\n")
            f.write("Direct comparison of fine-tuned models with base model, both using no additional context.\n\n")
            
            if not no_context_comparison.empty:
                # Performance comparison table
                model_performance = no_context_comparison.groupby("model").agg({
                    "verification_rate": "mean",
                    "verified_count": "sum",
                    "total_runs": "sum",
                    "avg_time": "mean",
                    "avg_iterations": "mean"
                }).reset_index()
                model_performance = model_performance.sort_values("verification_rate", ascending=False)
                
                f.write("**Performance Comparison:**\n\n")
                f.write("| Model | Verification Rate | Verified Count | Total Runs | Avg Time | Avg Iterations |\n")
                f.write("|-------|------------------|----------------|------------|----------|----------------|\n")
                
                for _, row in model_performance.iterrows():
                    f.write(f"| {row['model']} | {row['verification_rate']:.3f} | {row['verified_count']} | {row['total_runs']} | {row['avg_time']:.1f} | {row['avg_iterations']:.1f} |\n")
                
                f.write("\n")
                
                # Key findings
                best_ft = model_performance[model_performance["model"] != "4o-mini"]
                base_perf = model_performance[model_performance["model"] == "4o-mini"]
                
                if not best_ft.empty and not base_perf.empty:
                    best_ft_model = best_ft.iloc[0]
                    base_rate = base_perf.iloc[0]["verification_rate"]
                    ft_rate = best_ft_model["verification_rate"]
                    improvement = ((ft_rate - base_rate) / base_rate) * 100 if base_rate > 0 else 0
                    
                    f.write("**Key Findings:**\n")
                    f.write(f"- Best fine-tuned model: `{best_ft_model['model']}` ({ft_rate:.3f} verification rate)\n")
                    f.write(f"- Base model performance: {base_rate:.3f} verification rate\n")
                    f.write(f"- Fine-tuning improvement: {improvement:.1f}%\n\n")
            
            f.write("![Fine-tuned vs Base Model](finetune_vs_base.png)\n\n")
            
            # Context Analysis
            f.write("## Base Model Context Enhancement Analysis\n\n")
            f.write("Analysis of base model performance across different context configurations.\n\n")
            
            if not context_performance.empty:
                f.write("**Context Performance Analysis:**\n\n")
                f.write("| Context Type | Verification Rate | Verified | Total | Avg Time | Avg Iterations |\n")
                f.write("|-------------|------------------|----------|-------|----------|----------------|\n")
                
                for _, row in context_performance.iterrows():
                    f.write(f"| {row['context_type']} | {row['verification_rate']:.3f} | {row['verified_count']} | {row['total_runs']} | {row['avg_time']:.1f} | {row['avg_iterations']:.1f} |\n")
                
                f.write("\n")
                
                # Context insights
                best_context = context_performance.iloc[0]
                worst_context = context_performance.iloc[-1]
                
                f.write("**Context Analysis:**\n")
                f.write(f"- Best context: `{best_context['context_type']}` ({best_context['verification_rate']:.3f} rate)\n")
                f.write(f"- Worst context: `{worst_context['context_type']}` ({worst_context['verification_rate']:.3f} rate)\n")
                
                if worst_context['verification_rate'] > 0:
                    context_improvement = ((best_context['verification_rate'] - worst_context['verification_rate']) / worst_context['verification_rate']) * 100
                    f.write(f"- Context enhancement improvement: {context_improvement:.1f}%\n\n")
            
            f.write("![Context Performance](context_comparison.png)\n\n")
            
            # Add function-level analysis section for func_by_func mode
            if self.evaluation_mode == "func_by_func":
                f.write("## Function-level Verification Analysis\n\n")
                f.write("Analysis of which specific smart contract functions are most successfully verified.\n\n")
                f.write("![Function Verification Rates](function_verification.png)\n\n")
            
            # Strategic Conclusions
            f.write("## Strategic Analysis\n\n")
            
            if not no_context_comparison.empty and not context_performance.empty:
                model_perf = no_context_comparison.groupby("model")["verification_rate"].mean()
                best_ft_rate = model_perf[model_perf.index != "4o-mini"].max() if len(model_perf[model_perf.index != "4o-mini"]) > 0 else 0
                best_context_rate = context_performance["verification_rate"].max()
                
                f.write("**Performance Summary:**\n")
                f.write(f"- Best fine-tuned model: {best_ft_rate:.3f} verification rate\n")
                f.write(f"- Best context enhancement: {best_context_rate:.3f} verification rate\n")
                
                if best_ft_rate > best_context_rate:
                    winner = "Fine-tuning"
                    advantage = ((best_ft_rate - best_context_rate) / best_context_rate) * 100
                else:
                    winner = "Context enhancement"
                    advantage = ((best_context_rate - best_ft_rate) / best_ft_rate) * 100
                
                f.write(f"- **Winner: {winner}** (advantage: {advantage:.1f}%)\n\n")
                
                f.write("**Strategic Recommendations:**\n")
                f.write("1. **Resource Efficiency:** Context enhancement requires no training, fine-tuning requires computational resources\n")
                f.write("2. **Deployment Flexibility:** Context can be adjusted dynamically, fine-tuned models are static\n")
                f.write("3. **Performance Consistency:** Evaluate performance stability across different contract types\n")
                f.write("4. **Hybrid Approaches:** Consider combining fine-tuning with context enhancement\n\n")
            
            f.write(f"*Analysis generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        # Save raw data for further analysis
        no_context_comparison.to_csv(f"{output_directory}/no_context_comparison.csv", index=False)
        context_performance.to_csv(f"{output_directory}/context_performance.csv", index=False)
        
        print(f"Report generated for {requested_type.upper()} in {output_directory}/")
        return output_directory
    
    def _generate_combined_summary_report(self, ft_data: pd.DataFrame, base_data: pd.DataFrame, 
                                        erc_types: List[str], output_directory: str) -> None:
        """
        Generate a combined summary report across all ERC types.
        
        Args:
            ft_data: Fine-tuned model data
            base_data: Base model data
            erc_types: List of ERC types to analyze
            output_directory: Output directory
        """
        report_path = os.path.join(output_directory, "combined_summary_report.md")
        
        with open(report_path, "w") as f:
            f.write(f"# Executive Summary: Context Enhancement vs Fine-tuning\n")
            f.write(f"## {self.evaluation_mode.replace('_', ' ').title()} Verification Mode\n\n")
            f.write("Comprehensive analysis comparing context enhancement and fine-tuning across all ERC types.\n\n")
            
            # Collect summary statistics
            summary_data = []
            for erc_type in erc_types:
                no_context_comparison = self.compare_no_context_models(ft_data, base_data, erc_type)
                context_performance = self.analyze_base_model_contexts(base_data, erc_type)
                
                if not no_context_comparison.empty and not context_performance.empty:
                    model_performance = no_context_comparison.groupby("model")["verification_rate"].mean()
                    
                    best_ft_rate = model_performance[model_performance.index != "4o-mini"].max() if len(model_performance[model_performance.index != "4o-mini"]) > 0 else 0
                    base_no_context_rate = model_performance.get("4o-mini", 0)
                    best_context_rate = context_performance["verification_rate"].max()
                    best_context_name = context_performance.iloc[0]["context_type"]
                    
                    summary_data.append({
                        "erc_type": erc_type,
                        "best_ft_rate": best_ft_rate,
                        "base_no_context_rate": base_no_context_rate,
                        "best_context_rate": best_context_rate,
                        "best_context_name": best_context_name
                    })
            
            # Executive Summary Table
            f.write("## Performance Summary\n\n")
            f.write("| ERC Type | Best Fine-tuned | Base (No Context) | Best Context | Best Context Name |\n")
            f.write("|----------|------------------|-------------------|--------------|------------------|\n")
            
            for data in summary_data:
                f.write(f"| {data['erc_type'].upper()} | {data['best_ft_rate']:.3f} | {data['base_no_context_rate']:.3f} | {data['best_context_rate']:.3f} | {data['best_context_name']} |\n")
            
            f.write("\n")
            
            # Strategic Analysis
            f.write("## Strategic Insights\n\n")
            
            context_wins = sum(1 for data in summary_data if data['best_context_rate'] > data['best_ft_rate'])
            ft_wins = len(summary_data) - context_wins
            
            f.write("**Approach Effectiveness:**\n")
            f.write(f"- Context enhancement superior: {context_wins}/{len(summary_data)} ERC types ({context_wins/len(summary_data)*100:.0f}%)\n")
            f.write(f"- Fine-tuning superior: {ft_wins}/{len(summary_data)} ERC types ({ft_wins/len(summary_data)*100:.0f}%)\n\n")
            
            # Calculate average improvements
            valid_data = [d for d in summary_data if d['base_no_context_rate'] > 0]
            if valid_data:
                avg_context_improvement = sum((d['best_context_rate'] - d['base_no_context_rate']) / d['base_no_context_rate'] * 100 for d in valid_data) / len(valid_data)
                avg_ft_improvement = sum((d['best_ft_rate'] - d['base_no_context_rate']) / d['base_no_context_rate'] * 100 for d in valid_data) / len(valid_data)
                
                f.write("**Average Performance Improvements:**\n")
                f.write(f"- Context enhancement: {avg_context_improvement:.1f}% improvement over baseline\n")
                f.write(f"- Fine-tuning: {avg_ft_improvement:.1f}% improvement over baseline\n\n")
            
            f.write("## Implementation Recommendations\n\n")
            f.write("**Based on the analysis:**\n\n")
            
            if context_wins > ft_wins:
                f.write("1. **Primary Strategy:** Context enhancement shows superior performance\n")
                f.write("2. **Secondary Strategy:** Fine-tuning for specific use cases\n")
            else:
                f.write("1. **Primary Strategy:** Fine-tuning shows superior performance\n")
                f.write("2. **Secondary Strategy:** Context enhancement for rapid deployment\n")
            
            f.write("3. **Hybrid Approach:** Consider combining both methods for optimal results\n")
            f.write("4. **Resource Allocation:** Balance training costs vs deployment flexibility\n\n")
            
            f.write("## Detailed Reports\n\n")
            for erc_type in erc_types:
                f.write(f"- [{erc_type.upper()} Analysis]({erc_type}/comparison_report.md)\n")
            
            f.write(f"\n*Executive summary generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        print(f"Combined summary report generated at {report_path}")


def main():
    """
    Main function to handle command-line arguments and run the appropriate analysis.
    """
    parser = argparse.ArgumentParser(
        description="Smart Contract Verification Assistant Performance Comparison Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
            # Compare fine-tuned models vs base model with context (entire contract mode)
            python compare_assistants.py --mode context_vs_finetune --evaluation_mode entire_contract

            # Compare fine-tuned models vs base model with context (function-by-function mode)
            python compare_assistants.py --mode context_vs_finetune --evaluation_mode func_by_func

            # Analyze fine-tuned models only for specific ERC type (entire contract)
            python compare_assistants.py --mode entire_contract_fine_tuning --requested_type erc20

            # Analyze base model with context for all ERC types (entire contract)
            python compare_assistants.py --mode entire_contract_base_full_context --requested_type all

            # Analyze fine-tuned models function-by-function for specific ERC type
            python compare_assistants.py --mode func_by_func_fine_tuning --requested_type erc20

            # Analyze base model with context function-by-function for all ERC types
            python compare_assistants.py --mode func_by_func_base_full_context --requested_type all
            """
    )
    
    parser.add_argument(
        "--mode", 
        choices=["func_by_func_fine_tuning", "func_by_func_base_full_context", "context_vs_finetune", "entire_contract_fine_tuning", "entire_contract_base_full_context"], 
        required=True, 
        help="Analysis mode: basic comparison or context vs fine-tuning comparison"
    )
    
    parser.add_argument(
        "--evaluation_mode", 
        choices=["entire_contract", "func_by_func"], 
        default="entire_contract", 
        help="Evaluation approach for context_vs_finetune mode (default: entire_contract)"
    )
    
    parser.add_argument(
        "--requested_type", 
        default="all", 
        help="ERC type to analyze: erc20, erc721, erc1155, or all (default: all)"
    )
    
    args = parser.parse_args()

    # Execute the appropriate analysis
    if args.mode == "context_vs_finetune":
        print(f"Starting context vs fine-tuning comparison ({args.evaluation_mode} mode)...")
        comparer = ContextVsFinetuneComparer(evaluation_mode=args.evaluation_mode)
        result = comparer.generate_comparison_report(requested_type=args.requested_type)
        
        if result:
            print(f"✓ Analysis complete! Results saved to: {result}")
        else:
            print("✗ Analysis failed. Check the error messages above.")
            
    else:
        print(f"Starting basic assistant comparison ({args.mode} mode)...")
        comparer = AssistantComparer(mode=args.mode)
        data = comparer.load_and_analyze_data()
        
        if data is not None and not data.empty:
            # Determine ERC types to analyze
            if args.requested_type == "all":
                requested_types = data["requested_type"].unique()
            else:
                requested_types = [args.requested_type]
            
            # Generate reports for each ERC type
            for requested_type in requested_types:
                output_dir = f"assistant_comparison_report/{args.mode}/{requested_type}"
                result = comparer.generate_report_for_erc(requested_type, output_dir)
                
                if result:
                    print(f"✓ Report generated for {requested_type.upper()}: {result}")
                else:
                    print(f"✗ Failed to generate report for {requested_type.upper()}")
            
            print(f"✓ Analysis complete! Reports available in: assistant_comparison_report/{args.mode}/")
        else:
            print("✗ No data available for analysis. Check your data directories.")


if __name__ == "__main__":
    main()