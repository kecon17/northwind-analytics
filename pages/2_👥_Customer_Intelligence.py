import streamlit as st
import pandas as pd
import plotly.express as px
from app.main import run_etl_pipeline
from app.ui.shared_components import render_sidebar

st.set_page_config(layout="wide", page_title="Customer Intelligence")

st.title("👥 Customer Intelligence")

sales_data = run_etl_pipeline()
if sales_data is not None:
    filtered_data = render_sidebar(sales_data)

    if filtered_data.empty:
        st.warning("No data available for the selected filters.")
    else:
        # --- Customer 360° Drill-Down ---
        customer_list = ["Overview"] + sorted(filtered_data['ContactName'].unique())
        selected_customer = st.selectbox("Select a Customer for a 360° View", customer_list)

        if selected_customer == "Overview":
            st.subheader("Customer Segmentation (RFM)")
            segment_counts = filtered_data.drop_duplicates(subset=['CustomerID'])['Segment'].value_counts()
            fig2 = px.bar(segment_counts, y=segment_counts.index, x=segment_counts.values, orientation='h', 
                          title="Number of Customers by Segment", labels={'y': 'Segment', 'x': 'Number of Customers'})
            st.plotly_chart(fig2, use_container_width=True)

            with st.expander("About RFM Segmentation"):
                st.info(
                    """
                    **This chart segments customers based on their purchasing behavior using the RFM model.**
                    - **Champions:** Your best and most loyal customers.
                    - **Loyal Customers:** Consistent buyers.
                    - **Potential Loyalists:** Recent customers with potential.
                    - **At-Risk:** Good customers who haven't purchased in a while.
                    - **Needs Attention:** Customers who are slipping away.
                    - **Hibernating:** Lapsed customers.
                    """
                )
        else:
            st.subheader(f"Customer 360°: {selected_customer}")
            customer_data = filtered_data[filtered_data['ContactName'] == selected_customer]
            
            c_col1, c_col2, c_col3, c_col4 = st.columns(4)
            c_col1.metric("Lifetime Spend", f"${customer_data['Revenue'].sum():,.2f}")
            c_col2.metric("Total Orders", f"{customer_data['OrderID'].nunique()}")
            c_col3.metric("RFM Segment", customer_data['Segment'].iloc[0])
            c_col4.metric("Last Order Date", customer_data['OrderDate'].max().date().strftime("%Y-%m-%d"))

            st.markdown("---")
            st.subheader("Order History")
            st.dataframe(
                customer_data[['OrderID', 'OrderDate', 'ProductName', 'Quantity', 'Revenue']].sort_values('OrderDate', ascending=False),
                hide_index=True,
                use_container_width=True
            )