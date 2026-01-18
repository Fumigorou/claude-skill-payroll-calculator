#!/usr/bin/env python3
"""
給与計算スクリプト
複雑な条件分岐を含む給与計算を正確に実行します。
"""

import json
import sys
import math
from typing import Dict, List, Any

# 定数
MONTHLY_WORKING_HOURS = 160  # 月間所定労働時間
DAILY_WORKING_DAYS = 20      # 月間所定労働日数
DEPENDENT_DEDUCTION = 38000  # 扶養控除額（1人あたり）

# 残業倍率
OVERTIME_RATE_NORMAL = 1.25       # 45h以下
OVERTIME_RATE_EXTENDED = 1.35     # 45-60h
OVERTIME_RATE_EXCESSIVE = 1.50    # 60h超
LATE_NIGHT_PREMIUM = 0.25         # 深夜割増
HOLIDAY_RATE = 1.35               # 休日出勤

# 残業閾値
OVERTIME_THRESHOLD_1 = 45  # 第1段階閾値
OVERTIME_THRESHOLD_2 = 60  # 第2段階閾値


def truncate(value: float) -> int:
      """円未満切り捨て"""
      return int(math.floor(value))


def calculate_hourly_rate(base_salary: int) -> int:
      """時間単価を計算（基本給÷160、円未満切り捨て）"""
      return truncate(base_salary / MONTHLY_WORKING_HOURS)


def calculate_regular_overtime_allowance(hourly_rate: int, hours: float) -> int:
      """
          平日残業手当を計算（段階的計算）
              - 45h以下: 1.25倍
                  - 45-60h: 45hまで1.25倍、超過分1.35倍
                      - 60h超: 45hまで1.25倍、15h分1.35倍、超過分1.50倍
                          """
      if hours <= 0:
                return 0

      if hours <= OVERTIME_THRESHOLD_1:
                return truncate(hourly_rate * OVERTIME_RATE_NORMAL * hours)
elif hours <= OVERTIME_THRESHOLD_2:
        tier1 = hourly_rate * OVERTIME_RATE_NORMAL * OVERTIME_THRESHOLD_1
        tier2 = hourly_rate * OVERTIME_RATE_EXTENDED * (hours - OVERTIME_THRESHOLD_1)
        return truncate(tier1 + tier2)
else:
        tier1 = hourly_rate * OVERTIME_RATE_NORMAL * OVERTIME_THRESHOLD_1
          tier2 = hourly_rate * OVERTIME_RATE_EXTENDED * (OVERTIME_THRESHOLD_2 - OVERTIME_THRESHOLD_1)
        tier3 = hourly_rate * OVERTIME_RATE_EXCESSIVE * (hours - OVERTIME_THRESHOLD_2)
        return truncate(tier1 + tier2 + tier3)


def calculate_late_night_allowance(hourly_rate: int, hours: float) -> int:
      """深夜残業手当を計算（+0.25倍の追加分）"""
    if hours <= 0:
              return 0
          return truncate(hourly_rate * LATE_NIGHT_PREMIUM * hours)


def calculate_holiday_allowance(hourly_rate: int, hours: float) -> int:
      """休日出勤手当を計算（1.35倍）"""
    if hours <= 0:
              return 0
          return truncate(hourly_rate * HOLIDAY_RATE * hours)


def calculate_holiday_late_night_allowance(hourly_rate: int, hours: float) -> int:
      """休日深夜手当を計算（1.35倍 + 0.25倍）"""
    if hours <= 0:
              return 0
          return truncate(hourly_rate * (HOLIDAY_RATE + LATE_NIGHT_PREMIUM) * hours)


def calculate_absence_deduction(base_salary: int, absence_days: int) -> int:
      """
          欠勤控除を計算
              - 3日以下: (基本給÷20) × 日数
                  - 4日以上: (基本給÷20) × 日数 × 0.8（減額率適用）
                      """
    if absence_days <= 0:
              return 0

    daily_rate = truncate(base_salary / DAILY_WORKING_DAYS)

    if absence_days <= 3:
              return truncate(daily_rate * absence_days)
else:
        return truncate(daily_rate * absence_days * 0.8)


def calculate_tardiness_deduction(hourly_rate: int, tardiness_count: int) -> int:
      """
          遅刻早退控除を計算
              - 4回未満: (時間単価÷2) × 回数
                  - 4回以上: (時間単価÷2) × 回数 × 1.5（ペナルティ率適用）
                      """
    if tardiness_count <= 0:
              return 0

    base_deduction = truncate(hourly_rate / 2)

    if tardiness_count < 4:
              return truncate(base_deduction * tardiness_count)
else:
        return truncate(base_deduction * tardiness_count * 1.5)


def calculate_social_insurance(gross_pay: int, commute_allowance: int, insurance_rate: float) -> int:
      """社会保険料を計算"""
    taxable_base = gross_pay - commute_allowance
    return truncate(taxable_base * insurance_rate)


