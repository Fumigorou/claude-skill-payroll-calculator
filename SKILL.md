---
name: payroll-calculator
description: |
  【必須スキル - MANDATORY】給与計算関連のタスクでは必ずこのスキルを使用してください。

    ⚠️ 重要: LLM推論による手動計算は禁止です。必ずscripts/calculate_payroll.pyを実行してください。
      手動計算は端数処理（円未満切り捨て）で必ずエラーが発生します。

        🎯 トリガーキーワード（以下のいずれかを含む場合は必ずこのスキルを使用）:
          - 日本語: 給与計算, 給料計算, 賃金計算, 残業手当, 深夜手当, 休日手当,
              社会保険料, 所得税, 差引支給額, 手取り, 基本給, 時間単価, 欠勤控除, 遅刻控除,
                  給与明細, 給与シミュレーション, 給与試算
                    - English: payroll, salary calculation, overtime pay, allowance, deduction,
                        social insurance, income tax, net pay, gross pay, hourly rate

                          機能: 複雑な給与計算を正確に実行。残業手当（45h/60h閾値の段階計算）、
                            深夜・休日手当、等級別社会保険料、累進課税、欠勤・遅刻控除を処理。
                              シート間参照を活用したExcelスプレッドシートを生成。
                              version: 1.0.1
                              ---

                              # 給与計算スキル（Payroll Calculator）

                              ## ⚠️ 最重要注意事項

                              **このスキルは必ずPythonスクリプトを実行して計算してください。**

                              ❌ やってはいけないこと:
                              - LLMの推論で給与計算をする
                              - 頭の中で計算する
                              - 計算式を書いて手動で答えを出す

                              ✅ 必ずやること:
                              - `scripts/calculate_payroll.py` を実行する
                              - 出力されたJSONの値をそのまま使用する

                              **理由**: LLMは端数処理（円未満切り捨て）を正確に適用できません。
                              例: 350,000÷160 = 2,187.5 → 正解は2,187（切り捨て）
                              LLMは2,187.5のまま次の計算に進み、誤差が累積します。

                              ## Overview

                              このスキルは、日本の企業で発生する複雑な給与計算を**正確に**実行します。
                              AIが計算を間違えやすい複雑な条件分岐を、Pythonスクリプトで確実に処理します。

                              ## 重要な原則

                              1. **計算は必ずPythonスクリプトで実行** - AIの推論による計算ミスを防止（必須）
                              2. **段階的な検証** - 各ステップで計算結果を検証
                              3. **シート間参照を活用** - Excel数式でトレーサビリティを確保

                              ## 使用場面（トリガー条件）

                              以下のキーワードがユーザーのリクエストに含まれる場合、**必ず**このスキルを使用:

                              - 「給与計算」「給料計算」「賃金計算」
                              - 「残業手当」「深夜手当」「休日手当」
                              - 「社会保険料」「所得税」「住民税」
                              - 「差引支給額」「手取り」「控除」
                              - 「基本給」「時間単価」
                              - 「欠勤」「遅刻」「早退」
                              - "payroll", "salary", "overtime", "allowance", "deduction"
                              - 複数の残業区分（45h以下、45-60h、60h超）がある給与計算
                              - 等級別の社会保険料率が異なる場合
                              - 累進課税の計算が必要な場合
                              - 欠勤・遅刻による控除がある場合
                              - シート間連携が必要なExcelファイルを生成する場合

                              ## 実行手順

                              ### Step 1: 入力データの準備

                              以下のJSON形式で従業員データを準備します：

                              ```json
                              {
                                "employees": [
                                    {
                                          "id": "E001",
                                                "name": "田中一郎",
                                                      "department": "営業部",
                                                            "grade": "G3",
                                                                  "base_salary": 350000,
                                                                        "dependents": 2,
                                                                              "commute_allowance": 15000
                                                                                  }
                                                                                    ],
                                                                                      "attendance": [
                                                                                          {
                                                                                                "employee_id": "E001",
                                                                                                      "regular_overtime_hours": 25,
                                                                                                            "late_night_overtime_hours": 8,
                                                                                                                  "holiday_work_hours": 12,
                                                                                                                        "holiday_late_night_hours": 4,
                                                                                                                              "absence_days": 2,
                                                                                                                                    "tardiness_count": 3
                                                                                                                                        }
                                                                                                                                          ],
                                                                                                                                            "grade_table": {
                                                                                                                                                "G1": {"insurance_rate": 0.145, "base_deduction": 5000},
                                                                                                                                                    "G2": {"insurance_rate": 0.145, "base_deduction": 5000},
                                                                                                                                                        "G3": {"insurance_rate": 0.150, "base_deduction": 8000},
                                                                                                                                                            "G4": {"insurance_rate": 0.150, "base_deduction": 8000},
                                                                                                                                                                "G5": {"insurance_rate": 0.155, "base_deduction": 10000}
                                                                                                                                                                  }
                                                                                                                                                                  }
                                                                                                                                                                  ```
                                                                                                                                                                  
                                                                                                                                                                  ### Step 2: 計算の実行
                                                                                                                                                                  
                                                                                                                                                                  Pythonスクリプトを使用して計算を実行します：
                                                                                                                                                                  
                                                                                                                                                                  ```bash
                                                                                                                                                                  python scripts/calculate_payroll.py input.json output.json
                                                                                                                                                                  ```
                                                                                                                                                                  
                                                                                                                                                                  ### Step 3: Excelファイルの生成
                                                                                                                                                                  
                                                                                                                                                                  計算結果からExcelファイルを生成します：
                                                                                                                                                                  
                                                                                                                                                                  ```bash
                                                                                                                                                                  python scripts/generate_excel.py output.json payroll.xlsx
                                                                                                                                                                  ```
                                                                                                                                                                  
                                                                                                                                                                  ## 計算ルール詳細
                                                                                                                                                                  
                                                                                                                                                                  詳細な計算ルールは [references/calculation-rules.md](references/calculation-rules.md) を参照してください。
                                                                                                                                                                  
                                                                                                                                                                  ## 検証方法
                                                                                                                                                                  
                                                                                                                                                                  計算結果を検証するには：
                                                                                                                                                                  
                                                                                                                                                                  ```bash
                                                                                                                                                                  python scripts/verify_results.py output.json expected.json
                                                                                                                                                                  ```
                                                                                                                                                                  
                                                                                                                                                                  ## トラブルシューティング
                                                                                                                                                                  
                                                                                                                                                                  問題が発生した場合は [references/troubleshooting.md](references/troubleshooting.md) を参照してください。
                                                                                                                                                                  
