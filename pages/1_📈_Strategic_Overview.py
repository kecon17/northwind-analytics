import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from app.main import run_etl_pipeline
from app.ui.shared_components import render_sidebar
from datetime import date, timedelta

st.set_page_config(layout="wide", page_title="Strategic Overview")

def get_comparison_data(sales_data, start_date, end_date, period_type):
    """Calculates metrics for a comparison period."""
    if period_type == "Same Period Last Year":
        comp_start_date = start_date.replace(year=start_date.year - 1)
        comp_end_date = end_date.replace(year=end_date.year - 1)
        # We use the full, un-filtered sales_data for historical comparison
        return sales_data[
            (sales_data['OrderDate'].dt.date >= comp_start_date) &
            (sales_data['OrderDate'].dt.date <= comp_end_date)
        ]
    return None # Return None for "None" or any other case

st.title("📈 Strategic Overview")

sales_data = run_etl_pipeline()
if sales_data is not None:
    filtered_data = render_sidebar(sales_data)

    if filtered_data.empty:
        st.warning("No data available for the selected filters.")
    else:
        # --- Local Control for KPI Comparison ---
        st.markdown("### KPI Comparison")
        comparison_period = st.selectbox(
            "Compare KPIs against:",
            ["None", "Same Period Last Year"],
            label_visibility="collapsed"
        )
        
        # --- KPI Calculations ---
        main_total_revenue = filtered_data['Revenue'].sum()
        main_total_orders = filtered_data['OrderID'].nunique()
        
        qoq_growth = 0
        if not filtered_data.empty:
            last_order_date = filtered_data['OrderDate'].max()
            current_quarter_period = pd.Period(last_order_date, freq='Q')
            previous_quarter_period = current_quarter_period - 1
            current_quarter_revenue = sales_data[sales_data['OrderDate'].dt.to_period('Q') == current_quarter_period]['Revenue'].sum()
            previous_quarter_revenue = sales_data[sales_data['OrderDate'].dt.to_period('Q') == previous_quarter_period]['Revenue'].sum()
            if previous_quarter_revenue > 0:
                qoq_growth = (current_quarter_revenue - previous_quarter_revenue) / previous_quarter_revenue

        comp_data = get_comparison_data(sales_data, st.session_state.start_date, st.session_state.end_date, comparison_period)
        delta_revenue, delta_orders = None, None
        if comp_data is not None and not comp_data.empty:
            comp_revenue = comp_data['Revenue'].sum()
            comp_orders = comp_data['OrderID'].nunique()
            if comp_revenue > 0:
                delta_revenue = (main_total_revenue - comp_revenue) / comp_revenue
            if comp_orders > 0:
                delta_orders = (main_total_orders - comp_orders) / comp_orders

        # --- KPI Display with Sparklines ---
        def create_sparkline(data, y_col, x_col='OrderDate'):
            fig = go.Figure(go.Scatter(x=data[x_col], y=data[y_col], mode='lines', fill='tozeroy', line_shape='spline'))
            fig.update_layout(showlegend=False, xaxis_visible=False, yaxis_visible=False, margin=dict(l=0, r=0, t=0, b=0), height=50)
            return fig

        col1, col2, col3 = st.columns(3)
        with col1:
            col1.metric("Total Revenue", f"${main_total_revenue:,.2f}", f"{delta_revenue:.2%}" if delta_revenue is not None else None)
            revenue_spark_data = filtered_data.set_index('OrderDate').resample('D')['Revenue'].sum().reset_index()
            st.plotly_chart(create_sparkline(revenue_spark_data, 'Revenue'), use_container_width=True)

        with col2:
            col2.metric("Total Orders", f"{main_total_orders:,}", f"{delta_orders:.2%}" if delta_orders is not None else None)
            orders_spark_data = filtered_data.groupby(filtered_data['OrderDate'].dt.date)['OrderID'].nunique().reset_index()
            st.plotly_chart(create_sparkline(orders_spark_data, 'OrderID'), use_container_width=True)

        with col3:
            col3.metric("Quarterly Growth", f"{qoq_growth:.2%}", help="Growth of the latest quarter in the selection vs. the preceding quarter.")
        
        st.markdown("---")
        st.subheader("Revenue Trend")
        monthly_revenue = filtered_data.set_index('OrderDate').resample('ME')['Revenue'].sum()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=monthly_revenue.index, y=monthly_revenue.values, name='Revenue', fill='tozeroy'))
        st.plotly_chart(fig, use_container_width=True)