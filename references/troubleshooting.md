# Troubleshooting Guide

## Common Issues

### 1. openpyxl Not Installed

**Error:**
```
Error: openpyxl is not installed.
```

**Solution:**
```bash
pip install openpyxl
```

### 2. JSON Parse Error

**Error:**
```
Error: JSON parsing failed
```

**Causes:**
- JSON syntax error (missing comma, mismatched brackets)
- - Character encoding issues
 
  - **Solution:**
  - - Save files as UTF-8
    - - Validate JSON format using a linter
     
      - ### 3. Calculation Mismatch
     
      - **Checklist:**
     
      - 1. **Input Data**
        2.    - Verify base salary is correct
              -    - Verify grade is properly set
                   -    - Verify attendance data (overtime hours, absence days)
                    
                        - 2. **Grade Table**
                          3.    - Check insurance rates
                                -    - Check base deduction amounts
                                 
                                     - 3. **Calculation Rules**
                                       4.    - Overtime tiers (45h/60h thresholds)
                                             -    - Absence rules (3 days or less / 4 days or more)
                                                  -    - Tardiness rules (less than 4 / 4 or more)
                                                   
                                                       - ### 4. Excel Formula Errors
                                                   
                                                       - **#REF! Error:**
                                                       - - Check if sheet names were changed
                                                         - - Verify referenced cells exist
                                                          
                                                           - **#VALUE! Error:**
                                                           - - Check for non-numeric data in numeric fields
                                                            
                                                             - **#NAME? Error:**
                                                             - - LET function may not be supported
                                                               - - Recommend Excel 365 or Excel 2021+
                                                                
                                                                 - ### 5. VLOOKUP Error
                                                                
                                                                 - **Causes:**
                                                                 - - Grade table range is incorrect
                                                                   - - Grade code (G1-G5) doesn't match
                                                                    
                                                                     - **Solution:**
                                                                     - - Verify Master sheet grade table range
                                                                       - - Confirm employee grade exists in table
                                                                        
                                                                         - ## Debug Steps
                                                                        
                                                                         - ### Step 1: Validate Input
                                                                         - ```bash
                                                                           python -m json.tool input.json
                                                                           ```

                                                                           ### Step 2: Check Output
                                                                           ```bash
                                                                           python -m json.tool output.json
                                                                           ```

                                                                           ### Step 3: Verify Individual Calculations
                                                                           Review output.json for each employee:
                                                                           - `allowances`: Each allowance amount
                                                                           - - `deductions_from_pay`: Absence/tardiness deductions
                                                                             - - `statutory_deductions`: Insurance and tax
                                                                              
                                                                               - ### Step 4: Excel Formula Check
                                                                               - 1. Open Excel file
                                                                                 2. 2. Select cells to view formulas
                                                                                    3. 3. Verify cross-sheet references
                                                                                      
                                                                                       4. ## Support
                                                                                      
                                                                                       5. If issues persist, provide:
                                                                                       6. 1. Input data (input.json)
                                                                                          2. 2. Complete error message
                                                                                             3. 3. Expected output
                                                                                                4. 4. Environment (OS, Python version, Excel version)
