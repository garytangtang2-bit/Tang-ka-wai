"""analyze_grades.py — 班級成績快速分析腳本

讀取一份學生分題得分 CSV，輸出：
  1. 各題的「達標率」(以滿分 60% 為達標門檻)
  2. 達標率低於 threshold 的題目 (建議重點回顧)
  3. 學生總分與排名

用法:
    python analyze_grades.py --csv sample_grades.csv --class 3A
    python analyze_grades.py --csv sample_grades.csv --class 3A --threshold 0.5
"""

from __future__ import annotations

import argparse
import sys

import pandas as pd


def analyze(csv_path: str, class_id: str, threshold: float = 0.4) -> None:
    df = pd.read_csv(csv_path)
    df_class = df[df["class"] == class_id]
    if df_class.empty:
        sys.exit(f"[error] no rows for class={class_id} in {csv_path}")

    question_cols = [c for c in df_class.columns if c.startswith("Q")]
    full_marks = {q: df_class[q].max() for q in question_cols}

    rates = {}
    for q in question_cols:
        pass_score = full_marks[q] * 0.6
        rates[q] = (df_class[q] >= pass_score).mean()

    rate_df = (
        pd.DataFrame.from_dict(rates, orient="index", columns=["mastery_rate"])
        .sort_values("mastery_rate")
    )

    print(f"\n=== Class {class_id} — per-question mastery rate ===")
    print(rate_df.to_string(float_format="{:.1%}".format))

    weak = rate_df[rate_df["mastery_rate"] < threshold]
    print(f"\n=== Alert: questions below {threshold:.0%} mastery ===")
    if weak.empty:
        print("  (none — class meets minimum mastery on all questions)")
    else:
        for q in weak.index:
            print(f"  - {q}: {weak.loc[q, 'mastery_rate']:.1%} (needs review)")

    df_ranked = df_class.copy()
    df_ranked["total"] = df_ranked[question_cols].sum(axis=1)
    df_ranked["rank"] = (
        df_ranked["total"].rank(ascending=False, method="min").astype(int)
    )

    print(f"\n=== Class {class_id} — student standing ===")
    print(
        df_ranked[["student_id", "total", "rank"]]
        .sort_values("rank")
        .to_string(index=False)
    )


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--csv", required=True, help="path to grades CSV")
    p.add_argument("--class", dest="class_id", required=True, help="class id, e.g. 3A")
    p.add_argument("--threshold", type=float, default=0.4, help="mastery alert threshold")
    args = p.parse_args()
    analyze(args.csv, args.class_id, args.threshold)


if __name__ == "__main__":
    main()
