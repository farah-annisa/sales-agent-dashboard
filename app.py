import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Sales Performance Command Centre", layout="wide", page_icon="📊")

st.markdown("""
<style>
/* Global */
html, body, [class*="css"] {font-family: 'Segoe UI', sans-serif;}
[data-testid="stAppViewContainer"] {background-color: #0A1628;}
[data-testid="stHeader"] {background-color: #0A1628;}
[data-testid="block-container"] {padding: 1.5rem 2rem;}

/* Sidebar */
[data-testid="stSidebar"] {background-color: #0D1F3C; border-right: 1px solid #C9A84C;}
[data-testid="stSidebar"] * {color: #E8E8E8 !important;}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label {color: #C9A84C !important; font-weight: 600; font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase;}
[data-testid="stSidebar"] [data-baseweb="tag"] {background-color: #C9A84C !important; color: #0A1628 !important;}

/* Text */
h1, h2, h3 {color: #FFFFFF !important;}
p, span, div {color: #C8D0DC;}
.stCaption {color: #7A8BA0 !important;}

/* KPI Cards */
.kpi-card {
    background: linear-gradient(135deg, #0D1F3C 0%, #132847 100%);
    border: 1px solid #C9A84C;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 8px;
}
.kpi-label {color: #C9A84C; font-size: 11px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 6px;}
.kpi-value {color: #FFFFFF; font-size: 28px; font-weight: 700; line-height: 1.1;}
.kpi-sub {color: #7A8BA0; font-size: 12px; margin-top: 4px;}
.kpi-positive {color: #2ECC71; font-size: 12px; font-weight: 600;}
.kpi-negative {color: #E74C3C; font-size: 12px; font-weight: 600;}

/* Section headers */
.section-header {
    color: #C9A84C;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    border-bottom: 1px solid #1E3A5F;
    padding-bottom: 8px;
    margin-bottom: 16px;
}

/* Metric override */
[data-testid="metric-container"] {
    background: #0D1F3C;
    border: 1px solid #1E3A5F;
    border-radius: 8px;
    padding: 12px;
}
[data-testid="stMetricValue"] {color: #FFFFFF !important;}
[data-testid="stMetricLabel"] {color: #C9A84C !important;}

/* Divider */
hr {border-color: #1E3A5F !important;}

/* Dataframe */
[data-testid="stDataFrame"] {border: 1px solid #1E3A5F; border-radius: 8px;}

/* Download button */
.stDownloadButton button {
    background-color: #C9A84C !important;
    color: #0A1628 !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 6px !important;
}
</style>
""", unsafe_allow_html=True)

NAVY = "#0D1F3C"
GOLD = "#C9A84C"
LIGHT_NAVY = "#132847"
WHITE = "#FFFFFF"
GREEN = "#2ECC71"
RED = "#E74C3C"
AMBER = "#F39C12"
GRAY = "#7A8BA0"

@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "sales_data.csv")
    return pd.read_csv(path)

df = load_data()
month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown(f"<div style='color:{GOLD};font-size:18px;font-weight:700;letter-spacing:0.05em;padding:12px 0 4px;'>⚡ COMMAND CENTRE</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:{GRAY};font-size:11px;padding-bottom:16px;border-bottom:1px solid #1E3A5F;'>Banca ASNB · Sales Intelligence</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(f"<div style='color:{GOLD};font-size:10px;font-weight:700;letter-spacing:0.12em;'>🗺 REGION</div>", unsafe_allow_html=True)
    all_regions = sorted(df["Region"].unique())
    selected_region = st.multiselect("", options=all_regions, default=all_regions, label_visibility="collapsed", key="reg")

    st.markdown(f"<div style='color:{GOLD};font-size:10px;font-weight:700;letter-spacing:0.12em;margin-top:16px;'>📅 MONTH</div>", unsafe_allow_html=True)
    selected_month = st.multiselect("", options=month_order, default=month_order, label_visibility="collapsed", key="mon")

    st.markdown(f"<div style='color:{GOLD};font-size:10px;font-weight:700;letter-spacing:0.12em;margin-top:16px;'>👤 AGENT</div>", unsafe_allow_html=True)
    all_agents = sorted(df["Agent"].unique())
    selected_agent = st.multiselect("", options=all_agents, default=all_agents, label_visibility="collapsed", key="agt")

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"<div style='color:{GRAY};font-size:10px;border-top:1px solid #1E3A5F;padding-top:12px;'>Built by Farah Annisa<br>Master of Data Science · UM</div>", unsafe_allow_html=True)

