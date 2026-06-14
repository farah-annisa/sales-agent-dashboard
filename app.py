import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="LUX Beauty · Sales Command Centre", layout="wide", page_icon="💄")

st.markdown("""
<style>
html, body, [class*="css"] {font-family: 'Segoe UI', sans-serif;}
[data-testid="stAppViewContainer"] {background-color: #0A1628;}
[data-testid="stHeader"] {background-color: #0A1628;}
[data-testid="block-container"] {padding: 1.5rem 2rem;}

/* Sidebar */
[data-testid="stSidebar"] {background-color: #0D1F3C; border-right: 1px solid #C9A84C;}
[data-testid="stSidebar"] * {color: #E8E8E8 !important;}
[data-testid="stSidebar"] [data-baseweb="tag"] {background-color: #C9A84C !important; color: #0A1628 !important; font-weight:600;}
[data-testid="stSidebar"] [data-baseweb="select"] {background-color: #132847 !important; border-color: #1E3A5F !important;}

/* KPI Cards */
.kpi-card {
    background: linear-gradient(135deg, #0D1F3C 0%, #132847 100%);
    border: 1px solid #C9A84C;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 8px;
    min-height: 110px;
}
.kpi-label {color: #C9A84C; font-size: 10px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 8px;}
.kpi-value {color: #FFFFFF; font-size: 26px; font-weight: 700; line-height: 1.1;}
.kpi-sub {color: #7A8BA0; font-size: 11px; margin-top: 6px;}

.section-header {
    color: #C9A84C; font-size: 10px; font-weight: 700;
    letter-spacing: 0.18em; text-transform: uppercase;
    border-bottom: 1px solid #1E3A5F;
    padding-bottom: 8px; margin-bottom: 14px; margin-top: 4px;
}

/* Filter pills */
.filter-label {
    color: #C9A84C; font-size: 10px; font-weight: 700;
    letter-spacing: 0.12em; text-transform: uppercase;
    margin-bottom: 4px; margin-top: 14px; display: block;
}

hr {border-color: #1E3A5F !important;}
h1,h2,h3 {color: #FFFFFF !important;}
p, span, div {color: #C8D0DC;}
[data-testid="stDataFrame"] {border: 1px solid #1E3A5F; border-radius: 8px;}
.stDownloadButton button {
    background-color: #C9A84C !important; color: #0A1628 !important;
    font-weight: 700 !important; border: none !important; border-radius: 6px !important;
}
</style>
""", unsafe_allow_html=True)

NAVY="#0D1F3C"; GOLD="#C9A84C"; DARK="#0A1628"; LIGHT_NAVY="#132847"
WHITE="#FFFFFF"; GREEN="#2ECC71"; RED="#E74C3C"; AMBER="#F39C12"; GRAY="#7A8BA0"

@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "sales_data.csv")
    return pd.read_csv(path)

df = load_data()
month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
df["Month"] = pd.Categorical(df["Month"], categories=month_order, ordered=True)

