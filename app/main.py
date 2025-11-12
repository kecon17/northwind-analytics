"""
Main ETL orchestration and data loading module.
"""

import logging
import streamlit as st
import pandas as pd
from typing import Union
from .config import Config
from .etl.extract import get_db_engine, extract_data
from .etl.transform import create_comprehensive_sales_data, perform_rfm_analysis
from .etl.load import load_data

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@st.cache_data(ttl=3600) # Cache data for 1 hour
def run_etl_pipeline() -> Union[pd.DataFrame, None]:
    """Runs the full ETL pipeline.

    Returns:
        pd.DataFrame | None: Enriched sales data with RFM segments.
    """
    logging.info("Starting ETL pipeline...")

    connection_string = Config.get_db_connection_string()
    engine = get_db_engine(connection_string)

    if not engine:
        st.error("Failed to connect to the database. Please check your configuration.")
        return None

    # --- Define SQL queries for data extraction ---
    queries = {
        "customers": "SELECT * FROM Customers;",
        "orders": "SELECT * FROM Orders;",
        "order_details": "SELECT * FROM [Order Details];",
        "products": "SELECT * FROM Products;",
        "categories": "SELECT * FROM Categories;",
        "employees": "SELECT * FROM Employees;",
        "suppliers": "SELECT * FROM Suppliers;"
    }

    # --- Extract data from the database ---
    dataframes = {name: extract_data(engine, query) for name, query in queries.items()}

    # --- Check for extraction failures ---
    if any(df is None for df in dataframes.values()):
        st.error("Data extraction failed for one or more tables. Check logs for details.")
        return None

    # --- Transform data into comprehensive sales dataset ---
    sales_data = create_comprehensive_sales_data(
        orders=dataframes["orders"],
        order_details=dataframes["order_details"],
        products=dataframes["products"],
        categories=dataframes["categories"],
        employees=dataframes["employees"],
        customers=dataframes["customers"],
        suppliers=dataframes["suppliers"]
    )

    # --- Perform RFM analysis and segment customers ---
    rfm_segments = perform_rfm_analysis(sales_data)
    sales_data = pd.merge(sales_data, rfm_segments, on='CustomerID', how='left')

    # --- Load the final dataset ---
    final_sales_data = load_data(sales_data, "Comprehensive Sales Data")

    logging.info("ETL pipeline finished successfully.")
    return final_sales_data