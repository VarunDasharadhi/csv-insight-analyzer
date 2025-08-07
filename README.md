# 📊 CSV Insight Analyzer

A powerful and beginner-friendly web app built with **Streamlit** that allows users to upload messy or clean CSV files and instantly get deep insights — including:

✅ Column types  
✅ Missing values  
✅ Numeric stats (mean, median, std, etc.)  
✅ Categorical breakdowns  
✅ Data visualizations (histograms & bar charts)  
✅ PDF export report (with embedded graphs!)  
✅ Auto-fix support for tab/pipe/semicolon-separated messy files

---

## 🚀 Features

- **Robust CSV Reader**: Auto-detects delimiter & encoding
- **Clean Summary View**: Rows, columns, nulls, dtypes
- **Visual Analysis**: Histograms & bar charts (Matplotlib + Seaborn)
- **PDF Report Export**: All insights + visual charts included
- **Streamlit UI**: Clean, interactive & responsive

---

## 📷 Screenshots

![Upload and Preview](https://your-screenshot-link.com)
![Stats and Charts](https://your-screenshot-link.com)
*(Replace with real screenshots after deployment)*

---

## 🧠 Tech Stack

- `Python`
- `Pandas`
- `Matplotlib`, `Seaborn`
- `Streamlit`
- `ReportLab` (for PDF generation)

---

## 🛠 How to Run Locally

```bash
git clone https://github.com/VarunDasharadhi/csv-insight-analyzer.git
cd csv-insight-analyzer
pip install -r requirements.txt
streamlit run app.py
