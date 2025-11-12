import streamlit as st
import pandas as pd
import plotly.express as px
from app.main import run_etl_pipeline
from app.ui.shared_components import render_sidebar

st.set_page_config(layout="wide", page_title="Market Analysis")
st.title("🌍 Market Analysis")

sales_data = run_etl_pipeline()
if sales_data is not None:
    filtered_data = render_sidebar(sales_data)

    if filtered_data.empty:
        st.warning("No data available for the selected filters.")
    else:
        st.subheader("Revenue by Country")
        
        st.info("Click a country on the map, then use the filter below to drill down across the entire dashboard.")
        
        all_countries = sorted(sales_data['Country'].unique())
        selected_map_countries = st.multiselect(
            "Filter dashboard by selected countries:",
            options=all_countries,
            default=st.session_state.selected_countries
        )
        if selected_map_countries != st.session_state.selected_countries:
            st.session_state.selected_countries = selected_map_countries
            st.rerun()
        
        country_revenue = filtered_data.groupby(['Country', 'CountryISO3'], as_index=False)['Revenue'].sum()
        
        fig4 = px.choropleth(
            country_revenue, 
            locations='CountryISO3',
            locationmode='ISO-3',
            color='Revenue', 
            hover_name='Country', 
            color_continuous_scale=px.colors.sequential.Plasma, 
            title="Geographic Revenue Distribution"
        )
        st.plotly_chart(fig4, use_container_width=True)