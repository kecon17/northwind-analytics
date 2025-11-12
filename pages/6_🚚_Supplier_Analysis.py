import streamlit as st
import pandas as pd
import plotly.express as px
from app.main import run_etl_pipeline
from app.ui.shared_components import render_sidebar, create_download_button

def aggregate_top_n(df, group_col, agg_col, n=5, group_other=True):
    """
    Aggregates a DataFrame to show Top N. 
    If group_other is True, aggregates the rest into an 'Other' category.
    """
    df_agg = df.groupby(group_col)[agg_col].sum().reset_index()
    df_agg = df_agg.sort_values(by=agg_col, ascending=False)
    
    if group_other and len(df_agg) > n:
        top_n = df_agg.head(n)
        other_sum = df_agg.iloc[n:][agg_col].sum()
        other_row = pd.DataFrame([{group_col: 'Other', agg_col: other_sum}])
        return pd.concat([top_n, other_row])
    
    return df_agg.head(n) # Return only the Top N if group_other is False

st.set_page_config(layout="wide", page_title="Supplier Analysis")
st.title("🚚 Supplier Analysis")

sales_data = run_etl_pipeline()
if sales_data is not None:
    filtered_data = render_sidebar(sales_data)

    if filtered_data.empty:
        st.warning("No data available for the selected filters.")
    else:
        st.subheader("Supplier Performance")
        
        # ---  User control for the "Other" category ---
        group_other_toggle = st.checkbox(
            'Group smaller suppliers into an "Other" category', 
            value=False,
            help="When checked, shows the Top 5 suppliers and aggregates the rest. When unchecked, shows only the Top 5."
        )

        # --- Top N Logic ---
        top_suppliers_by_revenue = aggregate_top_n(filtered_data, 'SupplierName', 'Revenue', group_other=group_other_toggle)
        
        supplier_products = filtered_data[['SupplierName', 'ProductID']].drop_duplicates()
        supplier_product_counts = supplier_products.groupby('SupplierName')['ProductID'].count().reset_index()
        top_suppliers_by_products = aggregate_top_n(supplier_product_counts, 'SupplierName', 'ProductID', group_other=group_other_toggle)

        col1, col2 = st.columns(2)
        chart_title_suffix = "(Top 5 + Other)" if group_other_toggle else "(Top 5)"
        with col1:
            st.subheader(f"By Revenue {chart_title_suffix}")
            fig_rev = px.bar(
                top_suppliers_by_revenue,
                x='Revenue', y='SupplierName', orientation='h', text_auto='.2s'
            ).update_yaxes(categoryorder="total ascending")
            st.plotly_chart(fig_rev, use_container_width=True)
        
        with col2:
            st.subheader(f"By Unique Products Sold {chart_title_suffix}")
            fig_prod = px.bar(
                top_suppliers_by_products,
                x='ProductID', y='SupplierName', orientation='h', text_auto=True,
                labels={'ProductID': 'Number of Products'}
            ).update_yaxes(categoryorder="total ascending")
            st.plotly_chart(fig_prod, use_container_width=True)

        st.subheader("Full Supplier Data")
        full_supplier_performance = filtered_data.groupby('SupplierName').agg(
            Revenue=('Revenue', 'sum'),
            Orders=('OrderID', 'nunique'),
            Products=('ProductID', 'nunique')
        ).reset_index()
        st.dataframe(
            full_supplier_performance.sort_values("Revenue", ascending=False),
            hide_index=True, use_container_width=True
        )
        create_download_button(full_supplier_performance, "supplier_performance")