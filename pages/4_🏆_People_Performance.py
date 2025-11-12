import streamlit as st
import pandas as pd
import plotly.express as px
from app.main import run_etl_pipeline
from app.ui.shared_components import render_sidebar

st.set_page_config(layout="wide", page_title="People Performance")
st.title("🏆 People Performance")

sales_data = run_etl_pipeline()
if sales_data is not None:
    filtered_data = render_sidebar(sales_data)

    if filtered_data.empty:
        st.warning("No data available for the selected filters.")
    else:
        st.subheader("Employee Sales Leaderboard")

        employee_performance = filtered_data.groupby('EmployeeName').agg(
            Revenue=('Revenue', 'sum'),
            Orders=('OrderID', 'nunique')
        ).reset_index()

        p_col1, p_col2 = st.columns(2)
        with p_col1:
            st.subheader("By Revenue")
            fig_emp_rev = px.bar(
                employee_performance.sort_values('Revenue', ascending=True),
                x='Revenue', y='EmployeeName', orientation='h', text_auto='.2s'
            )
            st.plotly_chart(fig_emp_rev, use_container_width=True)
        
        with p_col2:
            st.subheader("By Orders")
            fig_emp_ord = px.bar(
                employee_performance.sort_values('Orders', ascending=True),
                x='Orders', y='EmployeeName', orientation='h', text_auto=True
            )
            st.plotly_chart(fig_emp_ord, use_container_width=True)