def calculate_income_tax(gross_pay: int, social_insurance: int, base_deduction: int, dependents: int) -> int:
      """所得税を計算（累進課税）"""
    taxable_income = gross_pay - social_insurance - base_deduction - (DEPENDENT_DEDUCTION * dependents)

    if taxable_income <= 0:
              return 0

    if taxable_income <= 162500:
              return truncate(taxable_income * 0.05)
elif taxable_income <= 275000:
        return truncate(taxable_income * 0.10 - 8125)
else:
        return truncate(taxable_income * 0.20 - 35625)


def calculate_employee_payroll(employee: Dict, attendance: Dict, grade_table: Dict) -> Dict:
      """1人の従業員の給与を計算"""
    base_salary = employee['base_salary']
    commute_allowance = employee['commute_allowance']
    dependents = employee.get('dependents', 0)
    grade = employee['grade']
    grade_info = grade_table[grade]

    regular_overtime = attendance.get('regular_overtime_hours', 0)
    late_night_overtime = attendance.get('late_night_overtime_hours', 0)
    holiday_work = attendance.get('holiday_work_hours', 0)
    holiday_late_night = attendance.get('holiday_late_night_hours', 0)
    absence_days = attendance.get('absence_days', 0)
    tardiness_count = attendance.get('tardiness_count', 0)

    hourly_rate = calculate_hourly_rate(base_salary)

    regular_overtime_allowance = calculate_regular_overtime_allowance(hourly_rate, regular_overtime)
    late_night_allowance = calculate_late_night_allowance(hourly_rate, late_night_overtime)
    holiday_allowance = calculate_holiday_allowance(hourly_rate, holiday_work)
    holiday_late_night_allowance = calculate_holiday_late_night_allowance(hourly_rate, holiday_late_night)

    absence_deduction = calculate_absence_deduction(base_salary, absence_days)
    tardiness_deduction = calculate_tardiness_deduction(hourly_rate, tardiness_count)

    total_allowances = (regular_overtime_allowance + late_night_allowance +
                                                holiday_allowance + holiday_late_night_allowance)
    total_deductions_from_pay = absence_deduction + tardiness_deduction
    gross_pay = base_salary + commute_allowance + total_allowances - total_deductions_from_pay

    social_insurance = calculate_social_insurance(gross_pay, commute_allowance, grade_info['insurance_rate'])
    income_tax = calculate_income_tax(gross_pay, social_insurance, grade_info['base_deduction'], dependents)

    total_deductions = social_insurance + income_tax
    net_pay = gross_pay - total_deductions

    return {
              'employee_id': employee['id'],
              'employee_name': employee['name'],
              'department': employee['department'],
              'grade': grade,
              'base_salary': base_salary,
              'commute_allowance': commute_allowance,
              'dependents': dependents,
              'hourly_rate': hourly_rate,
              'attendance': {
                            'regular_overtime_hours': regular_overtime,
                            'late_night_overtime_hours': late_night_overtime,
                            'holiday_work_hours': holiday_work,
                            'holiday_late_night_hours': holiday_late_night,
                            'absence_days': absence_days,
                            'tardiness_count': tardiness_count
              },
              'allowances': {
                            'regular_overtime': regular_overtime_allowance,
                            'late_night': late_night_allowance,
                            'holiday_work': holiday_allowance,
                            'holiday_late_night': holiday_late_night_allowance,
                            'total': total_allowances
              },
              'deductions_from_pay': {
                            'absence': absence_deduction,
                            'tardiness': tardiness_deduction,
                            'total': total_deductions_from_pay
              },
              'gross_pay': gross_pay,
              'statutory_deductions': {
                            'social_insurance': social_insurance,
                            'income_tax': income_tax,
                            'total': total_deductions
              },
              'net_pay': net_pay
    }


def process_payroll(input_data: Dict) -> Dict:
      """全従業員の給与計算を処理"""
      employees = input_data['employees']
      attendance_list = input_data['attendance']
      grade_table = input_data['grade_table']

    attendance_map = {a['employee_id']: a for a in attendance_list}

    results = []
    summary = {
              'total_gross_pay': 0,
              'total_deductions': 0,
              'total_net_pay': 0,
              'employee_count': len(employees)
    }

    for emp in employees:
              emp_id = emp['id']
              attendance = attendance_map.get(emp_id, {})
              result = calculate_employee_payroll(emp, attendance, grade_table)
              results.append(result)
              summary['total_gross_pay'] += result['gross_pay']
              summary['total_deductions'] += result['statutory_deductions']['total']
              summary['total_net_pay'] += result['net_pay']

    return {
              'results': results,
              'summary': summary,
              'grade_table': grade_table
    }


def main():
      if len(sys.argv) < 3:
                print("Usage: python calculate_payroll.py <input.json> <output.json>")
                sys.exit(1)

      input_file = sys.argv[1]
      output_file = sys.argv[2]

    try:
              with open(input_file, 'r', encoding='utf-8') as f:
                            input_data = json.load(f)

              output_data = process_payroll(input_data)

        with open(output_file, 'w', encoding='utf-8') as f:
                      json.dump(output_data, f, ensure_ascii=False, indent=2)

        print("=" * 60)
        print("給与計算完了")
        print("=" * 60)
        for result in output_data['results']#:!
