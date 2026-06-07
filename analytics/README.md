# analytics — 班級成績快速分析

一個輕量級 Python 腳本，協助教師在批改後迅速掌握班級表現：

- 找出全班達標率偏低的題目（達標 = 拿到該題六成或以上分數）
- 按總分排出學生名次
- 不依賴任何雲端服務或封閉系統，CSV 入、文字出

## 跑法

需要 Python 3.10+ 與 `pandas`。

```bash
pip install pandas
python analyze_grades.py --csv sample_grades.csv --class 3A
```

可選 `--threshold 0.5` 收緊達標警示。

## CSV 格式

```
student_id,class,Q1,Q2,Q3,Q4,Q5
S01,3A,8,7,10,3,9
...
```

題目欄以 `Q` 開頭即可，數量任意，腳本自動偵測。

## 設計取向

- 一個檔案、約 70 行，方便交班同事接手或自行修改
- 不寫入磁碟（除非另外重定向），不上載任何外部服務
- 配合學校現有的 Excel 工作流程，腳本只負責「分析」這一步
