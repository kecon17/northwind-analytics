"""
Main Streamlit application file (Landing Page).
"""

import streamlit as st

st.set_page_config(
    layout="wide", 
    page_title="Northwind Analytics",
    page_icon="📈"
)

def main():
    """Main function to render the landing page."""
    st.title("Northwind Strategic Dashboard")
    st.markdown("---")
    st.header("Welcome!")
    
    st.markdown(
        """
        This dashboard provides a strategic overview of the Northwind Trading Company's performance. 
        It transforms raw sales data into actionable insights, focusing on customers, products, suppliers, and employees.

        **👈 Please select a dashboard page from the sidebar** to begin your analysis.
        """
    )

    st.info(
        """
        **Dashboard Pages:**
        - **📈 Strategic Overview:** High-level KPIs and revenue trends.
        - **👥 Customer Intelligence:** RFM segmentation and a 360° view of individual customers.
        - **⚙️ Operational Performance:** Product performance matrix and reference table.
        - **🏆 People Performance:** Sales employee leaderboards.
        - **🌍 Market Analysis:** Geographic revenue distribution map.
        - **🚚 Supplier Analysis:** Supplier performance insights.
        - **🚚 Shipping Performance:** Analysis of shipping methods and their efficiency.
        """
    )

if __name__ == "__main__":
    main()
