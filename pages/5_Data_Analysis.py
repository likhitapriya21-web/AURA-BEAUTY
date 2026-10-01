# pages/5_Data_Analysis.py

import streamlit as st
import pandas as pd
import plotly.express as px
from utils.layout import apply_premium_layout, render_sidebar, render_header, render_stat_card, render_html
from utils.recommender import df

# Apply layout and styles
apply_premium_layout("Data Analysis", "📊")
render_sidebar("Data Analysis")

# Page Header
render_header(
    "Cosmetics Data Intelligence", 
    "Real-time formulation metrics, price distributions, and active pharmaceutical inventory archives."
)

# Cached KPI computations
@st.cache_data(show_spinner=False)
def get_kpis():
    return {
        "total": len(df),
        "brands": int(df["Brand"].nunique()),
        "price": float(df["Price"].mean()),
        "rating": float(df["Rating"].mean())
    }

kpis = get_kpis()

kpi1, kpi2, kpi3, kpi4 = st.columns(4, gap="medium")
with kpi1:
    render_html(render_stat_card(f"{kpis['total']:,}", "Active Formula Archive", icon="✦"))
with kpi2:
    render_html(render_stat_card(f"{kpis['brands']:,}", "Affiliated Boutiques", icon="◈"))
with kpi3:
    render_html(render_stat_card(f"₹{int(kpis['price']):,}", "Mean Formulation Price", icon="₹"))
with kpi4:
    render_html(render_stat_card(f"{kpis['rating']:.2f} ★", "Dermal Satisfaction Index", icon="★"))
    
st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)

# Cached charts for instant rendering
@st.cache_data(show_spinner=False)
def create_volume_chart():
    counts = df["Category"].value_counts().reset_index()
    counts.columns = ["Category", "Count"]
    fig = px.bar(
        counts, 
        x="Category", 
        y="Count",
        color="Category",
        color_discrete_map={
            "Skin": "#4A2E35",
            "Hair": "#A05E6B",
            "Makeup": "#C5A059"
        },
        category_orders={"Category": ["Skin", "Hair", "Makeup"]}
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family="Plus Jakarta Sans",
        showlegend=False,
        margin=dict(t=10, b=20, l=20, r=20),
        xaxis=dict(gridcolor='#F0E8E4', tickfont=dict(size=12, color='#2D1418')),
        yaxis=dict(gridcolor='#F0E8E4', tickfont=dict(size=12, color='#2D1418'))
    )
    return fig

@st.cache_data(show_spinner=False)
def create_price_chart():
    sample_df = df.sample(min(len(df), 5000), random_state=42)
    fig = px.histogram(
        sample_df,
        x="Price",
        color="Category",
        marginal="box",
        color_discrete_map={
            "Skin": "#4A2E35",
            "Hair": "#A05E6B",
            "Makeup": "#C5A059"
        }
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_family="Plus Jakarta Sans",
        margin=dict(t=10, b=20, l=20, r=20),
        xaxis=dict(gridcolor='#F0E8E4', tickfont=dict(size=12, color='#2D1418')),
        yaxis=dict(gridcolor='#F0E8E4', tickfont=dict(size=12, color='#2D1418')),
        legend=dict(font=dict(color='#2D1418'))
    )
    return fig

chart_col1, chart_col2 = st.columns(2, gap="large")

with chart_col1:
    render_html("<h4 class='serif-text' style='color:#2D1418; font-size:22px; text-align:center; margin-bottom: 12px;'>Discipline Curation Volume</h4>")
    st.plotly_chart(create_volume_chart(), use_container_width=True)
    
with chart_col2:
    render_html("<h4 class='serif-text' style='color:#2D1418; font-size:22px; text-align:center; margin-bottom: 12px;'>Product Pricing Distribution</h4>")
    st.plotly_chart(create_price_chart(), use_container_width=True)
    
st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)

render_html("""
<div style="margin-bottom: 20px;">
    <h3 class='serif-text' style='color:#2D1418; font-size: 26px; margin: 0 0 6px 0;'>✦ Active Inventory Explorer</h3>
    <p style='color:#6B5E59; font-size: 14.5px; margin: 0;'>Search, inspect, and isolate certified cosmetic formulations from our verified global archives.</p>
</div>
""")

# Custom filtering interface
col_filter1, col_filter2 = st.columns([1, 2], gap="medium")
categories = ["Skin", "Hair", "Makeup"]

with col_filter1:
    cat_select = st.multiselect(
        "Filter by Discipline", 
        categories, 
        default=categories
    )
with col_filter2:
    search_query = st.text_input("Search Brand or Product Name", placeholder="e.g. CeraVe, The Ordinary, Keratin...")
    
filtered_df = df[df["Category"].isin(cat_select)]
if search_query:
    query_clean = search_query.strip().lower()
    filtered_df = filtered_df[
        filtered_df["Product"].astype(str).str.lower().str.contains(query_clean, na=False) |
        filtered_df["Brand"].astype(str).str.lower().str.contains(query_clean, na=False)
    ]

# Display columns without internal lowercase helper columns
display_cols = ["Category", "Skin_Type", "Hair_Type", "Concern", "Product", "Brand", "Price", "Rating"]
available_cols = [c for c in display_cols if c in filtered_df.columns]

st.caption(f"Displaying top {min(200, len(filtered_df)):,} of {len(filtered_df):,} matching products")
st.dataframe(
    filtered_df[available_cols].head(200),
    use_container_width=True,
    height=420
)