filtered = df[
    df["Region"].isin(selected_region) &
    df["Month"].isin(selected_month) &
    df["Agent"].isin(selected_agent)
]

# ── Header ──
st.markdown(f"""
<div style='margin-bottom:8px;'>
    <div style='color:{GOLD};font-size:11px;font-weight:700;letter-spacing:0.2em;'>BANCA ASNB · SALES INTELLIGENCE PLATFORM</div>
    <div style='color:{WHITE};font-size:30px;font-weight:700;line-height:1.2;margin:4px 0;'>Sales Performance Command Centre</div>
    <div style='color:{GRAY};font-size:13px;'>Real-time KPI monitoring · Agent achievement tracking · Regional analysis</div>
</div>
""", unsafe_allow_html=True)
st.divider()

# ── KPI Row ──
total_sales = filtered["Actual Sales (RM)"].sum()
total_target = filtered["Target (RM)"].sum()
overall_achievement = (total_sales / total_target * 100) if total_target > 0 else 0
top_agent = filtered.groupby("Agent")["Actual Sales (RM)"].sum().idxmax()
top_agent_sales = filtered.groupby("Agent")["Actual Sales (RM)"].sum().max()
exceeded_count = filtered[filtered["Status"] == "Exceeded"]["Agent"].nunique()
below_count = filtered[filtered["Status"] == "Below Target"]["Agent"].nunique()
total_accounts = filtered["Accounts Opened"].sum()
avg_achievement = filtered["Achievement (%)"].mean()

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-label'>Total Sales</div>
        <div class='kpi-value'>RM {total_sales/1e6:.2f}M</div>
        <div class='kpi-sub'>vs Target RM {total_target/1e6:.2f}M</div>
    </div>""", unsafe_allow_html=True)

with col2:
    color = GREEN if overall_achievement >= 100 else (AMBER if overall_achievement >= 90 else RED)
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-label'>Overall Achievement</div>
        <div class='kpi-value' style='color:{color};'>{overall_achievement:.1f}%</div>
        <div class='kpi-sub'>Team average: {avg_achievement:.1f}%</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-label'>🏆 Top Agent</div>
        <div class='kpi-value' style='font-size:18px;'>{top_agent}</div>
        <div class='kpi-sub'>RM {top_agent_sales:,.0f}</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-label'>Agents Exceeded Target</div>
        <div class='kpi-value' style='color:{GREEN};'>{exceeded_count}</div>
        <div class='kpi-sub' style='color:{RED};'>{below_count} below target</div>
    </div>""", unsafe_allow_html=True)

