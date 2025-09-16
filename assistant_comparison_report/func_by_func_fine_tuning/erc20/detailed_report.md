# Assistant Fine-Tuning Performance Analysis for ERC20 (Function-by-Function Mode)

This document analyzes fine-tuning experiments for formal postcondition generation in smart contracts. Analysis based on 80 total runs.

## Overall Performance Analysis

Success rates for generating postconditions that pass formal verification.

**Total Runs Analyzed:** 80

| model                    | verification_rate | verified_count | total_runs |
| :----------------------- | :---------------- | :------------- | :--------- |
| erc-20-721-1155-001-5-16 | 90.00             | 9              | 10         |
| erc-20-721-001-5-16      | 80.00             | 8              | 10         |
| erc-721-1155-001-5-16    | 80.00             | 8              | 10         |
| erc-20-1155-001-5-16     | 70.00             | 7              | 10         |
| erc-20-001-5-16          | 60.00             | 6              | 10         |
| erc-1155-001-5-16        | 20.00             | 2              | 10         |
| 4o-mini                  | 0.00              | 0              | 10         |
| erc-721-001-5-16         | 0.00              | 0              | 10         |

**Key Observations:**

- Best performing model: 'erc-20-721-1155-001-5-16' with 90.00% success rate
- Average success rate: 50.00%
- Lowest performing model: 'erc-721-001-5-16' with 0.00% success rate

![Overall Verification Rates](verification_rates.png)

## Efficiency Analysis

Analysis of iterations and time required for successful vs failed verification attempts.

| model                    | avg_fail_iterations | avg_success_iterations | avg_fail_time      | avg_success_time   | fail_rate |
| :----------------------- | :------------------ | :--------------------- | :----------------- | :----------------- | :-------- |
| 4o-mini                  | 32.8                | 0.0                    | 983.2470988512039  | 0.0                | 100.00    |
| erc-721-001-5-16         | 27.4                | 0.0                    | 286.13276574611666 | 0.0                | 100.00    |
| erc-1155-001-5-16        | 21.625              | 9.0                    | 244.70638886094093 | 110.95581293106079 | 80.00     |
| erc-20-001-5-16          | 17.5                | 10.833333333333334     | 250.84748131036758 | 180.97096248467764 | 40.00     |
| erc-20-1155-001-5-16     | 19.666666666666668  | 9.571428571428571      | 223.36651571591696 | 110.3314436163221  | 30.00     |
| erc-20-721-001-5-16      | 18.0                | 11.25                  | 206.10038304328918 | 128.55050814151764 | 20.00     |
| erc-721-1155-001-5-16    | 19.5                | 9.75                   | 287.7330940961838  | 153.27940759062767 | 20.00     |
| erc-20-721-1155-001-5-16 | 28.0                | 11.222222222222221     | 354.554322719574   | 143.03005101945666 | 10.00     |

## Function-level Verification Analysis

Analysis of which specific smart contract functions are most successfully verified.

![Function Verification Rates](function_verification.png)

## Conclusions and Recommendations

**Key Findings:**

1. Top performing models: `erc-20-721-1155-001-5-16`, `erc-20-721-001-5-16`, `erc-721-1155-001-5-16`
2. Baseline model (4o-mini) performance: 0.00%
3. Successful verifications are faster than failed attempts, indicating early success predictors

_Report generated on 2025-09-11 20:18:28_
