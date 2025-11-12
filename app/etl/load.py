"""
Load module for the ETL pipeline.

In this project, 'load' simply means returning the transformed data
to the Streamlit application for display.
"""

import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(df: pd.DataFrame, description: str) -> pd.DataFrame:
    """'Loads' the data by logging a message and returning it.

    Args:
        df (pd.DataFrame): The transformed DataFrame.
        description (str): A description of the data being loaded.

    Returns:
        pd.DataFrame: The same DataFrame that was passed in.
    """
    if not isinstance(df, pd.DataFrame):
        logging.error("Load function received an object that is not a DataFrame.")
        return pd.DataFrame() # Return empty DataFrame on error

    logging.info(f"Successfully loaded {description} with {len(df)} rows.")
    return df