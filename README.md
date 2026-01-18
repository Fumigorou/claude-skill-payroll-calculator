# Payroll Calculator - Claude Code Skill

A Claude Code Skill for accurate Japanese payroll calculations with complex multi-tier rules.

## Why This Skill?

AI models often struggle with complex payroll calculations due to:
- Multi-tier overtime rates with different thresholds (45h/60h)
- - Conditional logic for deductions (absence days, tardiness counts)
  - - Progressive tax brackets with different formulas
    - - Precise truncation requirements (floor to yen)
     
      - This skill uses Python scripts for **deterministic, accurate calculations** instead of relying on AI inference.
     
      - ## Features
     
      - - **Multi-tier Overtime Calculation**
        -   - 0-45h: 1.25x rate
            -   - 45-60h: 1.35x rate
                -   - 60h+: 1.50x rate
                 
                    - - **Premium Calculations**
                      -   - Late night premium (+0.25x)
                          -   - Holiday work (1.35x)
                              -   - Holiday late night (1.60x)
                               
                                  - - **Deduction Calculations**
                                    -   - Absence deduction (with 4+ days penalty)
                                        -   - Tardiness deduction (with 4+ times penalty)
                                         
                                            - - **Statutory Deductions**
                                              -   - Grade-based social insurance (G1-G5: 14.5%-15.5%)
                                                  -   - Progressive income tax (5%/10%/20% brackets)
                                                   
                                                      - - **Excel Output**
                                                        -   - 6-sheet workbook with cross-references
                                                            -   - Master, Attendance, Allowances, Deductions, Payslip, Verification sheets
                                                             
                                                                - ## Installation
                                                             
                                                                - ### For Claude Code Users
                                                             
                                                                - 1. Clone this repository into your Claude Code skills directory:
                                                                 
                                                                  2. ```bash
                                                                     # Project-specific (shared with team)
                                                                     git clone https://github.com/Fumigorou/claude-skill-payroll-calculator.git .claude/skills/payroll-calculator

                                                                     # Or personal (available across all projects)
                                                                     git clone https://github.com/Fumigorou/claude-skill-payroll-calculator.git ~/.claude/skills/payroll-calculator
                                                                     ```

                                                                     2. Install dependencies:
                                                                    
                                                                     3. ```bash
                                                                        pip install openpyxl
                                                                        ```

                                                                        ### For Standalone Use

                                                                        ```bash
                                                                        git clone https://github.com/Fumigorou/claude-skill-payroll-calculator.git
                                                                        cd claude-skill-payroll-calculator
                                                                        pip install openpyxl
                                                                        ```

                                                                        ## Usage

                                                                        ### With Claude Code

                                                                        Simply ask Claude to calculate payroll:

                                                                        ```
                                                                        "Calculate monthly payroll for 3 employees with the following data..."
                                                                        "Generate a payroll Excel spreadsheet for January 2025"
                                                                        ```

                                                                        Claude will automatically use this skill when it detects payroll-related requests.

                                                                        ### Standalone Scripts

                                                                        ```bash
                                                                        # Calculate payroll
                                                                        python scripts/calculate_payroll.py input.json output.json

                                                                        # Generate Excel
                                                                        python scripts/generate_excel.py output.json payroll.xlsx

                                                                        # Verify results
                                                                        python scripts/verify_results.py output.json expected.json
                                                                        ```

                                                                        ## Input Format

                                                                        ```json
                                                                        {
                                                                          "employees": [
                                                                            {
                                                                              "id": "E001",
                                                                              "name": "Tanaka Ichiro",
                                                                              "department": "Sales",
                                                                              "grade": "G3",
                                                                              "base_salary": 300000,
                                                                              "commute_allowance": 15000,
                                                                              "dependents": 2
                                                                            }
                                                                          ],
                                                                          "attendance": [
                                                                            {
                                                                              "employee_id": "E001",
                                                                              "regular_overtime_hours": 50,
                                                                              "late_night_overtime_hours": 5,
                                                                              "holiday_work_hours": 8,
                                                                              "absence_days": 1,
                                                                              "tardiness_count": 2
                                                                            }
                                                                          ],
                                                                          "grade_table": {
                                                                            "G1": {"insurance_rate": 0.145, "base_deduction": 48000},
                                                                            "G2": {"insurance_rate": 0.145, "base_deduction": 48000},
                                                                            "G3": {"insurance_rate": 0.150, "base_deduction": 48000},
                                                                            "G4": {"insurance_rate": 0.150, "base_deduction": 48000},
                                                                            "G5": {"insurance_rate": 0.155, "base_deduction": 48000}
                                                                          }
                                                                        }
                                                                        ```

                                                                        ## File Structure

                                                                        ```
                                                                        claude-skill-payroll-calculator/
                                                                        ├── SKILL.md                 # Skill definition (required)
                                                                        ├── README.md                # This file
                                                                        ├── scripts/
                                                                        │   ├── calculate_payroll.py # Core calculation engine
                                                                        │   ├── generate_excel.py    # Excel output generator
                                                                        │   └── verify_results.py    # Result verification
                                                                        └── references/
                                                                            ├── calculation-rules.md # Detailed formulas
                                                                            └── troubleshooting.md   # Common issues
                                                                        ```

                                                                        ## Requirements

                                                                        - Python 3.8+
                                                                        - - openpyxl (for Excel generation)
                                                                         
                                                                          - ## License
                                                                         
                                                                          - MIT License
                                                                         
                                                                          - ## Contributing
                                                                         
                                                                          - Contributions are welcome! Please feel free to submit a Pull Request.
                                                                         
                                                                          - ## Related Links
                                                                         
                                                                          - - [Claude Code Skills Documentation](https://code.claude.com/docs/skills)
                                                                            - - [Anthropic Skills Repository](https://github.com/anthropics/skills)
