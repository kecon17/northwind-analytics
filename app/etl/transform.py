"""
Transform module for creating a comprehensive, analysis-ready sales dataset.
"""

import pandas as pd
from .utils import map_country_to_region, map_country_to_iso3

def create_comprehensive_sales_data(
    orders: pd.DataFrame,
    order_details: pd.DataFrame,
    products: pd.DataFrame,
    categories: pd.DataFrame,
    employees: pd.DataFrame,
    customers: pd.DataFrame,
    suppliers: pd.DataFrame
) -> pd.DataFrame:
    """Merges and transforms raw data tables into a single, rich sales overview DataFrame.

    This function calculates revenue, joins product and category information, and adds
    details about the customer and the sales employee responsible for the order.

    Returns:
        pd.DataFrame: A comprehensive DataFrame ready for analytics.
    """
    # --- Calculate Revenue for each item ---
    order_details['Revenue'] = order_details['UnitPrice'] * order_details['Quantity'] * (1 - order_details['Discount'])

    # --- Create clean, pre-selected DataFrames to avoid column conflicts ---
    product_info = products[['ProductID', 'ProductName', 'SupplierID', 'CategoryID']]
    customers_info = customers[['CustomerID', 'ContactName', 'Country']]
    employees_info = employees[['EmployeeID', 'FirstName', 'LastName']].assign(EmployeeName=lambda x: x.FirstName + ' ' + x.LastName)
    suppliers_info = suppliers[['SupplierID', 'CompanyName']].rename(columns={'CompanyName': 'SupplierName'})

    # --- Build the final DataFrame with controlled merges ---
    sales_data = order_details.copy()
    sales_data = pd.merge(sales_data, product_info, on='ProductID', how='left')
    sales_data = pd.merge(sales_data, categories, on='CategoryID', how='left')
    sales_data = pd.merge(sales_data, suppliers_info, on='SupplierID', how='left')
    sales_data = pd.merge(sales_data, orders, on='OrderID', how='left')
    sales_data = pd.merge(sales_data, customers_info, on='CustomerID', how='left')
    sales_data = pd.merge(sales_data, employees_info, on='EmployeeID', how='left')

    # --- Convert date columns to datetime ---
    sales_data['OrderDate'] = pd.to_datetime(sales_data['OrderDate'])
    sales_data['ShippedDate'] = pd.to_datetime(sales_data['ShippedDate'])

    # --- Map Country to Region and ISO3 ---
    sales_data['Region'] = sales_data['Country'].apply(map_country_to_region)
    sales_data['CountryISO3'] = sales_data['Country'].apply(map_country_to_iso3)

    # --- Select and order final columns ---
    final_columns = [
        'OrderID', 'OrderDate', 'ShippedDate', 'CustomerID', 'ContactName',
        'Region', 'Country', 'CountryISO3',
        'EmployeeID', 'EmployeeName', 'ProductID', 'ProductName',
        'CategoryID', 'CategoryName', 'SupplierID', 'SupplierName',
        'UnitPrice', 'Quantity', 'Discount', 'Revenue'
    ]
    
    return sales_data[final_columns]

def perform_rfm_analysis(sales_data: pd.DataFrame) -> pd.DataFrame:
    """Performs RFM analysis to segment customers.

    Args:
        sales_data (pd.DataFrame): The comprehensive sales data.

    Returns:
        pd.DataFrame: A DataFrame with CustomerID and their RFM segments.
    """
    # --- Ensure OrderDate is datetime ---
    sales_data['OrderDate'] = pd.to_datetime(sales_data['OrderDate'])
    snapshot_date = sales_data['OrderDate'].max() + pd.DateOffset(days=1)

    # --- Calculate RFM metrics ---
    rfm = sales_data.groupby('CustomerID').agg({
        'OrderDate': lambda date: (snapshot_date - date.max()).days, # Recency
        'OrderID': 'nunique', # Frequency
        'Revenue': 'sum' # Monetary
    })

    rfm.rename(columns={'OrderDate': 'Recency', 'OrderID': 'Frequency', 'Revenue': 'MonetaryValue'}, inplace=True)

    # --- Assign RFM scores ---
    rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1]) # Higher score is better (more recent)
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 4, labels=[1, 2, 3, 4])
    rfm['M_Score'] = pd.qcut(rfm['MonetaryValue'], 4, labels=[1, 2, 3, 4])

    rfm['RFM_Segment'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
    
    # --- Define segments based on RFM scores ---
    segment_map = {
        r'[1-2][1-2]': 'Hibernating',
        r'[1-2][3-4]': 'At-Risk',
        r'3[1-2]': 'Needs Attention',
        r'33': 'Loyal Customers',
        r'[3-4][4]': 'Champions',
        r'4[1-3]': 'Potential Loyalists',
    }

    rfm['Segment'] = 'Other'
    for regex, segment in segment_map.items():
        rfm.loc[rfm['RFM_Segment'].str.match(regex), 'Segment'] = segment

    return rfm[['Segment']]