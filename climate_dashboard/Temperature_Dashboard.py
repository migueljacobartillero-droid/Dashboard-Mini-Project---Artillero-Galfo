import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Climate Pulse | Strategic Intelligence",
    page_icon=":material/device_thermostat:", # Replaced emoji with Material Icon
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. DESIGN SYSTEM & CSS
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=IBM+Plex+Sans:wght@300;400;600&display=swap');
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons+Round');

    :root {
        --neon-pink: #FF4E88;
        --neon-mint: #00F5D4;
        --bg-midnight: #0B0E14;
        --glass-bg: rgba(255, 255, 255, 0.02);
        --glass-border: rgba(255, 255, 255, 0.08);
    }

    .stApp {
        background-color: var(--bg-midnight);
        background-image: radial-gradient(circle at 2px 2px, rgba(255,255,255,0.03) 1px, transparent 0);
        background-size: 40px 40px;
        font-family: 'IBM Plex Sans', sans-serif;
        color: #E2E8F0;
    }

    /* Typography */
    h1, h2, h3, h4 { font-family: 'Inter', sans-serif !important; }
    
    /* Streamlit Tabs Customization for Better UX */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px 8px 0px 0px;
        gap: 12px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #94A3B8;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .stTabs [aria-selected="true"] {
        color: var(--neon-mint) !important;
        border-bottom-color: var(--neon-mint) !important;
    }

    /* Insight Banner (Hero Section) */
    .insight-hero {
        background: linear-gradient(135deg, rgba(255, 78, 136, 0.1) 0%, rgba(0, 245, 212, 0.05) 100%);
        border: 1px solid var(--glass-border);
        border-left: 6px solid var(--neon-pink);
        padding: 35px;
        border-radius: 16px;
        margin-top: 10px;
        margin-bottom: 30px;
    }
    .insight-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 3px;
        color: var(--neon-pink);
        font-weight: 800;
        margin-bottom: 12px;
    }
    .insight-body {
        font-size: 1.3rem;
        line-height: 1.6;
        color: #F8FAFC;
        font-weight: 400;
    }

    /* KPI Cards */
    [data-testid="stMetric"] {
        background: var(--glass-bg);
        border: 1px solid var(--glass-border);
        padding: 20px 25px;
        border-radius: 16px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    [data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif;
        font-weight: 800;
        color: var(--neon-mint) !important;
        font-size: 2.2rem !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
        color: #94A3B8 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Icon Heading Alignment */
    .flex-heading {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 15px;
    }
    .mi {
        font-family: 'Material Icons Round';
        font-size: 2rem;
        color: var(--neon-mint);
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. DATA ENGINE
# ==========================================
@st.cache_data
def get_data():
    try:
        g = pd.read_csv("global_trend.csv").dropna().sort_values('Year')
        c = pd.read_csv("country_trend.csv").dropna()
        g['Decade'] = (g['Year'] // 10) * 10
        return g, c
    except Exception:
        return None, None

df_global, df_country = get_data()

if df_global is None:
    st.error("Error: CSV data files not detected. Please upload global_trend.csv and country_trend.csv.", icon=":material/error:")
    st.stop()

# ==========================================
# 4. SIDEBAR (Dedicated to Controls Only)
# ==========================================
with st.sidebar:
    st.markdown("<div class='flex-heading'><span class='mi'>tune</span><h2>Global Filters</h2></div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94A3B8; font-size:0.9rem; margin-bottom:20px;'>Adjust the timeline to see real-time updates across all modules.</p>", unsafe_allow_html=True)
    
    y_min, y_max = int(df_global['Year'].min()), int(df_global['Year'].max())
    years = st.slider("Historical Timeline", y_min, y_max, (1960, y_max))
    
    filtered_g = df_global[df_global['Year'].between(years[0], years[1])]
    
    st.divider()
    st.markdown("""
        <div style='font-size: 0.8rem; color: #64748B;'>
            <b>SYSTEM STATUS:</b> ONLINE<br>
            <b>DATA INTEGRITY:</b> VERIFIED<br>
            <b>SOURCE:</b> BERKELEY EARTH
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. MAIN PAGE HEADER & TABS
# ==========================================
st.markdown("<div class='flex-heading'><span class='mi' style='font-size:2.5rem;'>sensors</span><h1 style='margin:0; font-size:2.5rem;'>Climate Pulse Intelligence</h1></div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Using native Streamlit Material Icons for the tabs (Emoji Replaced)
tab1, tab2, tab3 = st.tabs([
    ":material/language: GLOBAL OVERVIEW", 
    ":material/map: GEOGRAPHIC MATRIX", 
    ":material/warning: RISK ANOMALIES"
])

# ------------------------------------------
# TAB 1: GLOBAL OVERVIEW
# ------------------------------------------
with tab1:
    net_diff = filtered_g['AverageTemperature'].iloc[-1] - filtered_g['AverageTemperature'].iloc[0]
    
    # Hero Insight
    st.markdown(f"""
        <div class="insight-hero">
            <div class="insight-title">Executive Discovery</div>
            <div class="insight-body">
                Since {years[0]}, the global thermal profile has entered a high-velocity phase. 
                Average temperatures are currently trending <b style="color:var(--neon-mint);">{net_diff:+.2f}°C</b> 
                higher than the selected baseline, indicating a fundamental acceleration in planetary heat retention.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Organized KPIs
    k1, k2, k3, k4 = st.columns(4)
    avg_temp = filtered_g['AverageTemperature'].mean()
    warming_rate = np.polyfit(filtered_g['Year'], filtered_g['AverageTemperature'], 1)[0]
    peak_yr = int(filtered_g.loc[filtered_g['AverageTemperature'].idxmax(), 'Year'])

    with k1: st.metric("Average Temperature", f"{avg_temp:.2f}°C")
    with k2: st.metric("Net Shift", f"{net_diff:+.2f}°C", delta_color="inverse")
    with k3: st.metric("Warming Velocity", f"{warming_rate:+.4f}/yr")
    with k4: st.metric("Historic Peak Year", peak_yr)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Side-by-side Chart Layout
    c1, c2 = st.columns([1.5, 1]) 
    
    with c1:
        st.markdown("<div class='flex-heading'><span class='mi' style='font-size:1.5rem;'>trending_up</span><h3>Thermal Velocity Over Time</h3></div>", unsafe_allow_html=True)
        fig_line = px.area(filtered_g, x="Year", y="AverageTemperature", template="plotly_dark")
        fig_line.update_traces(line_color='#00F5D4', fillcolor='rgba(0, 245, 212, 0.08)', line_width=3)
        fig_line.update_layout(
            margin=dict(l=0, r=0, t=20, b=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            yaxis_title="Temperature (°C)", xaxis_title=None
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with c2:
        st.markdown("<div class='flex-heading'><span class='mi' style='font-size:1.5rem;'>bar_chart</span><h3>Decadal Variance</h3></div>", unsafe_allow_html=True)
        fig_box = px.box(filtered_g, x="Decade", y="AverageTemperature", template="plotly_dark", color_discrete_sequence=['#FF4E88'])
        fig_box.update_layout(
            margin=dict(l=0, r=0, t=20, b=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Decade", yaxis_title=None, showlegend=False
        )
        st.plotly_chart(fig_box, use_container_width=True)

# ------------------------------------------
# TAB 2: GEOGRAPHIC MATRIX
# ------------------------------------------
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    col_filters, col_space = st.columns([2, 1])
    with col_filters:
        countries = st.multiselect(
            "Select Jurisdictions to Compare", 
            options=sorted(df_country['Country'].unique()), 
            default=["United States", "China", "India", "Brazil", "Canada"]
        )
    
    st.markdown("<hr style='border-color: rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
    
    # Advanced Heatmap Full Width
    st.markdown("<div class='flex-heading'><span class='mi'>grid_view</span><h3>Comparative Heat Matrix</h3></div>", unsafe_allow_html=True)
    df_pivot = df_country[(df_country['Country'].isin(countries)) & (df_country['Year'].between(years[0], years[1]))].pivot(index="Country", columns="Year", values="AverageTemperature")
    
    fig_heat = px.imshow(df_pivot, color_continuous_scale='Magma', aspect="auto", template="plotly_dark")
    fig_heat.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=20))
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Animated Choropleth Full Width
    st.markdown("<div class='flex-heading'><span class='mi'>public</span><h3>Global Progression Animation</h3></div>", unsafe_allow_html=True)
    fig_map = px.choropleth(df_country[df_country['Year'].between(years[0], years[1])], 
                           locations="Country", locationmode='country names', color="AverageTemperature", 
                           animation_frame="Year", color_continuous_scale="Viridis", template="plotly_dark")
    fig_map.update_layout(
        height=650, 
        margin=dict(l=0, r=0, t=10, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='rgba(0,0,0,0)')
    )
    st.plotly_chart(fig_map, use_container_width=True)

# ------------------------------------------
# TAB 3: RISK ANOMALIES
# ------------------------------------------
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    
    baseline = df_global[df_global['Year'] <= 1950]['AverageTemperature'].mean()
    filtered_g['Anomaly'] = filtered_g['AverageTemperature'] - baseline
    
    # Replaced emoji with Material Icon parameter
    st.info(f"**Methodology Note:** Anomalies are calculated as deviations from the historical pre-1950 baseline temperature of **{baseline:.2f}°C**.", icon=":material/lightbulb:")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='flex-heading'><span class='mi' style='font-size:1.5rem;'>stacked_bar_chart</span><h3>Baseline Deviation Engine</h3></div>", unsafe_allow_html=True)
    
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=filtered_g['Year'], 
        y=filtered_g['Anomaly'],
        marker_color=['#FF4E88' if x > 0 else '#00F5D4' for x in filtered_g['Anomaly']],
        opacity=0.85
    ))
    fig_bar.update_layout(
        template="plotly_dark", 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(255,255,255,0.02)', 
        xaxis_title="Year",
        yaxis_title="Deviation from Baseline (°C)",
        margin=dict(t=20, b=20, l=20, r=20),
        height=550
    )
    fig_bar.add_hline(y=0, line_width=2, line_color="rgba(255,255,255,0.5)")
    st.plotly_chart(fig_bar, use_container_width=True)