with col5:
    st.markdown(f"""<div class='kpi-card'>
        <div class='kpi-label'>Total Accounts Opened</div>
        <div class='kpi-value'>{total_accounts:,}</div>
        <div class='kpi-sub'>Across {filtered["Agent"].nunique()} agents</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Achievement Gauge + Monthly Trend ──
col_a, col_b = st.columns([1, 2])

with col_a:
    st.markdown("<div class='section-header'>ACHIEVEMENT GAUGE</div>", unsafe_allow_html=True)
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=overall_achievement,
        delta={"reference": 100, "valueformat": ".1f", "suffix": "%"},
        number={"suffix": "%", "font": {"size": 36, "color": WHITE}},
        gauge={
            "axis": {"range": [0, 150], "tickcolor": GRAY, "tickfont": {"color": GRAY}},
            "bar": {"color": GOLD, "thickness": 0.25},
            "bgcolor": LIGHT_NAVY,
            "bordercolor": GOLD,
            "steps": [
                {"range": [0, 90], "color": "#1A0A0A"},
                {"range": [90, 110], "color": "#0A1A0A"},
                {"range": [110, 150], "color": "#0A150A"},
            ],
            "threshold": {"line": {"color": WHITE, "width": 2}, "thickness": 0.75, "value": 100}
        }
    ))
    fig_gauge.update_layout(
        height=280, margin=dict(t=20, b=10, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)", font={"color": WHITE}
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_b:
    st.markdown("<div class='section-header'>MONTHLY SALES vs TARGET</div>", unsafe_allow_html=True)
    monthly = filtered.groupby("Month", observed=True)[["Actual Sales (RM)", "Target (RM)"]].sum().reset_index()
    monthly["Gap"] = monthly["Actual Sales (RM)"] - monthly["Target (RM)"]
    fig_monthly = go.Figure()
    fig_monthly.add_trace(go.Bar(
        x=monthly["Month"], y=monthly["Actual Sales (RM)"],
        name="Actual Sales", marker_color=GOLD, opacity=0.9
    ))
    fig_monthly.add_trace(go.Scatter(
        x=monthly["Month"], y=monthly["Target (RM)"],
        name="Target", mode="lines+markers",
        line=dict(color=WHITE, width=2, dash="dot"),
        marker=dict(size=6, color=WHITE)
    ))
    fig_monthly.update_layout(
        height=280, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"color": GRAY}, legend=dict(orientation="h", y=-0.25, font=dict(color=GRAY)),
        xaxis=dict(gridcolor="#1E3A5F", tickfont=dict(color=GRAY)),
        yaxis=dict(gridcolor="#1E3A5F", tickfont=dict(color=GRAY), tickformat=",.0f"),
        margin=dict(t=10, b=10)
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

st.divider()

# ── Agent Leaderboard + Region ──
col_c, col_d = st.columns([3, 2])

with col_c:
    st.markdown("<div class='section-header'>AGENT ACHIEVEMENT LEADERBOARD</div>", unsafe_allow_html=True)
    leaderboard = filtered.groupby("Agent").agg(
        Total_Sales=("Actual Sales (RM)", "sum"),
        Total_Target=("Target (RM)", "sum"),
        Avg_Achievement=("Achievement (%)", "mean")
    ).reset_index()
    leaderboard["Achievement"] = (leaderboard["Total_Sales"] / leaderboard["Total_Target"] * 100).round(1)
    leaderboard = leaderboard.sort_values("Achievement", ascending=True)
    leaderboard["Color"] = leaderboard["Achievement"].apply(
        lambda x: GREEN if x >= 110 else (AMBER if x >= 90 else RED)
    )
    fig_lb = go.Figure()
    fig_lb.add_trace(go.Bar(
        x=leaderboard["Achievement"], y=leaderboard["Agent"],
        orientation="h",
        marker_color=leaderboard["Color"],
        text=leaderboard["Achievement"].apply(lambda x: f"{x:.1f}%"),
        textposition="outside", textfont=dict(color=WHITE, size=11)
    ))
    fig_lb.add_vline(x=100, line_dash="dash", line_color=WHITE, line_width=1,
                     annotation_text="100% Target", annotation_font_color=GOLD, annotation_font_size=10)
    fig_lb.update_layout(
        height=420, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font={"color": GRAY},
        xaxis=dict(gridcolor="#1E3A5F", tickfont=dict(color=GRAY), range=[0, 160]),
        yaxis=dict(tickfont=dict(color=WHITE, size=11)),
        margin=dict(t=10, b=10, r=60)
    )
    st.plotly_chart(fig_lb, use_container_width=True)

with col_d:
    st.markdown("<div class='section-header'>REGIONAL BREAKDOWN</div>", unsafe_allow_html=True)
    region_df = filtered.groupby("Region").agg(
        Total_Sales=("Actual Sales (RM)", "sum"),
        Avg_Achievement=("Achievement (%)", "mean")
    ).reset_index().sort_values("Total_Sales", ascending=False)

    fig_region = go.Figure(go.Pie(
        labels=region_df["Region"],
        values=region_df["Total_Sales"],
        hole=0.55,
        marker=dict(colors=[GOLD, "#E8C97A", "#A07830", "#6B5020", "#3D2E10"],
                    line=dict(color=NAVY, width=2)),
        textfont=dict(color=WHITE, size=11),
        textinfo="label+percent"
    ))
    fig_region.add_annotation(
        text=f"<b>RM {total_sales/1e6:.1f}M</b><br><span style='font-size:10px'>Total</span>",
        x=0.5, y=0.5, showarrow=False, font=dict(color=WHITE, size=13), align="center"
    )
    fig_region.update_layout(
        height=240, paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False, margin=dict(t=10, b=10)
    )
    st.plotly_chart(fig_region, use_container_width=True)

    st.markdown("<div class='section-header' style='margin-top:8px;'>STATUS SPLIT</div>", unsafe_allow_html=True)
    status_counts = filtered.groupby("Status")["Agent"].nunique().reset_index()
    status_counts.columns = ["Status", "Count"]
    color_map = {"Exceeded": GREEN, "Achieved": AMBER, "Below Target": RED}
    for _, row in status_counts.iterrows():
        pct = row["Count"] / status_counts["Count"].sum() * 100
        c = color_map.get(row["Status"], GRAY)
        st.markdown(f"""
        <div style='display:flex;justify-content:space-between;align-items:center;
                    background:{LIGHT_NAVY};border-left:3px solid {c};
                    padding:8px 12px;border-radius:4px;margin-bottom:6px;'>
            <span style='color:{WHITE};font-size:12px;'>{row["Status"]}</span>
            <span style='color:{c};font-weight:700;font-size:13px;'>{row["Count"]} agents</span>
        </div>""", unsafe_allow_html=True)

st.divider()

# ── Detail Table ──
st.markdown("<div class='section-header'>FULL AGENT PERFORMANCE TABLE</div>", unsafe_allow_html=True)
summary = filtered.groupby(["Agent", "Region"]).agg(
    Total_Sales=("Actual Sales (RM)", "sum"),
    Total_Target=("Target (RM)", "sum"),
    Avg_Achievement=("Achievement (%)", "mean"),
    Accounts_Opened=("Accounts Opened", "sum"),
    Customer_Visits=("Customer Visits", "sum")
).reset_index()
summary["Avg_Achievement"] = summary["Avg_Achievement"].round(1)
summary["Conversion Rate (%)"] = (summary["Accounts_Opened"] / summary["Customer_Visits"] * 100).round(1)
summary = summary.sort_values("Total_Sales", ascending=False)
summary.columns = ["Agent", "Region", "Total Sales (RM)", "Total Target (RM)",
                   "Avg Achievement (%)", "Accounts Opened", "Customer Visits", "Conversion Rate (%)"]

def highlight(val):
    if val >= 110: return "background-color: #0A2A0A; color: #2ECC71; font-weight:600"
    elif val >= 90: return "background-color: #2A1A0A; color: #F39C12; font-weight:600"
    else: return "background-color: #2A0A0A; color: #E74C3C; font-weight:600"

styled = summary.style.map(highlight, subset=["Avg Achievement (%)"])\
    .format({"Total Sales (RM)": "RM {:,.0f}", "Total Target (RM)": "RM {:,.0f}",
             "Avg Achievement (%)": "{:.1f}%", "Conversion Rate (%)": "{:.1f}%"})
st.dataframe(styled, use_container_width=True, height=420)

col_dl, col_empty = st.columns([1, 4])
with col_dl:
    csv = summary.to_csv(index=False)
    st.download_button("⬇️ Export Report (CSV)", csv, "agent_performance_report.csv", "text/csv")

st.markdown(f"<br><div style='color:{GRAY};font-size:11px;text-align:center;border-top:1px solid #1E3A5F;padding-top:12px;'>Sales Performance Command Centre · Built by Farah Annisa · Master of Data Science, Universiti Malaya</div>", unsafe_allow_html=True)
