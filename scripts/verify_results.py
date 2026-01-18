#!/usr/bin/env python3
"""
Verification script for payroll calculation results.
Compares calculated values against expected values.
"""

import json
import sys


def verify_results(calculated, expected):
      """Compare calculated vs expected results"""
      results = []
      total_errors = 0

    calc_results = {r['employee_id']: r for r in calculated['results']}
    exp_results = {r['employee_id']: r for r in expected['results']}

    for emp_id in calc_results:
              calc = calc_results[emp_id]
              exp = exp_results.get(emp_id)

        if not exp:
                      results.append({
                                        'employee_id': emp_id,
                                        'status': 'ERROR',
                                        'message': 'Expected data not found'
                      })
                      total_errors += 1
                      continue

        errors = []

        if calc['gross_pay'] != exp['gross_pay']:
                      errors.append(f"Gross pay: calc={calc['gross_pay']:,}, exp={exp['gross_pay']:,}")

        if calc['net_pay'] != exp['net_pay']:
                      errors.append(f"Net pay: calc={calc['net_pay']:,}, exp={exp['net_pay']:,}")

        calc_ded = calc['statutory_deductions']['total']
        exp_ded = exp['statutory_deductions']['total']
        if calc_ded != exp_ded:
                      errors.append(f"Deductions: calc={calc_ded:,}, exp={exp_ded:,}")

        if errors:
                      results.append({
                                        'employee_id': emp_id,
                                        'employee_name': calc['employee_name'],
                                        'status': 'MISMATCH',
                                        'errors': errors
                      })
                      total_errors += len(errors)
else:
              results.append({
                                'employee_id': emp_id,
                                'employee_name': calc['employee_name'],
                                'status': 'OK',
                                'gross_pay': calc['gross_pay'],
                                'net_pay': calc['net_pay']
              })

    return {
              'verification_results': results,
              'total_employees': len(calc_results),
              'total_errors': total_errors,
              'status': 'PASS' if total_errors == 0 else 'FAIL'
    }


def main():
      if len(sys.argv) < 3:
                print("Usage: python verify_results.py <calculated.json> <expected.json>")
                sys.exit(1)

      try:
                with open(sys.argv[1], 'r', encoding='utf-8') as f:
                              calculated = json.load(f)

                with open(sys.argv[2], 'r', encoding='utf-8') as f:
                              expected = json.load(f)

                result = verify_results(calculated, expected)

          print("=" * 60)
        print("Verification Report")
        print("=" * 60)

        for r in result['verification_results']:
                      print(f"\\n[{r['employee_id']} {r.get('employee_name', '')}]")
                      if r['status'] == 'OK':
                                        print(f"  OK - Gross: {r['gross_pay']:,}, Net: {r['net_pay']:,}")
elif r['status'] == 'MISMATCH':
                print("  MISMATCH:")
                for error in r['errors']:
                                      print(f"    - {error}")
else:
                print(f"  {r['message']}")

        print("\\n" + "=" * 60)
        print(f"Result: {result['status']}")
        print(f"Employees: {result['total_employees']}")
        print(f"Errors: {result['total_errors']}")
        print("=" * 60)

        sys.exit(0 if result['status'] == 'PASS' else 1)

except FileNotFoundError as e:
        print(f"Error: File not found: {e}")
        sys.exit(1)
except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
      main()
