#!/usr/bin/env python3
"""
Base Model Context Impact Analysis for Loop Effectiveness

This script analyzes the 4o-mini base model specifically to understand how different
context types affect performance and identify potential specification copying behavior.

Key Questions Answered:
1. When does the model copy reference specifications vs. reason independently?
2. How much do different context types help vs. pure model capability?
3. What's the optimal context strategy for maximum effectiveness?
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple
import json

class BaseModelContextAnalyzer:
    """Analyzes context impact on 4o-mini base model performance."""

    def __init__(self):
        self.base_path = Path("/Users/gabrielnogueira/Projects/master/DbC-GPT-v2/experiments")
        self.analysis_data = None

    def load_existing_analysis(self) -> pd.DataFrame:
        """Load the existing full analysis data."""
        analysis_file = Path("counterexample_analysis/loop_effectiveness_analysis/full_analysis_data.csv")
        if not analysis_file.exists():
            raise FileNotFoundError("Please run analyze_loop_effectiveness.py first to generate the base analysis data")

        return pd.read_csv(analysis_file)

    def filter_base_model_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filter for 4o-mini base model data only."""
        base_model_data = df[
            (df['experiment_type'] == 'base_full_context') &
            (df['assistant'] == '4o-mini')
        ].copy()

        print(f"Filtered to {len(base_model_data)} runs for 4o-mini base model")
        return base_model_data

    def categorize_contexts(self, df: pd.DataFrame) -> pd.DataFrame:
        """Categorize context types for analysis."""
        def get_context_category(row):
            contract = row['contract']
            context = row['context']

            if context == 'none':
                return 'no_context'
            elif context == contract:
                return 'same_type_context'  # Potential copying scenario
            elif '_' in context:
                # Multi-context scenario - check if contract is in the list of contexts
                context_parts = context.split('_')
                if contract in context_parts:
                    return 'multi_context_including_same'  # Multi-context with same type included
                else:
                    return 'multi_context_different'  # Multi-context, no same type
            else:
                return 'cross_type_context'  # Different single context

        df['context_category'] = df.apply(get_context_category, axis=1)
        return df

    def calculate_context_metrics(self, df: pd.DataFrame) -> Dict:
        """Calculate key metrics for each context category."""
        metrics = {}

        # Group by context category and contract type
        for (category, contract), group in df.groupby(['context_category', 'contract']):
            key = f"{category}_{contract}"

            total_runs = len(group)
            successful_runs = group[group['verified'] == True]
            total_successful = len(successful_runs)

            # Core metrics
            first_time_success = len(group[(group['iterations'] == 0) & (group['verified'] == True)])
            second_iteration_success = len(group[(group['iterations'] == 1) & (group['verified'] == True)])
            loop_useful = len(group[(group['iterations'] > 0) & (group['verified'] == True)])

            # Rates
            success_rate = (total_successful / total_runs) * 100 if total_runs > 0 else 0
            first_time_rate = (first_time_success / total_runs) * 100 if total_runs > 0 else 0
            loop_useful_rate = (loop_useful / total_runs) * 100 if total_runs > 0 else 0

            # Average iterations for successful cases
            avg_iterations = successful_runs['iterations'].mean() if len(successful_runs) > 0 else 0

            metrics[key] = {
                'context_category': category,
                'contract': contract,
                'total_runs': total_runs,
                'successful_runs': total_successful,
                'success_rate': success_rate,
                'first_time_success': first_time_success,
                'first_time_rate': first_time_rate,
                'second_iteration_success': second_iteration_success,
                'loop_useful_cases': loop_useful,
                'loop_useful_rate': loop_useful_rate,
                'avg_iterations_if_successful': avg_iterations
            }

        # Also calculate overall metrics by category
        for category in df['context_category'].unique():
            category_data = df[df['context_category'] == category]
            total_runs = len(category_data)
            successful_runs = category_data[category_data['verified'] == True]
            total_successful = len(successful_runs)

            first_time_success = len(category_data[(category_data['iterations'] == 0) & (category_data['verified'] == True)])
            second_iteration_success = len(category_data[(category_data['iterations'] == 1) & (category_data['verified'] == True)])
            loop_useful = len(category_data[(category_data['iterations'] > 0) & (category_data['verified'] == True)])

            success_rate = (total_successful / total_runs) * 100 if total_runs > 0 else 0
            first_time_rate = (first_time_success / total_runs) * 100 if total_runs > 0 else 0
            loop_useful_rate = (loop_useful / total_runs) * 100 if total_runs > 0 else 0

            avg_iterations = successful_runs['iterations'].mean() if len(successful_runs) > 0 else 0

            metrics[f"{category}_OVERALL"] = {
                'context_category': category,
                'contract': 'ALL',
                'total_runs': total_runs,
                'successful_runs': total_successful,
                'success_rate': success_rate,
                'first_time_success': first_time_success,
                'first_time_rate': first_time_rate,
                'second_iteration_success': second_iteration_success,
                'loop_useful_cases': loop_useful,
                'loop_useful_rate': loop_useful_rate,
                'avg_iterations_if_successful': avg_iterations
            }

        return metrics

    def analyze_copying_behavior(self, metrics: Dict) -> Dict:
        """Analyze potential copying behavior by comparing context scenarios."""
        copying_analysis = {}

        contracts = ['erc20', 'erc721', 'erc1155']

        for contract in contracts:
            # Get metrics for different context scenarios
            no_context = metrics.get(f"no_context_{contract}", {})
            same_type = metrics.get(f"same_type_context_{contract}", {})
            cross_type_keys = [k for k in metrics.keys() if f"cross_type_context_{contract}" in k]

            if no_context and same_type:
                # Compare first-time success rates
                no_context_first_rate = no_context.get('first_time_rate', 0)
                same_type_first_rate = same_type.get('first_time_rate', 0)

                # Calculate improvement from adding same-type context
                improvement = same_type_first_rate - no_context_first_rate

                # Calculate copying indicator (high improvement suggests copying)
                copying_indicator = improvement / no_context_first_rate if no_context_first_rate > 0 else float('inf')

                copying_analysis[contract] = {
                    'no_context_first_time_rate': no_context_first_rate,
                    'same_type_first_time_rate': same_type_first_rate,
                    'improvement_percentage_points': improvement,
                    'relative_improvement': copying_indicator,
                    'no_context_success_rate': no_context.get('success_rate', 0),
                    'same_type_success_rate': same_type.get('success_rate', 0),
                    'no_context_avg_iterations': no_context.get('avg_iterations_if_successful', 0),
                    'same_type_avg_iterations': same_type.get('avg_iterations_if_successful', 0)
                }

        return copying_analysis

    def generate_detailed_report(self, df: pd.DataFrame, metrics: Dict, copying_analysis: Dict):
        """Generate comprehensive analysis report."""
        print("\n" + "="*80)
        print("BASE MODEL CONTEXT IMPACT ANALYSIS - 4o-mini")
        print("="*80)

        print(f"\n📊 OVERALL BASE MODEL STATISTICS:")
        print(f"Total runs analyzed: {len(df):,}")
        print(f"Total successful runs: {len(df[df['verified'] == True]):,}")
        print(f"Overall success rate: {(len(df[df['verified'] == True])/len(df))*100:.1f}%")

        print(f"\n🔍 CONTEXT CATEGORY BREAKDOWN:")
        for category in df['context_category'].unique():
            category_metrics = metrics.get(f"{category}_OVERALL", {})
            if category_metrics:
                print(f"\n{category.upper().replace('_', ' ')}:")
                print(f"  Total runs: {category_metrics['total_runs']:,}")
                print(f"  Success rate: {category_metrics['success_rate']:.1f}%")
                print(f"  First-time success rate: {category_metrics['first_time_rate']:.1f}%")
                print(f"  Loop useful rate: {category_metrics['loop_useful_rate']:.1f}%")
                print(f"  Avg iterations (successful): {category_metrics['avg_iterations_if_successful']:.2f}")

        print(f"\n🎯 COPYING BEHAVIOR ANALYSIS:")
        for contract, analysis in copying_analysis.items():
            print(f"\n{contract.upper()} CONTRACT:")
            print(f"  No context first-time success: {analysis['no_context_first_time_rate']:.1f}%")
            print(f"  Same-type context first-time success: {analysis['same_type_first_time_rate']:.1f}%")
            print(f"  Improvement: +{analysis['improvement_percentage_points']:.1f} percentage points")

            if analysis['relative_improvement'] == float('inf'):
                print(f"  Relative improvement: Infinite (started from 0%)")
            else:
                print(f"  Relative improvement: {analysis['relative_improvement']*100:.1f}%")

            # Interpretation
            if analysis['improvement_percentage_points'] > 30:
                print(f"  🚨 HIGH COPYING INDICATOR: Large improvement suggests heavy reliance on reference specs")
            elif analysis['improvement_percentage_points'] > 15:
                print(f"  ⚠️  MODERATE COPYING: Some reliance on reference specifications")
            else:
                print(f"  ✅ LOW COPYING: Minimal reliance on reference specifications")

        print(f"\n📈 DETAILED CONTEXT COMPARISON:")
        # Create comparison table
        comparison_data = []
        for key, metric in metrics.items():
            if '_OVERALL' not in key:  # Skip overall metrics for detailed table
                comparison_data.append(metric)

        if comparison_data:
            comparison_df = pd.DataFrame(comparison_data)
            comparison_df = comparison_df.sort_values(['context_category', 'contract'])

            print("\nDETAILED METRICS BY CONTEXT AND CONTRACT:")
            print(comparison_df.to_string(index=False, float_format='%.1f'))

        print(f"\n🏆 KEY INSIGHTS:")

        # Find best performing context overall
        best_category = max(metrics.keys(), key=lambda k: metrics[k]['success_rate'] if '_OVERALL' in k else 0)
        if '_OVERALL' in best_category:
            best_metrics = metrics[best_category]
            print(f"1. Best overall context: {best_metrics['context_category'].replace('_', ' ').title()}")
            print(f"   - Success rate: {best_metrics['success_rate']:.1f}%")
            print(f"   - First-time success rate: {best_metrics['first_time_rate']:.1f}%")

        # Analyze copying patterns
        high_copying_contracts = [c for c, a in copying_analysis.items() if a['improvement_percentage_points'] > 20]
        if high_copying_contracts:
            print(f"2. High copying behavior detected for: {', '.join(high_copying_contracts).upper()}")
            print(f"   - These contracts show significant performance boosts with same-type context")

        # Best strategy recommendation
        no_context_avg = np.mean([metrics[f"no_context_{c}_OVERALL"]['success_rate'] for c in ['erc20', 'erc721', 'erc1155'] if f"no_context_{c}_OVERALL" in metrics])
        same_type_avg = np.mean([metrics[f"same_type_context_{c}_OVERALL"]['success_rate'] for c in ['erc20', 'erc721', 'erc1155'] if f"same_type_context_{c}_OVERALL" in metrics])

        print(f"3. Context Strategy Recommendation:")
        if same_type_avg > no_context_avg + 15:
            print(f"   - PROVIDE SAME-TYPE CONTEXT: Average improvement of {same_type_avg - no_context_avg:.1f} percentage points")
        else:
            print(f"   - MINIMAL CONTEXT BENEFIT: Pure model capability is relatively strong")

        self.export_context_analysis(df, metrics, copying_analysis)

    def export_context_analysis(self, df: pd.DataFrame, metrics: Dict, copying_analysis: Dict):
        """Export detailed context analysis results."""
        output_dir = Path("counterexample_analysis/base_model_context_analysis")
        output_dir.mkdir(exist_ok=True)

        # Export filtered dataset with context categories
        df.to_csv(output_dir / "4o_mini_context_analysis_data.csv", index=False)

        # Export metrics breakdown
        metrics_df = pd.DataFrame.from_dict(metrics, orient='index')
        metrics_df.to_csv(output_dir / "context_metrics_breakdown.csv")

        # Export copying behavior analysis
        copying_df = pd.DataFrame.from_dict(copying_analysis, orient='index')
        copying_df.to_csv(output_dir / "copying_behavior_analysis.csv")

        # Export summary statistics
        summary_stats = {
            "total_runs_analyzed": len(df),
            "total_successful_runs": len(df[df['verified'] == True]),
            "overall_success_rate": (len(df[df['verified'] == True]) / len(df)) * 100,
            "context_categories": list(df['context_category'].unique()),
            "copying_analysis_summary": copying_analysis
        }

        with open(output_dir / "context_analysis_summary.json", 'w') as f:
            json.dump(summary_stats, f, indent=2, default=str)

        print(f"\n💾 Context analysis results exported to: {output_dir}")
        print(f"  - 4o_mini_context_analysis_data.csv: Filtered dataset with context categories")
        print(f"  - context_metrics_breakdown.csv: Detailed metrics by context type")
        print(f"  - copying_behavior_analysis.csv: Copying behavior analysis")
        print(f"  - context_analysis_summary.json: Summary statistics and insights")


    def analyze(self):
        """Main analysis function."""
        print("Loading existing analysis data...")
        df = self.load_existing_analysis()

        print("Filtering for 4o-mini base model...")
        base_model_df = self.filter_base_model_data(df)

        print("Categorizing contexts...")
        base_model_df = self.categorize_contexts(base_model_df)

        print("Calculating context metrics...")
        metrics = self.calculate_context_metrics(base_model_df)

        print("Analyzing copying behavior...")
        copying_analysis = self.analyze_copying_behavior(metrics)

        print("Generating comprehensive report...")
        self.generate_detailed_report(base_model_df, metrics, copying_analysis)

def main():
    """Main execution function."""
    analyzer = BaseModelContextAnalyzer()
    analyzer.analyze()

if __name__ == "__main__":
    main()