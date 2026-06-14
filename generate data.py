import pandas as pd
import numpy as np

np.random.seed(42)

agents = [
    "Ahmad Razif", "Siti Norzah", "Muhd Hafiz", "Nurul Ain", "Zainudin Malik",
    "Faizah Othman", "Khairul Azman", "Rohani Jusoh", "Syafiq Nadzri", "Aina Liyana",
    "Hasrul Nizam", "Noraini Hamid", "Firdaus Kamal", "Suraya Zainal", "Azri Hisham"
]

regions = {
    "Ahmad Razif": "Kuala Lumpur", "Siti Norzah": "Selangor", "Muhd Hafiz": "Johor",
    "Nurul Ain": "Kuala Lumpur", "Zainudin Malik": "Penang", "Faizah Othman": "Selangor",
    "Khairul Azman": "Johor", "Rohani Jusoh": "Perak", "Syafiq Nadzri": "Kuala Lumpur",
    "Aina Liyana": "Selangor", "Hasrul Nizam": "Penang", "Noraini Hamid": "Johor",
    "Firdaus Kamal": "Perak", "Suraya Zainal": "Kuala Lumpur", "Azri Hisham": "Selangor"
}

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

targets = {agent: np.random.randint(80000, 150000) for agent in agents}

records = []
for agent in agents:
    for month in months:
        target = targets[agent]
        actual = int(target * np.random.uniform(0.6, 1.3))
        records.append({
            "Agent": agent,
            "Region": regions[agent],
            "Month": month,
            "Target (RM)": target,
            "Actual Sales (RM)": actual,
            "Accounts Opened": np.random.randint(5, 40),
            "Customer Visits": np.random.randint(20, 80),
        })

df = pd.DataFrame(records)
df["Achievement (%)"] = (df["Actual Sales (RM)"] / df["Target (RM)"] * 100).round(1)
df["Status"] = df["Achievement (%)"].apply(
    lambda x: "Exceeded" if x >= 110 else ("Achieved" if x >= 90 else "Below Target")
)
df.to_csv("/home/claude/sales_dashboard/sales_data.csv", index=False)
print("Dataset generated:")
print(df.head())
print(df.shape)
