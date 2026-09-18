# UCI Default of Credit Card Clients Schema Report

Official URL: https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients
DOI: 10.24432/C55S3H
Raw artifact: `data/raw/default+of+credit+card+clients.zip` (not modified).
The `.xls` member was converted via Excel COM to a temporary CSV for reading only.

- Rows: 30000
- Columns: 25
- UCI page stated instances: 30000
- UCI page stated features: 23
- Target column: default payment next month
- Target definition status: VERIFIED_FROM_UCI_SPREADSHEET_AND_DOCUMENTATION

## Columns

| column | x_code | dtype |
| --- | --- | --- |
| ID | ID | str |
| LIMIT_BAL | X1 | int64 |
| SEX | X2 | int64 |
| EDUCATION | X3 | int64 |
| MARRIAGE | X4 | int64 |
| AGE | X5 | int64 |
| PAY_0 | X6 | int64 |
| PAY_2 | X7 | int64 |
| PAY_3 | X8 | int64 |
| PAY_4 | X9 | int64 |
| PAY_5 | X10 | int64 |
| PAY_6 | X11 | int64 |
| BILL_AMT1 | X12 | int64 |
| BILL_AMT2 | X13 | int64 |
| BILL_AMT3 | X14 | int64 |
| BILL_AMT4 | X15 | int64 |
| BILL_AMT5 | X16 | int64 |
| BILL_AMT6 | X17 | int64 |
| PAY_AMT1 | X18 | int64 |
| PAY_AMT2 | X19 | int64 |
| PAY_AMT3 | X20 | int64 |
| PAY_AMT4 | X21 | int64 |
| PAY_AMT5 | X22 | int64 |
| PAY_AMT6 | X23 | int64 |
| default payment next month | Y | int64 |

## Target

{
  "target_column": "default payment next month",
  "target_definition_status": "VERIFIED_FROM_UCI_SPREADSHEET_AND_DOCUMENTATION",
  "target_definition_from_documentation": "UCI Additional Variable Information: binary default payment (Yes = 1, No = 0) as the response variable. Spreadsheet header names this column 'default payment next month'.",
  "unique_values": [
    1,
    0
  ],
  "value_counts": [
    {
      "value": 0,
      "count": 23364,
      "percentage": 77.88
    },
    {
      "value": 1,
      "count": 6636,
      "percentage": 22.12
    }
  ],
  "missing_target_rows": 0,
  "prevalence_eq_1": 0.2212,
  "prevalence_eq_1_percentage": 22.12
}

## Temporal fields

NO_CALENDAR_TIMESTAMPS. Payment/bill columns encode a fixed April-September 2005 window from the UCI documentation, not per-row origination timestamps.

## Financing purpose

ABSENT

## Documentation vs contents conflicts

These discrepancies were not silently recoded.

[
  {
    "field": "EDUCATION",
    "documentation": "UCI Additional Variable Information: 1=graduate school; 2=university; 3=high school; 4=others.",
    "undocumented_values_observed": [
      0,
      5,
      6
    ],
    "counts": {
      "0": 14,
      "5": 280,
      "6": 51
    },
    "status": "SOURCE_CONTENTS_CONFLICT"
  },
  {
    "field": "MARRIAGE",
    "documentation": "UCI Additional Variable Information: 1=married; 2=single; 3=others.",
    "undocumented_values_observed": [
      0
    ],
    "counts": {
      "0": 54
    },
    "status": "SOURCE_CONTENTS_CONFLICT"
  },
  {
    "field": "PAY_0",
    "documentation": "UCI Additional Variable Information: -1=pay duly; 1=delay one month; ...; 8=delay eight months; 9=delay nine months and above. Values 0 and -2 are not defined there.",
    "undocumented_values_observed": [
      -2,
      0
    ],
    "counts": {
      "-2": 2759,
      "0": 14737
    },
    "status": "SOURCE_CONTENTS_CONFLICT"
  },
  {
    "field": "PAY_2",
    "documentation": "UCI Additional Variable Information: -1=pay duly; 1=delay one month; ...; 8=delay eight months; 9=delay nine months and above. Values 0 and -2 are not defined there.",
    "undocumented_values_observed": [
      -2,
      0
    ],
    "counts": {
      "-2": 3782,
      "0": 15730
    },
    "status": "SOURCE_CONTENTS_CONFLICT"
  },
  {
    "field": "PAY_3",
    "documentation": "UCI Additional Variable Information: -1=pay duly; 1=delay one month; ...; 8=delay eight months; 9=delay nine months and above. Values 0 and -2 are not defined there.",
    "undocumented_values_observed": [
      -2,
      0
    ],
    "counts": {
      "-2": 4085,
      "0": 15764
    },
    "status": "SOURCE_CONTENTS_CONFLICT"
  },
  {
    "field": "PAY_4",
    "documentation": "UCI Additional Variable Information: -1=pay duly; 1=delay one month; ...; 8=delay eight months; 9=delay nine months and above. Values 0 and -2 are not defined there.",
    "undocumented_values_observed": [
      -2,
      0
    ],
    "counts": {
      "-2": 4348,
      "0": 16455
    },
    "status": "SOURCE_CONTENTS_CONFLICT"
  },
  {
    "field": "PAY_5",
    "documentation": "UCI Additional Variable Information: -1=pay duly; 1=delay one month; ...; 8=delay eight months; 9=delay nine months and above. Values 0 and -2 are not defined there.",
    "undocumented_values_observed": [
      -2,
      0
    ],
    "counts": {
      "-2": 4546,
      "0": 16947
    },
    "status": "SOURCE_CONTENTS_CONFLICT"
  },
  {
    "field": "PAY_6",
    "documentation": "UCI Additional Variable Information: -1=pay duly; 1=delay one month; ...; 8=delay eight months; 9=delay nine months and above. Values 0 and -2 are not defined there.",
    "undocumented_values_observed": [
      -2,
      0
    ],
    "counts": {
      "-2": 4895,
      "0": 16286
    },
    "status": "SOURCE_CONTENTS_CONFLICT"
  }
]

Negative BILL_AMT* counts: {'BILL_AMT1': 590, 'BILL_AMT2': 669, 'BILL_AMT3': 655, 'BILL_AMT4': 675, 'BILL_AMT5': 655, 'BILL_AMT6': 688}

Column profile: `results/tables/uci_column_profile.csv`.
