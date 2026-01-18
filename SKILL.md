---
name: payroll-calculator
description: Use this skill when calculating Japanese payroll with complex rules including multi-tier overtime (45h/60h thresholds), late night and holiday premiums, grade-based social insurance, progressive income tax, and absence/tardiness deductions. Triggers on keywords like "payroll", "salary calculation", "overtime allowance", "social insurance", "income tax calculation", "Japanese labor law".
---

# Payroll Calculator Skill

A Claude Code skill for accurate Japanese payroll calculations with complex multi-tier rules that AI inference often gets wrong.

## When to Use This Skill

Use this skill when the user requests:
- Japanese payroll or salary calculations
- - Overtime allowance calculations with tiered rates
  - - Social insurance premium calculations
    - - Income tax calculations with progressive rates
      - - Attendance-based deductions (absence, tardiness)
        - - Generation of payroll Excel spreadsheets
         
          - ## Instructions
         
          - ### Phase 1: Data Preparation
         
          - 1. **Collect Required Input Data**
            2.    - Employee master data (ID, name, department, grade, base salary, commute allowance, dependents)
                  -    - Attendance data (overtime hours, late night hours, holiday hours, absences, tardiness)
                       -    - Grade table (insurance rates, base deductions per grade G1-G5)
                        
                            - 2. **Prepare Input JSON**
                              3.    Create a JSON file with the following structure:
                              4.   ```json
                                      {
                                        "employees": [...],
                                        "attendance": [...],
                                        "grade_table": {...}
                                      }
                                      ```

                                   ### Phase 2: Execute Calculation

                                   Run the payroll calculation script:
                                   ```bash
                                   python scripts/calculate_payroll.py input.json output.json
                                   ```

                                   ### Phase 3: Generate Excel Output

                                   Generate the Excel spreadsheet with 6 sheets:
                                   ```bash
                                   python scripts/generate_excel.py output.json payroll.xlsx
                                   ```

                                   ### Phase 4: Verify Results (Optional)

                                   Compare against expected values:
                                   ```bash
                                   python scripts/verify_results.py output.json expected.json
                                   ```

                                   ## Calculation Rules Summary

                                   ### Overtime Allowances (Critical - Tiered Calculation)

                                   | Hours | Rate | Formula |
                                   |-------|------|---------|
                                   | 0-45h | 1.25x | hourly_rate * 1.25 * hours |
                                   | 45-60h | 1.35x | (45h @ 1.25x) + (excess @ 1.35x) |
                                   | 60h+ | 1.50x | (45h @ 1.25x) + (15h @ 1.35x) + (excess @ 1.50x) |

                                   ### Other Premiums
                                   - **Late Night**: +0.25x (22:00-05:00)
                                   - - **Holiday Work**: 1.35x
                                     - - **Holiday Late Night**: 1.60x (1.35 + 0.25)
                                      
                                       - ### Deductions
                                       - - **Absence**: 3 days or less: daily_rate * days / 4+ days: daily_rate * days * 0.8
                                         - - **Tardiness**: Less than 4: (hourly/2) * count / 4+: (hourly/2) * count * 1.5
                                          
                                           - ### Social Insurance (Grade-based)
                                           - - G1, G2: 14.5%
                                             - - G3, G4: 15.0%
                                               - - G5: 15.5%
                                                
                                                 - ### Income Tax (Progressive)
                                                 - - 0-162,500: 5%
                                                   - - 162,501-275,000: 10% - 8,125
                                                     - - 275,001+: 20% - 35,625
                                                      
                                                       - ## Examples
                                                      
                                                       - ### Example 1: Basic Payroll Calculation
                                                      
                                                       - **User Request**: "Calculate payroll for employee Tanaka with base salary 300,000, 50 hours overtime"
                                                      
                                                       - **Execution**:
                                                       - ```bash
                                                         # Prepare input.json with employee data
                                                         python scripts/calculate_payroll.py input.json output.json
                                                         ```

                                                         **Expected Output**:
                                                         - Hourly rate: 300,000 / 160 = 1,875
                                                         - - Overtime: (45h * 1,875 * 1.25) + (5h * 1,875 * 1.35) = 118,406
                                                          
                                                           - ### Example 2: Full Payroll with Excel
                                                          
                                                           - **User Request**: "Generate monthly payroll spreadsheet for 3 employees"
                                                          
                                                           - **Execution**:
                                                           - ```bash
                                                             python scripts/calculate_payroll.py employees.json results.json
                                                             python scripts/generate_excel.py results.json payroll_2025_01.xlsx
                                                             ```

                                                             **Output**: Excel file with 6 sheets (Master, Attendance, Allowances, Deductions, Payslip, Verification)

                                                             ## What This Skill Cannot Do

                                                             - Tax filing or year-end adjustments
                                                             - - Bonus calculations
                                                               - - Retirement benefit calculations
                                                                 - - Social insurance grade determination (requires separate lookup)
                                                                   - - Currency conversions (JPY only)
                                                                    
                                                                     - ## File Structure
                                                                    
                                                                     - ```
                                                                       scripts/
                                                                         calculate_payroll.py  # Core calculation engine
                                                                         generate_excel.py     # Excel output generator
                                                                         verify_results.py     # Result verification

                                                                       references/
                                                                         calculation-rules.md  # Detailed calculation formulas
                                                                         troubleshooting.md    # Common issues and solutions
                                                                       ```

                                                                       ## Dependencies

                                                                       - Python 3.8+
                                                                       - - openpyxl (for Excel generation): `pip install openpyxl`
                                                                        
                                                                         - ## Related Documentation
                                                                        
                                                                         - For detailed calculation rules, see [references/calculation-rules.md](references/calculation-rules.md)
                                                                         - For troubleshooting, see [references/troubleshooting.md](references/troubleshooting.md)