# ── Sidebar ──
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center;padding:20px 0 16px;border-bottom:1px solid #1E3A5F;'>
        <div style='font-size:28px;'>💄</div>
        <div style='color:{GOLD};font-size:16px;font-weight:700;letter-spacing:0.08em;margin-top:4px;'>LUX BEAUTY</div>
        <div style='color:{GRAY};font-size:10px;letter-spacing:0.1em;margin-top:2px;'>SALES COMMAND CENTRE</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Region filter
    st.markdown(f"<span class='filter-label'>🗺 Region</span>", unsafe_allow_html=True)
    all_regions = sorted(df["Region"].unique())
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("All", key="r_all", use_container_width=True):
            st.session_state["sel_region"] = all_regions
    with col_b:
        if st.button("Clear", key="r_clr", use_container_width=True):
            st.session_state["sel_region"] = []
    if "sel_region" not in st.session_state:
        st.session_state["sel_region"] = all_regions
    selected_region = st.multiselect("", options=all_regions,
        default=st.session_state["sel_region"], label_visibility="collapsed", key="reg")

    # Category filter
    st.markdown(f"<span class='filter-label'>✨ Product Category</span>", unsafe_allow_html=True)
    all_cats = sorted(df["Category"].unique())
    col_c, col_d = st.columns(2)
    with col_c:
        if st.button("All", key="c_all", use_container_width=True):
            st.session_state["sel_cat"] = all_cats
    with col_d:
        if st.button("Clear", key="c_clr", use_container_width=True):
            st.session_state["sel_cat"] = []
    if "sel_cat" not in st.session_state:
        st.session_state["sel_cat"] = all_cats
    selected_cat = st.multiselect("", options=all_cats,
        default=st.session_state["sel_cat"], label_visibility="collapsed", key="cat")

    # Month filter
    st.markdown(f"<span class='filter-label'>📅 Month</span>", unsafe_allow_html=True)
    col_e, col_f = st.columns(2)
    with col_e:
        if st.button("All", key="m_all", use_container_width=True):
            st.session_state["sel_month"] = month_order
    with col_f:
        if st.button("Clear", key="m_clr", use_container_width=True):
            st.session_state["sel_month"] = []
    if "sel_month" not in st.session_state:
        st.session_state["sel_month"] = month_order
    selected_month = st.multiselect("", options=month_order,
        default=st.session_state["sel_month"], label_visibility="collapsed", key="mon")

    # Agent filter
    st.markdown(f"<span class='filter-label'>👤 Agent</span>", unsafe_allow_html=True)
    all_agents = sorted(df["Agent"].unique())
    col_g, col_h = st.columns(2)
    with col_g:
        if st.button("All", key="a_all", use_container_width=True):
            st.session_state["sel_agent"] = all_agents
    with col_h:
        if st.button("Clear", key="a_clr", use_container_width=True):
            st.session_state["sel_agent"] = []
    if "sel_agent" not in st.session_state:
        st.session_state["sel_agent"] = all_agents
    selected_agent = st.multiselect("", options=all_agents,
        default=st.session_state["sel_agent"], label_visibility="collapsed", key="agt")

    st.markdown(f"""<br><div style='color:{GRAY};font-size:10px;border-top:1px solid #1E3A5F;
    padding-top:12px;text-align:center;'>Built by Farah Annisa<br>Master of Data Science · UM</div>""",
    unsafe_allow_html=True)

filtered = df[
    df["Region"].isin(selected_region) &
    df["Category"].isin(selected_cat) &
    df["Month"].isin(selected_month) &
    df["Agent"].isin(selected_agent)
]

if filtered.empty:
    st.warning("No data matches the selected filters. Please adjust your selections.")
    st.stop()

# ── Header ──
st.markdown(f"""
<div style='margin-bottom:8px;'>
    <div style='color:{GOLD};font-size:11px;font-weight:700;letter-spacing:0.2em;'>💄 LUX BEAUTY SDN BHD · SALES INTELLIGENCE PLATFORM</div>
    <div style='color:{WHITE};font-size:30px;font-weight:700;line-height:1.2;margin:4px 0;'>Sales Performance Command Centre</div>
    <div style='color:{GRAY};font-size:13px;'>Real-time KPI monitoring · Agent achievement tracking · Regional & category analysis</div>
</div>""", unsafe_allow_html=True)
st.divider()

# ── KPI Cards ──
total_sales = filtered["Actual Sales (RM)"].sum()
total_target = filtered["Target (RM)"].sum()
overall_achievement = (total_sales / total_target * 100) if total_target > 0 else 0
top_agent = filtered.groupby("Agent")["Actual Sales (RM)"].sum().idxmax()
top_agent_sales = filtered.groupby("Agent")["Actual Sales (RM)"].sum().max()
exceeded_count = filtered[filtered["Status"]=="Exceeded"]["Agent"].nunique()
below_count = filtered[filtered["Status"]=="Below Target"]["Agent"].nunique()
total_units = filtered["Units Sold"].sum()
total_clients = filtered["New Clients"].sum()
avg_achievement = filtered["Achievement (%)"].mean()
ach_color = GREEN if overall_achievement >= 100 else (AMBER if overall_achievement >= 90 else RED)

