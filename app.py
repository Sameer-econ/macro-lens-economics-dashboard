import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -----------------------------
# MacroLens | Economic Dashboard
# -----------------------------
st.set_page_config(
    page_title="MacroLens | Economic Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "data" / "sample_economic_data.csv"

st.markdown("""
<style>
    .stApp { background: #0b1020; color: #edf2ff; }
    [data-testid="stSidebar"] { background: #11182b; }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #151f35, #101729);
        border: 1px solid #283653;
        padding: 18px 18px 12px 18px;
        border-radius: 14px;
    }
    [data-testid="stMetricLabel"] { color: #9eb0d0; }
    [data-testid="stMetricValue"] { color: #f4f7ff; }
    .hero {
        padding: 26px 28px; border-radius: 18px; margin-bottom: 18px;
        background: linear-gradient(115deg, #15294a 0%, #142039 55%, #192344 100%);
        border: 1px solid #2b4168;
    }
    .eyebrow { color: #7dd3fc; font-size: 0.78rem; letter-spacing: .16em; font-weight: 700; }
    .hero h1 { margin: 6px 0 4px 0; font-size: 2.25rem; color: #f5f8ff; }
    .hero p { color: #b9c7df; margin: 0; font-size: 1rem; }
    .section-title { color: #edf2ff; font-weight: 700; font-size: 1.15rem; margin: 8px 0 2px 0; }
    .small-note { color: #9eacc5; font-size: .84rem; }
    div[data-testid="stDataFrame"] { border: 1px solid #283653; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    data = pd.read_csv(DATA_PATH)
    data["year"] = pd.to_numeric(data["year"], errors="coerce").astype("Int64")
    data["value"] = pd.to_numeric(data["value"], errors="coerce")
    return data.dropna(subset=["year", "value"])

df = load_data()

st.markdown("""
<div class="hero">
  <div class="eyebrow">MACROLENS / ECONOMIC INTELLIGENCE</div>
  <h1>See the economy in context.</h1>
  <p>An interactive macroeconomic dashboard for exploring growth, inflation and labour-market trends.</p>
</div>
""", unsafe_allow_html=True)

st.warning(
    "DEMO DATA: The included dataset is synthetic and illustrative, not official economic statistics. "
    "Use it to explore the dashboard design; replace it with cited official data before making real-world claims."
)

with st.sidebar:
    st.markdown("## 🎛️ Dashboard controls")
    st.caption("Filter the view. All charts update automatically.")
    countries = sorted(df["country"].unique().tolist())
    selected_countries = st.multiselect("Countries", countries, default=["India", "United States", "United Kingdom"])
    if not selected_countries:
        selected_countries = countries[:1]
        st.info("Select at least one country to display results.")
    indicators = sorted(df["indicator"].unique().tolist())
    selected_indicator = st.selectbox("Primary indicator", indicators, index=0)
    min_year, max_year = int(df["year"].min()), int(df["year"].max())
    year_range = st.slider("Year range", min_value=min_year, max_value=max_year, value=(2015, 2025), step=1)
    show_table = st.checkbox("Show filtered data table", value=True)
    st.markdown("---")
    st.caption("Built with Python · Streamlit · Pandas · Plotly")
    st.caption("Project: MacroLens")

filtered = df[
    df["country"].isin(selected_countries)
    & df["year"].between(year_range[0], year_range[1])
]
primary = filtered[filtered["indicator"] == selected_indicator].copy()
primary = primary.sort_values(["country", "year"])

# KPI row for selected indicator
latest_year = int(primary["year"].max()) if not primary.empty else year_range[1]
latest = primary[primary["year"] == latest_year]
k1, k2, k3, k4 = st.columns(4)
k1.metric("Countries selected", f"{len(selected_countries)}")
k2.metric("Indicator", selected_indicator.replace(" (%)", ""))
k3.metric("Latest year in view", f"{latest_year}")
if not latest.empty:
    avg = latest["value"].mean()
    k4.metric("Selected-country average", f"{avg:.2f}%", help="Simple unweighted average of the selected countries in the latest year.")
else:
    k4.metric("Selected-country average", "N/A")

st.markdown('<div class="section-title">01 / Indicator trend</div>', unsafe_allow_html=True)
st.caption("Compare the selected indicator across countries over time.")
if primary.empty:
    st.info("No observations match the current filters.")
else:
    fig = px.line(
        primary, x="year", y="value", color="country", markers=True,
        template="plotly_dark", labels={"year": "Year", "value": selected_indicator, "country": "Country"},
        color_discrete_sequence=["#65d6ff", "#a78bfa", "#34d399", "#fbbf24", "#fb7185"]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=25, b=10), legend_title_text="",
        hovermode="x unified", height=390
    )
    fig.update_xaxes(dtick=1, gridcolor="#26334d")
    fig.update_yaxes(gridcolor="#26334d", ticksuffix="%")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns([1.15, 0.85])
with left:
    st.markdown('<div class="section-title">02 / Country snapshot</div>', unsafe_allow_html=True)
    st.caption(f"{selected_indicator} in {latest_year}; lower or higher is not automatically better.")
    if not latest.empty:
        snap = latest.sort_values("value", ascending=False)
        bar = px.bar(
            snap, x="country", y="value", color="country", text_auto=".2f",
            template="plotly_dark", labels={"country": "Country", "value": selected_indicator},
            color_discrete_sequence=["#65d6ff", "#a78bfa", "#34d399", "#fbbf24", "#fb7185"]
        )
        bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False, margin=dict(l=10, r=10, t=20, b=10), height=320
        )
        bar.update_yaxes(gridcolor="#26334d", ticksuffix="%")
        st.plotly_chart(bar, use_container_width=True)
    else:
        st.info("No data available for the selected year range.")
with right:
    st.markdown('<div class="section-title">03 / Macro overview</div>', unsafe_allow_html=True)
    st.caption("Latest available observation for each selected country and indicator.")
    all_latest = filtered.sort_values("year").groupby(["country", "indicator"], as_index=False).tail(1)
    if not all_latest.empty:
        heat = all_latest.pivot(index="country", columns="indicator", values="value")
        heat_fig = px.imshow(
            heat, text_auto=".1f", aspect="auto", color_continuous_scale="Blues",
            template="plotly_dark", labels=dict(color="Value (%)")
        )
        heat_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=20, b=10), height=320
        )
        st.plotly_chart(heat_fig, use_container_width=True)
    else:
        st.info("No data available for this selection.")

st.markdown('<div class="section-title">04 / Read the data carefully</div>', unsafe_allow_html=True)
st.markdown("""
- **GDP growth** describes the pace of change in economic output; it is not the size of the economy.
- **Inflation** measures the rate at which a price index rises; falling inflation does not necessarily mean prices are falling.
- **Unemployment** is defined differently across datasets and countries, so definitions and source notes matter.
- **Correlation is not causation.** A chart can reveal patterns, but it cannot by itself prove why they occurred.
""")

if show_table:
    st.markdown('<div class="section-title">05 / Filtered data</div>', unsafe_allow_html=True)
    display_df = filtered.sort_values(["year", "country", "indicator"]).copy()
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    csv_bytes = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download filtered CSV",
        data=csv_bytes,
        file_name="macrolens_filtered_data.csv",
        mime="text/csv"
    )

with st.expander("About this project and its data"):
    st.write(
        "MacroLens is a beginner-friendly portfolio project demonstrating data loading, filtering, "
        "interactive visualisation and basic macroeconomic interpretation. The bundled sample values "
        "are synthetic and should not be cited as actual country statistics."
    )
    st.write("To use real data, replace the CSV with observations from a documented source such as the World Bank, IMF, OECD or national statistical agencies. Preserve source names, units, definitions and download dates.")

st.markdown("---")
st.markdown(
    '<p class="small-note">MACROLENS · Learning project · Synthetic demo dataset · Built for transparent exploration</p>',
    unsafe_allow_html=True
)
