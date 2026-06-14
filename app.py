import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Sales Agent Performance Dashboard", layout="wide", page_icon="📊")

# ── Load Data ──
@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv")
    return df

df = load_data()

month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)

# ── Sidebar ──
st.sidebar.image("https://img.icons8.com/color/96/combo-chart.png", width=60)
st.sidebar.title("Filters")
selected_region = st.sidebar.multiselect("Region", options=df["Region"].unique(), default=df["Region"].unique())
selected_month = st.sidebar.multiselect("Month", options=month_order, default=month_order)
selected_agent = st.sidebar.multiselect("Agent", options=df["Agent"].unique(), default=df["Agent"].unique())

filtered = df[
    df["Region"].isin(selected_region) &
    df["Month"].isin(selected_month) &
    df["Agent"].isin(selected_agent)
]

# ── Header ──
st.title("📊 Sales Agent Performance Dashboard")
st.caption("Banca ASNB — Agent KPI Tracker | Anonymised Demo Dataset")
st.divider()

# ── KPI Cards ──
col1, col2, col3, col4 = st.columns(4)
total_sales = filtered["Actual Sales (RM)"].sum()
total_target = filtered["Target (RM)"].sum()
avg_achievement = filtered["Achievement (%)"].mean()
top_agent = filtered.groupby("Agent")["Actual Sales (RM)"].sum().idxmax()

col1.metric("💰 Total Sales", f"RM {total_sales:,.0f}")
col2.metric("🎯 Total Target", f"RM {total_target:,.0f}")
col3.metric("📈 Avg Achievement", f"{avg_achievement:.1f}%")
col4.metric("🏆 Top Agent", top_agent)

st.divider()

# ── Row 1: Sales Trend + Achievement by Region ──
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Monthly Sales Trend")
    monthly = filtered.groupby("Month", observed=True)[["Actual Sales (RM)", "Target (RM)"]].sum().reset_index()
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=monthly["Month"], y=monthly["Actual Sales (RM)"], name="Actual Sales", marker_color="#C0392B"))
    fig1.add_trace(go.Scatter(x=monthly["Month"], y=monthly["Target (RM)"], name="Target", mode="lines+markers", line=dict(color="#1F4E79", width=2, dash="dash")))
    fig1.update_layout(height=350, legend=dict(orientation="h", y=-0.2), margin=dict(t=10, b=10))
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.subheader("Achievement % by Region")
    region_df = filtered.groupby("Region")["Achievement (%)"].mean().reset_index().sort_values("Achievement (%)", ascending=True)
    fig2 = px.bar(region_df, x="Achievement (%)", y="Region", orientation="h",
                  color="Achievement (%)", color_continuous_scale=["#E74C3C", "#F39C12", "#27AE60"],
                  range_color=[60, 130])
    fig2.add_vline(x=100, line_dash="dash", line_color="#1F4E79", annotation_text="Target 100%")
    fig2.update_layout(height=350, margin=dict(t=10, b=10), coloraxis_showscale=False)
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Top Agents + Status Distribution ──
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Top 10 Agents by Total Sales")
    top10 = filtered.groupby("Agent")["Actual Sales (RM)"].sum().nlargest(10).reset_index()
    top10 = top10.sort_values("Actual Sales (RM)", ascending=True)
    fig3 = px.bar(top10, x="Actual Sales (RM)", y="Agent", orientation="h",
                  color="Actual Sales (RM)", color_continuous_scale=["#AED6F1", "#1F4E79"])
    fig3.update_layout(height=350, margin=dict(t=10, b=10), coloraxis_showscale=False)
    st.plotly_chart(fig3, use_container_width=True)

with col_d:
    st.subheader("Performance Status Distribution")
    status_df = filtered["Status"].value_counts().reset_index()
    status_df.columns = ["Status", "Count"]
    color_map = {"Exceeded": "#27AE60", "Achieved": "#F39C12", "Below Target": "#E74C3C"}
    fig4 = px.pie(status_df, names="Status", values="Count",
                  color="Status", color_discrete_map=color_map, hole=0.4)
    fig4.update_layout(height=350, margin=dict(t=10, b=10))
    st.plotly_chart(fig4, use_container_width=True)

# ── Row 3: Agent Detail Table ──
st.divider()
st.subheader("📋 Agent Detail Table")
summary = filtered.groupby(["Agent", "Region"]).agg(
    Total_Sales=("Actual Sales (RM)", "sum"),
    Total_Target=("Target (RM)", "sum"),
    Avg_Achievement=("Achievement (%)", "mean"),
    Accounts_Opened=("Accounts Opened", "sum"),
    Customer_Visits=("Customer Visits", "sum")
).reset_index()
summary["Avg_Achievement"] = summary["Avg_Achievement"].round(1)
summary = summary.sort_values("Total_Sales", ascending=False)
summary.columns = ["Agent", "Region", "Total Sales (RM)", "Total Target (RM)", "Avg Achievement (%)", "Accounts Opened", "Customer Visits"]

def highlight_achievement(val):
    if val >= 110:
        return "background-color: #D5F5E3; color: #1E8449"
    elif val >= 90:
        return "background-color: #FEF9E7; color: #B7950B"
    else:
        return "background-color: #FDEDEC; color: #922B21"

styled = summary.style.applymap(highlight_achievement, subset=["Avg Achievement (%)"])\
    .format({"Total Sales (RM)": "RM {:,.0f}", "Total Target (RM)": "RM {:,.0f}", "Avg Achievement (%)": "{:.1f}%"})
st.dataframe(styled, use_container_width=True, height=400)

# ── Download ──
csv = summary.to_csv(index=False)
st.download_button("⬇️ Download Agent Report (CSV)", csv, "agent_report.csv", "text/csv")

st.caption("Dashboard built with Python · pandas · Plotly · Streamlit | By Farah Annisa")
