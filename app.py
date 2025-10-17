import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(page_title="Advanced Data Dashboard", layout="wide", initial_sidebar_state="expanded")

# ============================================================================
# GLOBAL CSS
# ============================================================================
st.markdown("""
<style>
.main .block-container {padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1400px;}
.hero {background: linear-gradient(135deg,#6C5CE733,#A29BFE22); border:1px solid #eceffd; padding: 1.25rem 1.5rem; border-radius: 14px; margin-bottom: 1rem;}
.hero h1 {margin:0; font-size: 1.8rem; color:#2B2D42;}
.hero p {margin:0.2rem 0 0; color:#525566;}
.kpi {background:#fff; border:1px solid #eceffd; border-radius:14px; padding: 1rem 1.25rem; box-shadow: 0 2px 8px rgba(20,20,40,0.05);}
.kpi .label {font-size:0.85rem; color:#6b6f76;}
.kpi .value {font-size:1.4rem; color:#2B2D42; font-weight:600;}
.section {background:#fff; border:1px solid #eceffd; border-radius:14px; padding:1rem 1.25rem; box-shadow: 0 2px 10px rgba(20,20,40,0.04); margin-bottom: 1rem;}
.stTabs [data-baseweb="tab-list"] {gap: .25rem;}
.stTabs [data-baseweb="tab"] {background: #f0f2f6; border-radius: 10px; padding: .5rem 1rem;}
[data-testid="StyledTableContainer"] thead tr th {background:#f9fafc!important;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>📊 Advanced Data Dashboard</h1><p>Upload data, apply filters, and explore with multiple visualization types.</p></div>', unsafe_allow_html=True)

# ============================================================================
# SIDEBAR CONTROLS
# ============================================================================
with st.sidebar:
    st.header("⚙️ Controls")
    file = st.file_uploader("Upload CSV/Excel", type=["csv", "xls", "xlsx"])
    use_sample = st.checkbox("Use sample data", value=False)
    
    st.divider()
    st.subheader("Chart Type")
    chart_type = st.radio("Select Chart", 
        ["Bar", "Line", "Scatter", "Histogram", "Box Plot", "Pie", "Donut", "Sunburst", "Heatmap", "Violin", "Area"], 
        horizontal=False)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================
@st.cache_data
def load_df(f):
    """Load CSV or Excel file safely"""
    try:
        if f is None:
            return None
        
        filename = f.name.lower()
        
        if filename.endswith(".csv"):
            return pd.read_csv(f)
        elif filename.endswith((".xls", ".xlsx")):
            return pd.read_excel(f)
        else:
            return None
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        return None

def get_sample_data():
    """Load sample gapminder data"""
    try:
        return px.data.gapminder().query("year==2007")
    except Exception as e:
        st.error(f"Error loading sample data: {str(e)}")
        return None

# ============================================================================
# DATA LOADING AND VALIDATION
# ============================================================================
df = None

# Priority: file upload > sample data > nothing
if file is not None:
    df = load_df(file)
    if df is not None:
        st.success(f"✅ Loaded: {file.name}")
    else:
        st.error(f"❌ Could not load {file.name}")

if df is None and use_sample:
    df = get_sample_data()
    if df is not None:
        st.success("✅ Loaded sample data")

# If still no data, show info and stop
if df is None:
    st.info("📁 **Getting Started:**\n1. Upload a CSV/Excel file, OR\n2. Check 'Use sample data' in the sidebar")
    st.stop()

# Validate dataframe is not empty - check df is not None first
if df is not None and (df.empty or len(df) == 0):
    st.error("❌ Dataset is empty!")
    st.stop()

# Double check df exists before proceeding
if df is None:
    st.stop()

# ============================================================================
# COLUMN DETECTION
# ============================================================================
num_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(exclude="number").columns.tolist()

if not num_cols and not cat_cols:
    st.error("❌ No valid columns found in dataset!")
    st.stop()

# ============================================================================
# DATA FILTERING SECTION
# ============================================================================
st.markdown('<div class="section"><h3>🔍 Data Filters</h3>', unsafe_allow_html=True)
col_filter_1, col_filter_2, col_filter_3 = st.columns(3)

df_filtered = df.copy()

# Row filtering
with col_filter_1:
    row_limit = st.number_input("Max rows to display:", min_value=1, max_value=len(df), value=min(1000, len(df)))
    df_filtered = df_filtered.head(row_limit)

# Column filtering
with col_filter_2:
    selected_cols = st.multiselect("Columns to include:", options=df.columns.tolist(), default=df.columns.tolist())
    if selected_cols:
        df_filtered = df_filtered[selected_cols]
        # Update column lists
        num_cols = [col for col in num_cols if col in selected_cols]
        cat_cols = [col for col in cat_cols if col in selected_cols]

# Category filtering
with col_filter_3:
    if cat_cols:
        filter_col = st.selectbox("Filter by category:", options=[None] + cat_cols, key="filter_col")
        if filter_col is not None:
            filter_values = st.multiselect("Select values:", options=sorted(df_filtered[filter_col].unique()), key="filter_vals")
            if filter_values:
                df_filtered = df_filtered[df_filtered[filter_col].isin(filter_values)]

st.markdown('</div>', unsafe_allow_html=True)

# Check if filtered data is empty
if df_filtered.empty or len(df_filtered) == 0:
    st.warning("⚠️ No data matches your filters. Please adjust filters.")
    st.stop()

# ============================================================================
# KPI CARDS
# ============================================================================
st.markdown('<div class="section"><h3>📈 Quick Stats</h3>', unsafe_allow_html=True)
kpi_col_1, kpi_col_2, kpi_col_3, kpi_col_4 = st.columns(4)

with kpi_col_1:
    st.markdown(f'<div class="kpi"><div class="label">Total Rows</div><div class="value">{len(df_filtered):,}</div></div>', unsafe_allow_html=True)

with kpi_col_2:
    if num_cols:
        metric_col = num_cols[0]
        val = df_filtered[metric_col].mean()
        st.markdown(f'<div class="kpi"><div class="label">Mean ({metric_col})</div><div class="value">{val:,.2f}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="kpi"><div class="label">Mean</div><div class="value">N/A</div></div>', unsafe_allow_html=True)

with kpi_col_3:
    if cat_cols:
        uniq = cat_cols[0]
        cnt = df_filtered[uniq].nunique()
        st.markdown(f'<div class="kpi"><div class="label">Unique ({uniq})</div><div class="value">{cnt:,}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="kpi"><div class="label">Unique</div><div class="value">N/A</div></div>', unsafe_allow_html=True)

with kpi_col_4:
    st.markdown(f'<div class="kpi"><div class="label">Columns</div><div class="value">{len(df_filtered.columns)}</div></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# TABS
# ============================================================================
tab_chart, tab_data, tab_stats, tab_about = st.tabs(["📊 Chart", "🗃 Data", "📉 Statistics", "ℹ️ About"])

# ============================================================================
# TAB 1: CHART
# ============================================================================
with tab_chart:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    
    col_x, col_y, col_group = st.columns(3)
    
    chart_hints = {
        "Bar": "✓ X: any, Y: numeric",
        "Line": "✓ X: numeric/date, Y: numeric",
        "Scatter": "✓ X: numeric, Y: numeric (no text!)",
        "Histogram": "✓ X: numeric only",
        "Box Plot": "✓ X: categorical, Y: numeric",
        "Pie": "✓ X: categorical only",
        "Donut": "✓ X: categorical only",
        "Sunburst": "✓ X: categorical, Y: numeric",
        "Heatmap": "✓ Auto-correlates numeric columns",
        "Violin": "✓ X: categorical, Y: numeric",
        "Area": "✓ X: numeric/date, Y: numeric"
    }
    
    st.info(f"💡 **{chart_type}:** {chart_hints.get(chart_type, 'Select columns')}")
    
    all_cols = num_cols + cat_cols
    
    with col_x:
        x_axis = st.selectbox("X axis", options=all_cols if all_cols else ["No columns"], key="x")
    
    with col_y:
        y_options = [None] + num_cols if num_cols else [None]
        y_axis = st.selectbox("Y axis", options=y_options, key="y")
    
    with col_group:
        group_options = [None] + cat_cols if cat_cols else [None]
        group_by = st.selectbox("Color/Group", options=group_options, key="group")
    
    fig = None
    error_msg = None
    
    try:
        # BAR CHART
        if chart_type == "Bar":
            if y_axis is not None:
                fig = px.bar(df_filtered, x=x_axis, y=y_axis, color=group_by, barmode="group")
            else:
                error_msg = "⚠️ Please select a numeric Y axis"
        
        # LINE CHART
        elif chart_type == "Line":
            if y_axis is not None:
                fig = px.line(df_filtered, x=x_axis, y=y_axis, color=group_by, markers=True)
            else:
                error_msg = "⚠️ Please select a numeric Y axis"
        
        # SCATTER PLOT - STRICT: needs numeric X and Y
        elif chart_type == "Scatter":
            if y_axis is None:
                error_msg = "⚠️ Please select a numeric Y axis"
            elif x_axis not in num_cols:
                error_msg = f"⚠️ X axis '{x_axis}' is not numeric. Scatter needs numeric X & Y"
            else:
                fig = px.scatter(df_filtered, x=x_axis, y=y_axis, color=group_by, trendline="ols")
        
        # HISTOGRAM
        elif chart_type == "Histogram":
            if x_axis in num_cols:
                fig = px.histogram(df_filtered, x=x_axis, color=group_by, marginal="box", nbins=30)
            else:
                error_msg = f"⚠️ X axis '{x_axis}' is not numeric"
        
        # BOX PLOT
        elif chart_type == "Box Plot":
            if y_axis is None:
                error_msg = "⚠️ Please select a numeric Y axis"
            elif x_axis not in cat_cols:
                error_msg = f"⚠️ X axis '{x_axis}' is not categorical"
            else:
                fig = px.box(df_filtered, x=x_axis, y=y_axis, color=group_by)
        
        # PIE CHART
        elif chart_type == "Pie":
            if x_axis not in cat_cols:
                error_msg = f"⚠️ X axis '{x_axis}' is not categorical"
            else:
                agg_data = df_filtered.groupby(x_axis).size()
                if len(agg_data) > 0:
                    fig = px.pie(values=agg_data.values, names=agg_data.index, title=f"Distribution of {x_axis}")
                else:
                    error_msg = "⚠️ No data to display"
        
        # DONUT CHART
        elif chart_type == "Donut":
            if x_axis not in cat_cols:
                error_msg = f"⚠️ X axis '{x_axis}' is not categorical"
            else:
                agg_data = df_filtered.groupby(x_axis).size()
                if len(agg_data) > 0:
                    fig = px.pie(values=agg_data.values, names=agg_data.index, hole=0.3, title=f"Distribution of {x_axis}")
                else:
                    error_msg = "⚠️ No data to display"
        
        # SUNBURST
        elif chart_type == "Sunburst":
            if x_axis not in cat_cols or y_axis not in num_cols:
                error_msg = "⚠️ Sunburst needs categorical X and numeric Y"
            else:
                fig = px.sunburst(df_filtered, path=[x_axis], values=y_axis, title=f"Sunburst: {x_axis}")
        
        # HEATMAP
        elif chart_type == "Heatmap":
            if len(num_cols) < 2:
                error_msg = "⚠️ Heatmap needs at least 2 numeric columns"
            else:
                corr_matrix = df_filtered[num_cols].corr()
                fig = px.imshow(corr_matrix, text_auto=True, aspect="auto", title="Correlation Heatmap")
        
        # VIOLIN PLOT
        elif chart_type == "Violin":
            if y_axis is None:
                error_msg = "⚠️ Please select a numeric Y axis"
            elif x_axis not in cat_cols:
                error_msg = f"⚠️ X axis '{x_axis}' is not categorical"
            else:
                fig = px.violin(df_filtered, x=x_axis, y=y_axis, color=group_by, box=True)
        
        # AREA CHART
        elif chart_type == "Area":
            if y_axis is not None:
                fig = px.area(df_filtered, x=x_axis, y=y_axis, color=group_by)
            else:
                error_msg = "⚠️ Please select a numeric Y axis"
        
        # Display chart or error
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)
        elif error_msg:
            st.warning(error_msg)
    
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# TAB 2: DATA
# ============================================================================
with tab_data:
    st.markdown('<div class="section"><h3>Data Preview</h3>', unsafe_allow_html=True)
    st.dataframe(df_filtered, use_container_width=True)
    
    csv = df_filtered.to_csv(index=False)
    st.download_button("📥 Download filtered data", csv, file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", mime="text/csv")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# TAB 3: STATISTICS
# ============================================================================
with tab_stats:
    st.markdown('<div class="section"><h3>Statistical Summary</h3>', unsafe_allow_html=True)
    
    if num_cols:
        st.write("**Numeric Columns:**")
        st.dataframe(df_filtered[num_cols].describe())
    else:
        st.info("No numeric columns")
    
    if cat_cols:
        st.write("**Categorical Columns:**")
        for col in cat_cols[:5]:
            st.write(f"*{col}:* {df_filtered[col].nunique()} unique values")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# TAB 4: ABOUT
# ============================================================================
with tab_about:
    st.markdown('''<div class="section">
    <h3>📊 About This Dashboard</h3>
    <p>Advanced data visualization tool built with Streamlit & Plotly</p>
    
    <h4>Chart Types Guide:</h4>
    <ul>
    <li><strong>Bar:</strong> Compare categories</li>
    <li><strong>Line:</strong> Trends over time</li>
    <li><strong>Scatter:</strong> Relationships (numeric only)</li>
    <li><strong>Histogram:</strong> Distribution</li>
    <li><strong>Box Plot:</strong> Distribution by group</li>
    <li><strong>Pie/Donut:</strong> Parts of whole</li>
    <li><strong>Sunburst:</strong> Hierarchical breakdown</li>
    <li><strong>Heatmap:</strong> Correlations</li>
    <li><strong>Violin:</strong> Distribution density</li>
    <li><strong>Area:</strong> Cumulative trends</li>
    </ul>
    </div>''', unsafe_allow_html=True)