/ u s r / b i n / e n v  ppryitnhto(nf3"
\"\"n"【
{給r与計e算スsクリuプトl
 t複雑[な条'件分e岐をm含むp給与l計算oを正y確にe実行eしま_す。i
 d"'"]"}

{irmepsourltt [j'seomnp
 liomypeoer_tn asmyes'
 ]i}m】p"o)r
t   m a t h 
 f r o m   tpyrpiinntg( fi"m p o総支r給額t:  D i c¥{tr,e sLuilstt[,' gArnoys
s
_#p a定数y
'M]O:N,T}H"L)Y
_ W O R K I N G _ H O U RpSr i=n t1(6f0"    #控 除合月計間:所定 労働 時間 
¥D{ArIeLsYu_lWtO[R'KsItNaGt_uDtAoYrSy _=d e2d0u c t i o n s#' ]月[間所'定労t働日o数
   tDaElP'E]N:D,E}N"T)_
   D E D U C T I O N   =   3p8r0i0n0t ( f#"  扶 養控差除引額支（給1額:人あ たり¥）{
   r
   e#s u残業l倍率t
   [O'VnEeRtT_IpMaEy_'R]A:T,E}_"N)O
   R
   M A L   =   1 . 2p5r i n t ( " \ \#n "4 5+h 以下"
   =O"V E*R T6I0M)E
   _ R A T E _ E X TpErNiDnEtD( f=" 結1果を. 3{5o u t p u t#_ f4i5l-e6}0 hに保
   存しOましVた。E"R)T
   I
   M E _ R AeTxEc_eEpXtC EFSiSlIeVNEo t=F o1u.n5d0E r r o r#: 
   6 0 h 超 
    L A T Ep_rNiInGtH(Tf_"PERrErMoIrU:M  フ=ァイ ルが0見つ.かり2ませ5ん:   { i n p u t _ f#i l深夜e割増}
    "H)O
    L I D A Y _ R A TsEy s=. e1x.i3t5( 1 ) 
             e x c e p t   j#s o休日n出勤.
             J
             S#O N残業D閾値e
             cOoVdEeRETrIrMoEr_ TaHsR EeS:H
             O L D _ 1   =   4p5r i n#t (第1f段"階閾E値
             rOrVoErR:T IJMSEO_NTの解H析にR失敗EしまSしたH:O L{De_}2" )=
               6 0     #   第 2s段階y閾値s
               .
               e
               xdietf( 1t)r
               u n c a teex(cveapltu eE:x cfelpotaito)n  -a>s  ien:t
               : 
                        " " "p円未r満切iり捨nて"t"("f
                        " E r r orre:t u{ren} "i)n
                        t ( m a t h . f lsoyosr.(evxailtu(e1)))





                        idfe f_ _cnaalmceu_l_a t=e=_ h"o_u_rmlayi_nr_a_t"e:(
                        b a s e _msaailna(r)y: int) -> int:
                            """時間単価を計算（基本給÷160、円未満切り捨て）"""
                                return truncate(base_salary / MONTHLY_WORKING_HOURS)


                                def calculate_regular_overtime_allowance(hourly_rate: int, hours: float) -> int:
                                    """
                                        平日残業手当を計算（段階的計算）
                                            - 45h以下: 1.25倍
                                                - 45-60h: 45hまで1.25倍、超過分1.35倍
                                                    - 60h超: 45hまで1.25倍、15h分1.35倍、超過分1.50倍
                                                        """
                                                            if hours <= 0:
                                                                    return 0

                                                                        if hours <= OVERTIME_THRESHOLD_1:
                                                                                return truncate(hourly_rate * OVERTIME_RATE_NORMAL * hours)
                                                                                    elif hours <= OVERTIME_THRESHOLD_2:
                                                                                            tier1 = hourly_rate * OVERTIME_RATE_NORMAL * OVERTIME_THRESHOLD_1
                                                                                                    tier2 = hourly_rate * OVERTIME_RATE_EXTENDED * (hours - OVERTIME_THRESHOLD_1)
                                                                                                            return truncate(tier1 + tier2)
                                                                                                                else:
                                                                                                                        tier1 = hourly_rate * OVERTIME_RATE_NORMAL * OVERTIME_THRESHOLD_1
                                                                                                                                tier2 = hourly_rate * OVERTIME_RATE_EXTENDED * (OVERTIME_THRESHOLD_2 - OVERTIME_THRESHOLD_1)
                                                                                                                                        tier3 = hourly_rate * OVERTIME_RATE_EXCESSIVE * (hours - OVERTIME_THRESHOLD_2)
                                                                                                                                                return truncate(tier1 + tier2 + tier3)
                                                                                                                                                
                                                                                                                                                
                                                                                                                                                def calculate_late_night_allowance(hourly_rate: int, hours: float) -> int:
                                                                                                                                                    """深夜残業手当を計算（+0.25倍の追加分）"""
