---
name: payroll-calculator
description: Claude Code Skill for complex Japanese payroll calculations
version: 1.0.0
---

# Payroll Calculator Skill

A Claude Code skill for accurate Japanese payroll calculations with multi-tier overtime, social insurance, and progressive taxation.

## Features

- Multi-tier overtime calculation (45h/60h thresholds)
- - Late night and holiday work premiums
  - - Grade-based social insurance rates
    - - Progressive income tax
      - - Absence and tardiness deductions
        - - Excel output with cross-sheet references
         
          - ## Usage
         
          - ```bash
            python scripts/calculate_payroll.py input.json output.json
            python scripts/generate_excel.py output.json payroll.xlsx
            ```

            ## Documentation

            - [Calculation Rules](references/calculation-rules.md)
            - - [Troubleshooting](references/troubleshooting.md)
