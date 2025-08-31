# Context Enhancement Performance Analysis for ERC1155 (Function-by-Function Mode)

This document analyzes context enhancement strategies for formal postcondition generation in smart contracts. Analysis based on 80 total runs.

## Overall Performance Analysis

Success rates for generating postconditions that pass formal verification.

ERC1155

| context_type         | verification_rate | verified_count | total_runs | avg_time           | avg_iterations |
| :------------------- | :---------------- | :------------- | :--------- | :----------------- | :------------- |
| erc1155              | 100.00            | 10             | 10         | 209.78542284965516 | 7.2            |
| erc20_erc721_erc1155 | 100.00            | 10             | 10         | 2278.3314697265623 | 6.7            |
| erc721_erc1155       | 90.00             | 9              | 10         | 2327.9117312908174 | 9.0            |
| erc20_erc1155        | 70.00             | 7              | 10         | 2413.4484199285507 | 12.6           |
| erc20                | 40.00             | 4              | 10         | 415.41905546188354 | 16.6           |
| erc20_erc721         | 30.00             | 3              | 10         | 2525.4149800777436 | 16.3           |
| erc721               | 10.00             | 1              | 10         | 490.29315292835236 | 20.1           |
| none                 | 10.00             | 1              | 10         | 443.61972270011904 | 21.4           |

**Key Observations:**

- Best performing context: 'erc1155' with 100.00% success rate
- Average success rate: 56.25%
- Lowest performing context: 'none' with 10.00% success rate

![Overall Verification Rates](verification_rates.png)

## Efficiency Analysis

Analysis of iterations and time required for successful vs failed verification attempts.

| context_type         | avg_fail_iterations | avg_success_iterations | avg_fail_time      | avg_success_time   | fail_rate |
| :------------------- | :------------------ | :--------------------- | :----------------- | :----------------- | :-------- |
| erc721               | 21.444444444444443  | 8.0                    | 521.2040697203743  | 212.09490180015564 | 90.00     |
| none                 | 23.0                | 7.0                    | 474.8125154177348  | 162.88458824157715 | 90.00     |
| erc20_erc721         | 18.714285714285715  | 10.666666666666666     | 3511.4119034494674 | 224.75549221038818 | 70.00     |
| erc20                | 20.666666666666668  | 10.5                   | 528.9909324645996  | 245.06123995780945 | 60.00     |
| erc20_erc1155        | 24.0                | 7.714285714285714      | 7520.36861594518   | 224.76833592142378 | 30.00     |
| erc721_erc1155       | 24.0                | 7.333333333333333      | 487.2707171440125  | 2532.427399529351  | 10.00     |
| erc1155              | 0.0                 | 7.2                    | 0.0                | 209.78542284965516 | 0.00      |
| erc20_erc721_erc1155 | 0.0                 | 6.7                    | 0.0                | 2278.3314697265623 | 0.00      |

## Function-level Verification Analysis

Analysis of which specific smart contract functions are most successfully verified.

![Function Verification Rates](function_verification.png)

## Conclusions and Recommendations

**Key Findings:**

1. Top performing contexts: `erc1155`, `erc20_erc721_erc1155`, `erc721_erc1155`
2. Base model without context: 10.00%
3. Context enhancement improvement: 900.0% over no context

_Report generated on 2025-08-29 22:18:09_
