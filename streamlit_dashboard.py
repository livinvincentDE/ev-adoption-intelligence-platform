import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

# ====================== PAGE CONFIG & VIBRANT THEME ======================
st.set_page_config(
    page_title="⚡ EV Grid Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Vibrant Neon Cyber Theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700;900&family=Share+Tech+Mono&family=Rajdhani:wght@300;400;600&display=swap');

:root {
    --neon-green: #00ff41;
    --neon-cyan: #00f0ff;
    --neon-pink: #ff00aa;
    --dark-bg: #0a001f;
    --panel-bg: #12052e;
}

.stApp {
    background: linear-gradient(180deg, #0a001f 0%, #1a0033 100%);
}

.ev-header h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: 3.2rem;
    font-weight: 900;
    background: linear-gradient(90deg, #00ff41, #00f0ff, #ff00aa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 40px #00ff41;
    animation: glow 2s ease-in-out infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 20px #00ff41; }
    to { text-shadow: 0 0 50px #00f0ff, 0 0 80px #ff00aa; }
}

.stMetric {
    background: linear-gradient(135deg, #12052e, #1f0a4d);
    border: 2px solid var(--neon-green);
    border-radius: 12px;
    box-shadow: 0 0 25px rgba(0, 255, 65, 0.4);
}

.stPlotlyChart, .stDataFrame {
    border: 1px solid #00ff41;
    border-radius: 12px;
    box-shadow: 0 0 30px rgba(0, 255, 65, 0.25);
}

.stDownloadButton > button {
    background: linear-gradient(45deg, #00ff41, #00f0ff);
    color: black;
    font-weight: bold;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# Plotly Vibrant Theme
PLOTLY_LAYOUT = dict(
    paper_bgcolor='#12052e',
    plot_bgcolor='#12052e',
    font=dict(family='Share Tech Mono', color='#00ff41'),
    title_font=dict(family='Orbitron', color='#00f0ff', size=16),
    margin=dict(l=50, r=30, t=60, b=50),
    xaxis=dict(gridcolor='#3a1a66'),
    yaxis=dict(gridcolor='#3a1a66'),
)

NEON_SCALE = ['#1a0033', '#00aa33', '#00ff41', '#00f0ff', '#ff00aa']

# ====================== HEADER ======================
st.markdown("""
<div class="ev-header" style="text-align:center; padding: 1.5rem 0 0.5rem;">
    <h1>⚡ EV GRID INTELLIGENCE</h1>
    <p style="color:#00f0ff; font-family:'Share Tech Mono'; letter-spacing:4px; font-size:1.1rem;">
        ELECTRIC VEHICLE ADOPTION ANALYTICS PLATFORM • v2.0
    </p>
</div>
""", unsafe_allow_html=True)

# ====================== DATABASE ======================
@st.cache_resource
def get_db_connection():
    return duckdb.connect('ev_adoption.duckdb')

conn = get_db_connection()

@st.cache_data
def load_filter_options(_conn):
    years = [r[0] for r in _conn.execute("""
        SELECT DISTINCT CAST(model_year AS INTEGER) 
        FROM silver.ev_data WHERE model_year IS NOT NULL ORDER BY 1 DESC
    """).fetchall() if r[0]]
    
    makes = [r[0] for r in _conn.execute("SELECT DISTINCT make FROM silver.ev_data WHERE make IS NOT NULL ORDER BY make").fetchall()]
    ev_types = [r[0] for r in _conn.execute("SELECT DISTINCT ev_type_clean FROM silver.ev_data WHERE ev_type_clean IS NOT NULL ORDER BY ev_type_clean").fetchall()]
    states = [r[0] for r in _conn.execute("SELECT DISTINCT state FROM silver.ev_data WHERE state IS NOT NULL ORDER BY state").fetchall()]

    return years, makes, ev_types, sorted(states)

all_years, all_makes, all_ev_types, all_states = load_filter_options(conn)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown("### ⚡ FILTERS")
    st.caption("Leave empty to select all")

    selected_years = st.multiselect("📅 Model Year", all_years, key="years")
    selected_makes = st.multiselect("🏭 Manufacturer", all_makes, key="makes")
    selected_ev_types = st.multiselect("⚡ EV Type", all_ev_types, key="types")
    selected_states = st.multiselect("🗺️ State", all_states, key="states")

# ====================== FILTER VALUES ======================
selected_years = st.session_state.get("years") or all_years
selected_makes = st.session_state.get("makes") or all_makes
selected_ev_types = st.session_state.get("types") or all_ev_types
selected_states = st.session_state.get("states") or all_states

# ====================== WHERE CLAUSE - FIXED ======================
def build_where_clause(years, makes, ev_types, states):
    conditions = []
    
    if years:
        conditions.append(f"CAST(model_year AS INTEGER) IN ({','.join(map(str, years))})")
    
    if makes:
        make_str = ", ".join([f"'{m}'" for m in makes])   # Fixed here
        conditions.append(f"make IN ({make_str})")
    
    if ev_types:
        type_str = ", ".join([f"'{t}'" for t in ev_types])
        conditions.append(f"ev_type_clean IN ({type_str})")
    
    if states:
        state_str = ", ".join([f"'{s}'" for s in states])
        conditions.append(f"state IN ({state_str})")
    
    return "WHERE " + " AND ".join(conditions) if conditions else ""

where_clause = build_where_clause(selected_years, selected_makes, selected_ev_types, selected_states)

# ====================== MAIN DASHBOARD ======================
try:
    total_vehicles = conn.execute(f"SELECT COUNT(*) FROM silver.ev_data {where_clause}").fetchone()[0]
    uniq_makes = conn.execute(f"SELECT COUNT(DISTINCT make) FROM silver.ev_data {where_clause}").fetchone()[0]
    uniq_states = conn.execute(f"SELECT COUNT(DISTINCT state) FROM silver.ev_data {where_clause}").fetchone()[0]
    avg_year = conn.execute(f"SELECT ROUND(AVG(CAST(model_year AS INTEGER))) FROM silver.ev_data {where_clause}").fetchone()[0]

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("⚡ TOTAL VEHICLES", f"{total_vehicles:,}")
    with col2: st.metric("🏭 MANUFACTURERS", uniq_makes)
    with col3: st.metric("🗺️ STATES", uniq_states)
    with col4: st.metric("📅 AVG MODEL YEAR", int(avg_year) if avg_year else "N/A")

    if total_vehicles == 0:
        st.error("❌ No data found for selected filters.")
        st.stop()

    st.success(f"// GRID LOADED • {total_vehicles:,} vehicles", icon="⚡")
    st.divider()

    # Charts
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("📈 Vehicles by Model Year")
        year_df = conn.execute(f"""
            SELECT CAST(model_year AS INTEGER) as year, COUNT(*) as count 
            FROM silver.ev_data {where_clause} GROUP BY year ORDER BY year DESC
        """).fetch_df()
        if not year_df.empty:
            fig = px.bar(year_df, x='year', y='count', color='count', color_continuous_scale=NEON_SCALE)
            fig.update_layout(**PLOTLY_LAYOUT, title="EV COUNT BY MODEL YEAR")
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("🏭 Top 10 Manufacturers")
        make_df = conn.execute(f"""
            SELECT make, COUNT(*) as count 
            FROM silver.ev_data {where_clause} GROUP BY make ORDER BY count DESC LIMIT 10
        """).fetch_df()
        if not make_df.empty:
            fig = px.bar(make_df, x='count', y='make', orientation='h', color='count', color_continuous_scale=NEON_SCALE)
            fig.update_layout(**PLOTLY_LAYOUT, title="TOP 10 MANUFACTURERS")
            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("📋 Raw Data Sample (1000 rows)")
    sample_df = conn.execute(f"""
        SELECT model_year, make, model, ev_type_clean, city, state 
        FROM silver.ev_data {where_clause} LIMIT 1000
    """).fetch_df()

    st.dataframe(sample_df, use_container_width=True, height=420)

    csv = sample_df.to_csv(index=False)
    st.download_button("⬇️ Download CSV", csv, "ev_grid_data.csv", "text/csv", use_container_width=True)

except Exception as e:
    st.error(f"Error: {str(e)}")
    st.info("Make sure `ev_adoption.duckdb` exists and you have run `bruin run`.")
