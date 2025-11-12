"""
Extract module to fetch data from the Northwind database.
"""

import logging
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from typing import Union

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_engine(connection_string: str):
    """Creates a SQLAlchemy engine.

    Args:
        connection_string (str): The database connection string.

    Returns:
        sqlalchemy.engine.Engine: The SQLAlchemy engine or None if connection fails.
    """
    try:
        engine = create_engine(connection_string)
        logging.info("Database engine created successfully.")
        return engine
    except SQLAlchemyError as e:
        logging.error(f"Error creating database engine: {e}")
        return None

def extract_data(engine, query: str) -> Union[pd.DataFrame, None]:
    """Extracts data from the database using a SQL query.

    Args:
        engine (sqlalchemy.engine.Engine): The SQLAlchemy engine.
        query (str): The SQL query to execute.

    Returns:
        pd.DataFrame: A DataFrame containing the query results, or None on error.
    """
    if not engine:
        logging.error("Database engine is not available.")
        return None

    try:
        with engine.connect() as connection:
            df = pd.read_sql_query(text(query), connection)
            logging.info(f"Successfully extracted {len(df)} rows.")
            return df
    except SQLAlchemyError as e:
        logging.error(f"Error extracting data: {e}")
        return None