c1,c2,c3,c4,c5,c6 = st.columns(6)
cards = [
    ("TOTAL REVENUE", f"RM {total_sales/1e6:.2f}M", f"vs Target RM {total_target/1e6:.2f}M"),
    ("ACHIEVEMENT", f'<span style="color:{ach_color};">{overall_achievement:.1f}%</span>', f"Team avg: {avg_achievement:.1f}%"),
    ("🏆 TOP AGENT", f'<span style="font-size:17px;">{top_agent}</span>', f"RM {top_agent_sales:,.0f}"),
    ("EXCEEDED TARGET", f'<span style="color:{GREEN};">{exceeded_count}</span>', f'<span style="color:{RED};">{below_count} below target</span>'),
    ("UNITS SOLD", f"{total_units:,}", f"Across {filtered['Agent'].nunique()} agents"),
    ("NEW CLIENTS", f"{total_clients:,}", f"{filtered['Month'].nunique()} months tracked"),
]
for col, (label, value, sub) in zip([c1,c2,c3,c4,c5,c6], cards):
    col.markdown(f"""<div class='kpi-card'>
        <div class='kpi-label'>{label}</div>
        <div class='kpi-value'>{value}</div>
        <div class='kpi-sub'>{sub}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Gauge + Monthly Trend ──
col_a, col_b = st.columns([1,2])
with col_a:
    st.markdown("<div class='section-header'>ACHIEVEMENT GAUGE</div>", unsafe_allow_html=True)
    fig_g = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=overall_achievement,
        delta={"reference":100,"valueformat":".1f","suffix":"%"},
        number={"suffix":"%","font":{"size":36,"color":WHITE}},
        gauge={
            "axis":{"range":[0,150],"tickcolor":GRAY,"tickfont":{"color":GRAY}},
            "bar":{"color":GOLD,"thickness":0.25},
            "bgcolor":LIGHT_NAVY, "bordercolor":GOLD,
            "steps":[
                {"range":[0,90],"color":"#1A0808"},
                {"range":[90,110],"color":"#081A08"},
                {"range":[110,150],"color":"#061206"},
            ],
            "threshold":{"line":{"color":WHITE,"width":2},"thickness":0.75,"value":100}
        }
    ))
    fig_g.update_layout(height=260,margin=dict(t=20,b=10,l=20,r=20),
        paper_bgcolor="rgba(0,0,0,0)",font={"color":WHITE})
    st.plotly_chart(fig_g, use_container_width=True)

with col_b:
    st.markdown("<div class='section-header'>MONTHLY REVENUE vs TARGET</div>", unsafe_allow_html=True)
    monthly = filtered.groupby("Month",observed=True)[["Actual Sales (RM)","Target (RM)"]].sum().reset_index()
    fig_m = go.Figure()
    fig_m.add_trace(go.Bar(x=monthly["Month"],y=monthly["Actual Sales (RM)"],
        name="Actual Sales",marker_color=GOLD,opacity=0.9))
    fig_m.add_trace(go.Scatter(x=monthly["Month"],y=monthly["Target (RM)"],
        name="Target",mode="lines+markers",
        line=dict(color=WHITE,width=2,dash="dot"),marker=dict(size=6,color=WHITE)))
    fig_m.update_layout(height=260,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        font={"color":GRAY},legend=dict(orientation="h",y=-0.3,font=dict(color=GRAY)),
        xaxis=dict(gridcolor="#1E3A5F",tickfont=dict(color=GRAY)),
        yaxis=dict(gridcolor="#1E3A5F",tickfont=dict(color=GRAY),tickformat=",.0f"),
        margin=dict(t=10,b=10))
    st.plotly_chart(fig_m, use_container_width=True)

st.divider()

# ── Leaderboard + Category + Status ──
col_c, col_d, col_e = st.columns([3,2,1])

with col_c:
    st.markdown("<div class='section-header'>AGENT ACHIEVEMENT LEADERBOARD</div>", unsafe_allow_html=True)
    lb = filtered.groupby("Agent").agg(
        Total_Sales=("Actual Sales (RM)","sum"),
        Total_Target=("Target (RM)","sum")).reset_index()
    lb["Achievement"] = (lb["Total_Sales"]/lb["Total_Target"]*100).round(1)
    lb = lb.sort_values("Achievement",ascending=True)
    lb["Color"] = lb["Achievement"].apply(lambda x: GREEN if x>=110 else (AMBER if x>=90 else RED))
    fig_lb = go.Figure()
    fig_lb.add_trace(go.Bar(
        x=lb["Achievement"],y=lb["Agent"],orientation="h",
        marker_color=lb["Color"],
        text=lb["Achievement"].apply(lambda x: f"{x:.1f}%"),
        textposition="outside",textfont=dict(color=WHITE,size=11)
    ))
    fig_lb.add_vline(x=100,line_dash="dash",line_color=GOLD,line_width=1,
        annotation_text="100%",annotation_font_color=GOLD,annotation_font_size=10)
    fig_lb.update_layout(height=400,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        font={"color":GRAY},
        xaxis=dict(gridcolor="#1E3A5F",tickfont=dict(color=GRAY),range=[0,160]),
        yaxis=dict(tickfont=dict(color=WHITE,size=11)),
        margin=dict(t=10,b=10,r=60))
    st.plotly_chart(fig_lb, use_container_width=True)

with col_d:
    st.markdown("<div class='section-header'>SALES BY CATEGORY</div>", unsafe_allow_html=True)
    cat_df = filtered.groupby("Category")["Actual Sales (RM)"].sum().reset_index()
    fig_cat = go.Figure(go.Pie(
        labels=cat_df["Category"],values=cat_df["Actual Sales (RM)"],hole=0.55,
        marker=dict(colors=[GOLD,"#E8C97A","#A07830","#6B5020"],
            line=dict(color=DARK,width=2)),
        textfont=dict(color=WHITE,size=11),textinfo="label+percent"
    ))
    fig_cat.add_annotation(text=f"<b>4 Categories</b>",
        x=0.5,y=0.5,showarrow=False,font=dict(color=WHITE,size=12))
    fig_cat.update_layout(height=220,paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False,margin=dict(t=10,b=10))
    st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown("<div class='section-header' style='margin-top:8px;'>REGIONAL SPLIT</div>", unsafe_allow_html=True)
    reg_df = filtered.groupby("Region")["Actual Sales (RM)"].sum().reset_index().sort_values("Actual Sales (RM)",ascending=False)
    for _,row in reg_df.iterrows():
        pct = row["Actual Sales (RM)"]/total_sales*100
        st.markdown(f"""<div style='display:flex;justify-content:space-between;align-items:center;
            background:{LIGHT_NAVY};border-left:3px solid {GOLD};
            padding:7px 12px;border-radius:4px;margin-bottom:5px;'>
            <span style='color:{WHITE};font-size:12px;'>{row["Region"]}</span>
            <span style='color:{GOLD};font-weight:700;font-size:12px;'>{pct:.1f}%</span>
        </div>""", unsafe_allow_html=True)

with col_e:
    st.markdown("<div class='section-header'>STATUS</div>", unsafe_allow_html=True)
    sc = filtered.groupby("Status")["Agent"].nunique().reset_index()
    sc.columns = ["Status","Count"]
    color_map = {"Exceeded":GREEN,"Achieved":AMBER,"Below Target":RED}
    for _,row in sc.iterrows():
        c = color_map.get(row["Status"],GRAY)
        st.markdown(f"""<div style='background:{LIGHT_NAVY};border:1px solid {c};
            border-radius:8px;padding:14px;margin-bottom:8px;text-align:center;'>
            <div style='color:{c};font-size:24px;font-weight:700;'>{row["Count"]}</div>
            <div style='color:{GRAY};font-size:10px;letter-spacing:0.08em;margin-top:4px;'>{row["Status"].upper()}</div>
        </div>""", unsafe_allow_html=True)

st.divider()

# ── Table ──
st.markdown("<div class='section-header'>FULL AGENT PERFORMANCE TABLE</div>", unsafe_allow_html=True)
summary = filtered.groupby(["Agent","Region","Category"]).agg(
    Total_Sales=("Actual Sales (RM)","sum"),
    Total_Target=("Target (RM)","sum"),
    Avg_Achievement=("Achievement (%)","mean"),
    Units_Sold=("Units Sold","sum"),
    New_Clients=("New Clients","sum"),
    Client_Visits=("Client Visits","sum")
).reset_index()
summary["Avg_Achievement"] = summary["Avg_Achievement"].round(1)
summary["Conversion (%)"] = (summary["New_Clients"]/summary["Client_Visits"]*100).round(1)
summary = summary.sort_values("Total_Sales",ascending=False)
summary.columns = ["Agent","Region","Category","Total Sales (RM)","Total Target (RM)",
                   "Avg Achievement (%)","Units Sold","New Clients","Client Visits","Conversion (%)"]

def highlight(val):
    if val>=110: return "background-color:#0A2A0A;color:#2ECC71;font-weight:600"
    elif val>=90: return "background-color:#2A1A0A;color:#F39C12;font-weight:600"
    else: return "background-color:#2A0A0A;color:#E74C3C;font-weight:600"

styled = summary.style.map(highlight,subset=["Avg Achievement (%)"])\
    .format({"Total Sales (RM)":"RM {:,.0f}","Total Target (RM)":"RM {:,.0f}",
             "Avg Achievement (%)":"{:.1f}%","Conversion (%)":"{:.1f}%"})
st.dataframe(styled,use_container_width=True,height=420)

col_dl,_ = st.columns([1,4])
with col_dl:
    csv = summary.to_csv(index=False)
    st.download_button("⬇️ Export Report (CSV)",csv,"lux_beauty_sales_report.csv","text/csv")

st.markdown(f"""<br><div style='color:{GRAY};font-size:11px;text-align:center;
border-top:1px solid #1E3A5F;padding-top:12px;'>
LUX Beauty Sales Command Centre · Built by Farah Annisa · Master of Data Science, Universiti Malaya</div>""",
unsafe_allow_html=True)
