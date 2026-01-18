# Calculation Rules

## Overview

This document describes the detailed calculation rules for the payroll system.

## 1. Hourly Rate

```
Hourly Rate = Base Salary / 160 (truncate)
```

## 2. Overtime Allowances

### Regular Overtime (Tiered Calculation)

| Hours | Rate | Calculation |
|-------|------|-------------|
| 0-45h | 1.25x | hourly_rate * 1.25 * hours |
| 45-60h | 1.35x | (45h at 1.25x) + (excess at 1.35x) |
| 60h+ | 1.50x | (45h at 1.25x) + (15h at 1.35x) + (excess at 1.50x) |

### Late Night Premium
- Additional 0.25x for hours worked 22:00-05:00
- - Formula: hourly_rate * 0.25 * hours
 
  - ### Holiday Work
  - - Base rate: 1.35x
    - - Formula: hourly_rate * 1.35 * hours
     
      - ### Holiday Late Night
      - - Combined rate: 1.35x + 0.25x = 1.60x
        - - Formula: hourly_rate * 1.60 * hours
         
          - ## 3. Deductions from Pay
         
          - ### Absence Deduction
         
          - | Days | Formula |
          - |------|---------|
          - | 1-3 days | (base_salary / 20) * days |
          - | 4+ days | (base_salary / 20) * days * 0.8 |
         
          - ### Tardiness Deduction
         
          - | Count | Formula |
          - |-------|---------|
          - | 1-3 times | (hourly_rate / 2) * count |
          - | 4+ times | (hourly_rate / 2) * count * 1.5 |
         
          - ## 4. Gross Pay
         
          - ```
            Gross Pay = Base Salary + Commute Allowance + Total Allowances - Deductions from Pay
            ```

            ## 5. Statutory Deductions

            ### Social Insurance

            ```
            Social Insurance = (Gross Pay - Commute Allowance) * Insurance Rate
            ```

            Grade-based rates:
            - G1, G2: 14.5%
            - - G3, G4: 15.0%
              - - G5: 15.5%
               
                - ### Income Tax (Progressive)
               
                - ```
                  Taxable Income = Gross Pay - Social Insurance - Base Deduction - (38,000 * Dependents)
                  ```

                  | Taxable Income | Rate | Formula |
                  |----------------|------|---------|
                  | 0 - 162,500 | 5% | taxable * 0.05 |
                  | 162,501 - 275,000 | 10% | taxable * 0.10 - 8,125 |
                  | 275,001+ | 20% | taxable * 0.20 - 35,625 |

                  ## 6. Net Pay

                  ```
                  Net Pay = Gross Pay - Social Insurance - Income Tax
                  ```

                  ## Important Notes

                  - All calculations use truncation (floor) for yen amounts
                  - - Commute allowance is excluded from social insurance calculation
                    - - Dependent deduction is 38,000 yen per person
