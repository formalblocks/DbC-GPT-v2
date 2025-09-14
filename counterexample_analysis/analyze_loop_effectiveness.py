#!/usr/bin/env python3
"""
Loop Effectiveness Analysis for Entire Contract Verification

This script analyzes the effectiveness of the iterative refinement loop in the
entire contract verification approach by examining when LLMs succeed on the first
attempt vs. when they need multiple iterations.

Key Questions Answered:
1. How many times did the LLM get it right the first time? (iterations=0, verified=True)
2. How many times did the LLM get it right after the first iteration? (iterations=1, verified=True)
3. How many cases showed the loop was useful? (iterations>0, verified=True)
"""

import os
import pandas as pd
import glob
from pathlib import Path
from typing import Dict, List, Tuple
import json

class LoopEffectivenessAnalyzer:
    """Analyzes loop effectiveness in entire contract verification experiments."""

    def __init__(self):
        self.base_path = Path("/Users/gabrielnogueira/Projects/master/DbC-GPT-v2/experiments")
        self.results_dirs = [
            "results_entire_contract_fine_tuning",
            "results_entire_contract_base_full_context"
        ]
        self.all_data = []

    def collect_all_csv_files(self) -> List[Path]:
        """Collect all CSV files from both result directories."""
        csv_files = []

        for results_dir in self.results_dirs:
            dir_path = self.base_path / results_dir
            if dir_path.exists():
                pattern = str(dir_path / "**" / "*.csv")
                csv_files.extend([Path(f) for f in glob.glob(pattern, recursive=True)])

        print(f"Found {len(csv_files)} CSV files to analyze")
        return csv_files

    def parse_file_path(self, file_path: Path) -> Dict[str, str]:
        """Extract metadata from file path structure."""
        parts = file_path.parts

        # Find the results directory index
        results_dir_idx = None
        for i, part in enumerate(parts):
            if part.startswith("results_entire_contract_"):
                results_dir_idx = i
                break

        if results_dir_idx is None:
            return {}

        result_type = parts[results_dir_idx]

        # Extract assistant, contract, context from path
        try:
            if result_type == "results_entire_contract_fine_tuning":
                assistant = parts[results_dir_idx + 1]
                contract = parts[results_dir_idx + 2]
                context = parts[results_dir_idx + 3]
                experiment_type = "fine_tuning"
            elif result_type == "results_entire_contract_base_full_context":
                assistant = parts[results_dir_idx + 1]
                contract = parts[results_dir_idx + 2]
                context = parts[results_dir_idx + 3]
                experiment_type = "base_full_context"
            else:
                return {}

            return {
                "experiment_type": experiment_type,
                "assistant": assistant,
                "contract": contract,
                "context": context,
                "file_path": str(file_path)
            }
        except IndexError:
            return {}

    def load_and_process_csv(self, file_path: Path) -> pd.DataFrame:
        """Load CSV and add metadata."""
        try:
            df = pd.read_csv(file_path)
            metadata = self.parse_file_path(file_path)

            # Add metadata columns
            for key, value in metadata.items():
                df[key] = value

            return df
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return pd.DataFrame()

    def analyze_data(self):
        """Main analysis function."""
        print("Collecting CSV files...")
        csv_files = self.collect_all_csv_files()

        print("Processing CSV files...")
        all_dataframes = []
        for csv_file in csv_files:
            df = self.load_and_process_csv(csv_file)
            if not df.empty:
                all_dataframes.append(df)

        if not all_dataframes:
            print("No valid CSV files found!")
            return

        # Combine all data
        self.combined_df = pd.concat(all_dataframes, ignore_index=True)
        print(f"Total runs analyzed: {len(self.combined_df)}")

        # Ensure verified column is boolean
        self.combined_df['verified'] = self.combined_df['verified'].astype(bool)

        # Calculate key metrics
        self.calculate_metrics()
        self.generate_detailed_breakdown()
        self.generate_summary_report()

    def calculate_metrics(self):
        """Calculate key effectiveness metrics."""
        df = self.combined_df

        # Total runs
        self.total_runs = len(df)

        # Success cases
        successful_runs = df[df['verified'] == True]
        self.total_successful = len(successful_runs)

        # First-time success (iterations = 0, verified = True)
        first_time_success = df[(df['iterations'] == 0) & (df['verified'] == True)]
        self.first_time_success_count = len(first_time_success)

        # Success after first iteration (iterations = 1, verified = True)
        second_iteration_success = df[(df['iterations'] == 1) & (df['verified'] == True)]
        self.second_iteration_success_count = len(second_iteration_success)

        # Loop was useful (iterations > 0, verified = True)
        loop_useful = df[(df['iterations'] > 0) & (df['verified'] == True)]
        self.loop_useful_count = len(loop_useful)

        # Average iterations for successful cases
        if self.total_successful > 0:
            self.avg_iterations_successful = successful_runs['iterations'].mean()
        else:
            self.avg_iterations_successful = 0

        # Success rate
        self.success_rate = (self.total_successful / self.total_runs) * 100 if self.total_runs > 0 else 0

    def generate_detailed_breakdown(self):
        """Generate detailed breakdown by assistant and contract type."""
        df = self.combined_df

        # Group by assistant and contract
        self.breakdown_by_assistant = df.groupby(['experiment_type', 'assistant', 'contract']).agg({
            'run': 'count',  # Total runs
            'verified': ['sum', lambda x: (x.sum() / len(x)) * 100],  # Success count and rate
        }).round(2)

        self.breakdown_by_assistant.columns = ['total_runs', 'successful_runs', 'success_rate_pct']

        # Calculate iteration-specific metrics by group
        groups = df.groupby(['experiment_type', 'assistant', 'contract'])

        iteration_metrics = []
        for (exp_type, assistant, contract), group in groups:
            successful = group[group['verified'] == True]

            first_time = len(group[(group['iterations'] == 0) & (group['verified'] == True)])
            second_iter = len(group[(group['iterations'] == 1) & (group['verified'] == True)])
            loop_useful = len(group[(group['iterations'] > 0) & (group['verified'] == True)])

            iteration_metrics.append({
                'experiment_type': exp_type,
                'assistant': assistant,
                'contract': contract,
                'first_time_success': first_time,
                'second_iteration_success': second_iter,
                'loop_useful_cases': loop_useful,
                'avg_iterations_if_successful': successful['iterations'].mean() if len(successful) > 0 else 0
            })

        self.iteration_breakdown = pd.DataFrame(iteration_metrics)

    def generate_summary_report(self):
        """Generate and print comprehensive summary report."""
        print("\n" + "="*80)
        print("LOOP EFFECTIVENESS ANALYSIS - ENTIRE CONTRACT VERIFICATION")
        print("="*80)

        print(f"\n📊 OVERALL STATISTICS:")
        print(f"Total runs analyzed: {self.total_runs:,}")
        print(f"Total successful runs: {self.total_successful:,}")
        print(f"Overall success rate: {self.success_rate:.1f}%")
        print(f"Average iterations for successful runs: {self.avg_iterations_successful:.2f}")

        print(f"\n🎯 KEY FINDINGS:")
        print(f"First-time success (iteration=0): {self.first_time_success_count:,} cases ({(self.first_time_success_count/self.total_runs)*100:.1f}% of all runs)")
        print(f"Success after first iteration (iteration=1): {self.second_iteration_success_count:,} cases ({(self.second_iteration_success_count/self.total_runs)*100:.1f}% of all runs)")
        print(f"Loop was useful (iterations>0 + successful): {self.loop_useful_count:,} cases ({(self.loop_useful_count/self.total_runs)*100:.1f}% of all runs)")

        if self.total_successful > 0:
            print(f"\n📈 SUCCESS BREAKDOWN:")
            first_time_pct_of_success = (self.first_time_success_count / self.total_successful) * 100
            loop_useful_pct_of_success = (self.loop_useful_count / self.total_successful) * 100
            print(f"Of successful runs:")
            print(f"  - {first_time_pct_of_success:.1f}% succeeded on first try")
            print(f"  - {loop_useful_pct_of_success:.1f}% needed refinement loop (iterations > 0)")

        print(f"\n🔄 LOOP UTILITY ANALYSIS:")
        if self.loop_useful_count > 0:
            loop_utility_rate = (self.loop_useful_count / self.total_runs) * 100
            print(f"The refinement loop was useful in {self.loop_useful_count:,} cases ({loop_utility_rate:.1f}% of all runs)")
            print(f"This means the iterative approach provided value beyond first attempt in {loop_utility_rate:.1f}% of experiments")
        else:
            print("The refinement loop provided no additional successful cases beyond first attempts")

        # Detailed breakdown by experiment type
        print(f"\n📋 BREAKDOWN BY EXPERIMENT TYPE:")
        for exp_type in self.combined_df['experiment_type'].unique():
            subset = self.combined_df[self.combined_df['experiment_type'] == exp_type]
            successful_subset = subset[subset['verified'] == True]

            first_time = len(subset[(subset['iterations'] == 0) & (subset['verified'] == True)])
            second_iter = len(subset[(subset['iterations'] == 1) & (subset['verified'] == True)])
            loop_useful = len(subset[(subset['iterations'] > 0) & (subset['verified'] == True)])

            print(f"\n{exp_type.upper().replace('_', ' ')}:")
            print(f"  Total runs: {len(subset):,}")
            print(f"  Successful runs: {len(successful_subset):,} ({(len(successful_subset)/len(subset))*100:.1f}%)")
            print(f"  First-time success: {first_time:,} ({(first_time/len(subset))*100:.1f}%)")
            print(f"  Second iteration success: {second_iter:,} ({(second_iter/len(subset))*100:.1f}%)")
            print(f"  Loop useful cases: {loop_useful:,} ({(loop_useful/len(subset))*100:.1f}%)")

        # Top performing assistants for first-time success
        print(f"\n🏆 TOP PERFORMERS - FIRST-TIME SUCCESS:")
        first_time_by_assistant = self.iteration_breakdown.groupby(['experiment_type', 'assistant'])['first_time_success'].sum().reset_index()
        first_time_by_assistant = first_time_by_assistant.sort_values('first_time_success', ascending=False).head(10)

        for _, row in first_time_by_assistant.iterrows():
            print(f"  {row['assistant']} ({row['experiment_type']}): {row['first_time_success']} first-time successes")

        # Export detailed data
        self.export_detailed_results()

    def export_detailed_results(self):
        """Export detailed results to CSV files."""
        output_dir = Path("counterexample_analysis/loop_effectiveness_analysis")
        output_dir.mkdir(exist_ok=True)

        # Export full dataset with metadata
        self.combined_df.to_csv(output_dir / "full_analysis_data.csv", index=False)

        # Export iteration breakdown
        self.iteration_breakdown.to_csv(output_dir / "iteration_breakdown_by_assistant.csv", index=False)

        # Export summary statistics
        summary_stats = {
            "total_runs": self.total_runs,
            "total_successful": self.total_successful,
            "success_rate": self.success_rate,
            "first_time_success_count": self.first_time_success_count,
            "first_time_success_rate": (self.first_time_success_count / self.total_runs) * 100,
            "second_iteration_success_count": self.second_iteration_success_count,
            "second_iteration_success_rate": (self.second_iteration_success_count / self.total_runs) * 100,
            "loop_useful_count": self.loop_useful_count,
            "loop_useful_rate": (self.loop_useful_count / self.total_runs) * 100,
            "avg_iterations_successful": self.avg_iterations_successful
        }

        with open(output_dir / "summary_statistics.json", 'w') as f:
            json.dump(summary_stats, f, indent=2)

        print(f"\n💾 Detailed results exported to: {output_dir}")
        print(f"  - full_analysis_data.csv: Complete dataset")
        print(f"  - iteration_breakdown_by_assistant.csv: Breakdown by assistant")
        print(f"  - summary_statistics.json: Key metrics summary")

def main():
    """Main execution function."""
    analyzer = LoopEffectivenessAnalyzer()
    analyzer.analyze_data()

if __name__ == "__main__":
    main()