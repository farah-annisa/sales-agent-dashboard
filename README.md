# 📊 Sales Agent Performance Dashboard

An end-to-end sales analytics project built with Python, pandas and Streamlit —
tracking KPIs, monthly trends and agent performance for a fictional Banca sales team.

-----

## 📌 Problem Statement

Sales managers need a fast, reliable way to monitor agent performance across regions,
identify top performers, and flag agents at risk of missing monthly targets — without
manually consolidating spreadsheets every reporting cycle.

This dashboard automates that process: load the data, get instant KPIs, trends and
rankings in one interactive view.

-----

## 🎯 What This Project Does

- Tracks **15 agents** across **5 regions** over **12 months**
- Computes KPIs: Total Sales, Achievement %, Accounts Opened, Customer Visits
- Flags agents as **Exceeded / Achieved / Below Target**
- Visualises monthly sales trends vs targets
- Ranks agents and regions by performance
- Exports agent summary report as CSV

-----

## 🛠 Tools & Technologies

|Category      |Tools                   |
|--------------|------------------------|
|Language      |Python 3.10             |
|Data Wrangling|pandas, NumPy           |
|Visualisation |Plotly                  |
|Dashboard     |Streamlit               |
|Data          |Anonymised dummy dataset|

-----

## 🔍 Key Insights

- Top-performing region consistently **exceeded 110% achievement** during mid-year months
- **Accounts Opened** correlates strongly with overall sales achievement
- Agents with high **Customer Visits** but low sales signal a conversion efficiency gap
- Monthly trend shows a **Q3 peak** driven by mid-year campaign periods

-----

## 📁 Repository Structure

```
sales-agent-dashboard/
│
├── app.py                  ← Streamlit dashboard
├── sales_data.csv          ← Anonymised agent dataset
├── generate_data.py        ← Script to regenerate dataset
├── requirements.txt        ← Python dependencies
└── README.md
```

-----

## 🚀 How to Run Locally

```bash
git clone https://github.com/Farah-Annisa/sales-agent-dashboard.git
cd sales-agent-dashboard
pip install -r requirements.txt
streamlit run app.py
```

-----

## 📸 Dashboard Preview

> *(Add screenshot here)*

-----

## 🎓 Academic & Professional Context

Built as part of a data analytics portfolio targeting **Data Analyst** and
**Sales Analyst** roles. Inspired by real sales agent management work at
Permodalan Nasional Berhad (PNB).

**Author:** Farah Annisa Binti Norhisham
**Programme:** Master of Data Science, Universiti Malaya
**LinkedIn:** [linkedin.com/in/farah-norhisham-88a3ab390](https://www.linkedin.com/in/farah-norhisham-88a3ab390)
