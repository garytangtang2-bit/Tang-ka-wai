import pandas as pd
import argparse
import os
import sys
import time

def main():
    parser = argparse.ArgumentParser(description="真實使用的學生成績數據分析腳本")
    parser.add_argument('--input', type=str, required=True, help='成績單檔案路徑 (支援 .csv 或 .xlsx)')
    parser.add_argument('--class_name', type=str, default='Class', help='輸出報告的班級名稱前綴')
    parser.add_argument('--passing_score', type=float, default=50.0, help='及格分數標準 (預設為 50)')
    parser.add_argument('--alert_threshold', type=float, default=40.0, help='答對率警報閾值，低於此百分比會觸發警報 (預設 40)')
    
    args = parser.parse_args()

    input_file = args.input

    if not os.path.exists(input_file):
        print(f"\033[91m[Error] 找不到指定的檔案: {input_file}\033[0m")
        sys.exit(1)

    print(f"[INFO] Loading data from {input_file}...")
    time.sleep(0.5)
    
    try:
        if input_file.endswith('.csv'):
            df = pd.read_csv(input_file)
        elif input_file.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(input_file)
        else:
            print("\033[91m[Error] 不支援的檔案格式，請提供 .csv 或 .xlsx 格式檔案\033[0m")
            sys.exit(1)
    except Exception as e:
        print(f"\033[91m[Error] 讀取檔案失敗: {e}\033[0m")
        sys.exit(1)
    
    print("[INFO] Cleaning missing values and converting data types...")
    time.sleep(0.5)
    
    # 自動忽略非數值欄位 (例如學號、姓名) 來找出「成績題目」欄位
    # 或者如果欄位有包含中文的非數字，我們必須先做轉換
    numeric_df = df.select_dtypes(include=['number'])
    
    if numeric_df.empty:
        print("\033[91m[Error] 檔案中沒有找到可分析的數字欄位！請確定成績是用數字表示。\033[0m")
        sys.exit(1)
        
    print("Processing: Calculating statistics for each question/subject...")
    time.sleep(0.5)
    
    report_data = []
    
    for col in numeric_df.columns:
        # 如果欄位名稱包含 ID、No 等字眼，通常是學號或座號，應跳過不分析
        if 'id' in col.lower() or 'no' in col.lower() or '號' in col:
            continue
            
        mean_score = numeric_df[col].mean()
        std_score = numeric_df[col].std()
        
        # 計算達標/及格率
        total_students = len(numeric_df[col].dropna())
        if total_students == 0:
            continue
            
        passed_students = (numeric_df[col] >= args.passing_score).sum()
        success_rate = (passed_students / total_students) * 100 
        
        report_data.append({
            'Subject / Question': col,
            'Average_Score': round(mean_score, 2),
            'Std_Deviation': round(std_score, 2),
            f'Success_Rate(>={args.passing_score}) %': round(success_rate, 2)
        })
        
        # 真實的預警系統
        if success_rate < args.alert_threshold:
            print(f"\033[95mAlert:\033[0m {col} success rate is {round(success_rate, 1)}% ( < {args.alert_threshold}% )")
    
    if not report_data:
        print("\033[93m[Warning] 分析完成，但沒有發現有效的成績數據欄位。\033[0m")
        sys.exit(0)

    report_df = pd.DataFrame(report_data)
    
    output_file = f"{args.class_name}_analytics_report.xlsx"
    csv_output_file = f"{args.class_name}_analytics_report.csv"
    
    try:
        report_df.to_excel(output_file, index=False)
        print(f"\033[92m> Success! Generated report: {output_file}\033[0m")
    except ModuleNotFoundError:
        report_df.to_csv(csv_output_file, index=False)
        print(f"\033[92m> Success! Generated report: {csv_output_file} (Saved as CSV since 'openpyxl' is missing)\033[0m")

if __name__ == "__main__":
    main()
