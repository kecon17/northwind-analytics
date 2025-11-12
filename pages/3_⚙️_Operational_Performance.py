import streamlit as st
import pandas as pd
import plotly.express as px
from app.main import run_etl_pipeline
from app.ui.shared_components import render_sidebar, create_download_button

st.set_page_config(layout="wide", page_title="Operational Performance")
st.title("⚙️ Operational Performance")

sales_data = run_etl_pipeline()
if sales_data is not None:
    filtered_data = render_sidebar(sales_data)

    if filtered_data.empty:
        st.warning("No data available for the selected filters.")
    else:
        st.subheader("Product Performance Matrix")
        product_performance = filtered_data.groupby(['ProductID', 'ProductName', 'CategoryName']).agg(
            {'Revenue': 'sum', 'Quantity': 'sum'}
        ).reset_index()

        fig3 = px.scatter(
            product_performance, 
            x='Quantity', 
            y='Revenue', 
            text='ProductID', 
            size='Revenue', 
            color='CategoryName', 
            hover_name='ProductName',
            labels={'Quantity': 'Total Quantity Sold', 'Revenue': 'Total Revenue'},
            title="Revenue vs. Quantity by Product"
        )
        fig3.update_traces(textposition='top center', textfont_size=10)
        st.plotly_chart(fig3, use_container_width=True)
        
        st.subheader("Product Reference")
        st.dataframe(
            product_performance.sort_values(by="Revenue", ascending=False),
            hide_index=True, use_container_width=True
        )
        create_download_button(product_performance, "product_performance")