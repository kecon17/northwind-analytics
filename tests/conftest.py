"""
Pytest configuration and shared fixtures for the ETL pipeline.
"""
import pytest
import pandas as pd

@pytest.fixture(scope="session")
def sample_customers_df() -> pd.DataFrame:
    data = {'CustomerID': ['ALFKI', 'ANATR'], 'ContactName': ['Maria Anders', 'Ana Trujillo'], 'Country': ['Germany', 'Mexico']}
    return pd.DataFrame(data)

@pytest.fixture(scope="session")
def sample_orders_df() -> pd.DataFrame:
    data = {'OrderID': [10248, 10249], 'CustomerID': ['ALFKI', 'ANATR'], 'EmployeeID': [5, 3], 'OrderDate': ['1996-07-04', '1996-07-05'], 'ShippedDate': ['1996-07-16', '1996-07-10']}
    return pd.DataFrame(data)

@pytest.fixture(scope="session")
def sample_order_details_df() -> pd.DataFrame:
    data = {
        'OrderID': [10248, 10249], 'ProductID': [11, 14], 'UnitPrice': [14.0, 18.6],
        'Quantity': [12, 9], 'Discount': [0, 0.1]
    }
    return pd.DataFrame(data)

@pytest.fixture(scope="session")
def sample_products_df() -> pd.DataFrame:
    data = {'ProductID': [11, 14], 'ProductName': ['Queso Cabrales', 'Tofu'], 'CategoryID': [4, 6], 'SupplierID': [5, 6]}
    return pd.DataFrame(data)

@pytest.fixture(scope="session")
def sample_categories_df() -> pd.DataFrame:
    data = {'CategoryID': [4, 6], 'CategoryName': ['Dairy Products', 'Meat/Poultry']}
    return pd.DataFrame(data)

@pytest.fixture(scope="session")
def sample_employees_df() -> pd.DataFrame:
    data = {'EmployeeID': [3, 5], 'FirstName': ['Janet', 'Steven'], 'LastName': ['Leverling', 'Buchanan']}
    return pd.DataFrame(data)

@pytest.fixture(scope="session")
def sample_suppliers_df() -> pd.DataFrame:
    data = {'SupplierID': [5, 6], 'CompanyName': ['Cooperativa de Quesos', 'Mayumi\'s']}
    return pd.DataFrame(data)
