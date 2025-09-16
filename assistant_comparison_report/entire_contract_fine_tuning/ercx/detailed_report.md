# Assistant Fine-Tuning Performance Analysis for ERCX (Entire Contract Mode)

This document analyzes fine-tuning experiments for formal postcondition generation in smart contracts. Analysis based on 1 total runs.

## Overall Performance Analysis

Success rates for generating postconditions that pass formal verification.

**Total Runs Analyzed:** 1

| model | verification_rate | verified_count | total_runs |
| :--- | :--- | :--- | :--- |
| 4.1 | 0.00 | 0 | 1 |

**Key Observations:**

- Best performing model: '4.1' with 0.00% success rate
- Average success rate: 0.00%
- Lowest performing model: '4.1' with 0.00% success rate

![Overall Verification Rates](verification_rates.png)

## Efficiency Analysis

Analysis of iterations and time required for successful vs failed verification attempts.

| model | avg_fail_iterations | avg_success_iterations | avg_fail_time | avg_success_time | fail_rate |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 4.1 | 10.0 | 0.0 | 274.3040256500244 | 0.0 | 100.00 |

## Function-level Verification Analysis

Analysis of which specific smart contract functions are most successfully verified.

![Function Verification Rates](function_verification.png)

## Conclusions and Recommendations

**Key Findings:**

1. Top performing models: `4.1`
3. Successful verifications are faster than failed attempts, indicating early success predictors

*Report generated on 2025-07-18 21:12:45*
