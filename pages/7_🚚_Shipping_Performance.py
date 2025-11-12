"""
Shipping & Logistics Performance Page

This page analyzes the time it takes to ship orders to customers, broken down by
shipper, country, and employee.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
from app.main import run_etl_pipeline
from app.ui.shared_components import render_sidebar

st.set_page_config(layout="wide", page_title="Shipping Performance")
st.title("🚚 Shipping & Logistics Performance")

# --- Load and Filter Data ---
sales_data = run_etl_pipeline()
if sales_data is not None:
    filtered_data = render_sidebar(sales_data)

    if filtered_data.empty:
        st.warning("No data available for the selected filters.")
    else:
        # --- Data Preparation ---
        # Calculate shipping time in days, handling potential missing dates
        df = filtered_data.dropna(subset=['OrderDate', 'ShippedDate']).copy()
        df['ShippingTime'] = (df['ShippedDate'] - df['OrderDate']).dt.days
        
        # Filter out any negative shipping times which indicate data errors
        df = df[df['ShippingTime'] >= 0]

        # --- KPI Card ---
        avg_shipping_time = df['ShippingTime'].mean()
        st.metric("Average Shipping Time", f"{avg_shipping_time:.2f} Days")
        st.markdown("---")

        # --- Visualizations ---
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Avg. Shipping Time by Country")
            country_shipping = df.groupby('Country')['ShippingTime'].mean().reset_index().sort_values('ShippingTime')
            fig_country = px.bar(
                country_shipping, x='ShippingTime', y='Country', orientation='h',
                labels={'ShippingTime': 'Average Shipping Time (Days)'}
            )
            st.plotly_chart(fig_country, use_container_width=True)

        with col2:
            st.subheader("Avg. Shipping Time by Employee")
            employee_shipping = df.groupby('EmployeeName')['ShippingTime'].mean().reset_index().sort_values('ShippingTime')
            fig_employee = px.bar(
                employee_shipping, x='ShippingTime', y='EmployeeName', orientation='h',
                labels={'ShippingTime': 'Average Shipping Time (Days)'}
            )
            st.plotly_chart(fig_employee, use_container_width=True)