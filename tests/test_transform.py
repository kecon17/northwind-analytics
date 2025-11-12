"""
Unit tests for the main ETL transform function.
"""
import pandas as pd
import pytest
from app.etl.transform import create_comprehensive_sales_data

def test_create_comprehensive_sales_data(
    sample_orders_df, sample_order_details_df, sample_products_df,
    sample_categories_df, sample_employees_df, sample_customers_df, sample_suppliers_df
):
    """
    Tests the end-to-end data transformation and enrichment pipeline.
    """
    # --- 1. Execute the function under test ---
    result_df = create_comprehensive_sales_data(
        orders=sample_orders_df,
        order_details=sample_order_details_df,
        products=sample_products_df,
        categories=sample_categories_df,
        employees=sample_employees_df,
        customers=sample_customers_df,
        suppliers=sample_suppliers_df
    )

    # --- 2. Assertions to validate the output ---

    # Assert that the DataFrame is not empty and has the expected shape
    assert not result_df.empty
    assert result_df.shape[0] == 2  # We expect 2 rows from our sample data

    # Assert that all expected columns (including new ones) are present
    expected_cols = [
        'Revenue', 'EmployeeName', 'SupplierName', 'Region', 'CountryISO3',
        'ShippedDate'
    ]
    for col in expected_cols:
        assert col in result_df.columns

    # Assert the correctness of a calculated 'Revenue' column
    # Order 10248: 14.0 * 12 * (1-0) = 168.0
    # Order 10249: 18.6 * 9 * (1-0.1) = 150.66
    assert result_df[result_df['OrderID'] == 10248]['Revenue'].iloc[0] == pytest.approx(168.0)
    assert result_df[result_df['OrderID'] == 10249]['Revenue'].iloc[0] == pytest.approx(150.66)

    # Assert the correctness of a merged 'EmployeeName' column
    assert result_df[result_df['OrderID'] == 10248]['EmployeeName'].iloc[0] == 'Steven Buchanan'
    assert result_df[result_df['OrderID'] == 10249]['EmployeeName'].iloc[0] == 'Janet Leverling'

    # Assert the correctness of the enriched 'Region' and 'CountryISO3' columns
    order_10248_row = result_df[result_df['OrderID'] == 10248].iloc[0]
    assert order_10248_row['Country'] == 'Germany'
    assert order_10248_row['Region'] == 'Europe'
    assert order_10248_row['CountryISO3'] == 'DEU'

    # Assert that the ShippedDate column has the correct data type
    assert pd.api.types.is_datetime64_any_dtype(result_df['ShippedDate'])