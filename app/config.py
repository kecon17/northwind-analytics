"""
Configuration module to handle environment variables.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Reads environment variables from .env file."""

    DB_SERVER = os.getenv("DB_SERVER")
    DB_DATABASE = os.getenv("DB_DATABASE")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    @staticmethod
    def get_db_connection_string() -> str:
        """Constructs the database connection string.

        Supports both SQL Server Authentication and Windows Authentication.
        """
        if Config.DB_USERNAME and Config.DB_PASSWORD:
            # SQL Server Authentication
            return (
                f"mssql+pymssql://{Config.DB_USERNAME}:{Config.DB_PASSWORD}@"
                f"{Config.DB_SERVER}/{Config.DB_DATABASE}"
            )
        else:
            # Windows Authentication
            # pymssql on Windows will automatically use the current user's credentials
            # if username/password are not provided.
            return f"mssql+pymssql://{Config.DB_SERVER}/{Config.DB_DATABASE}"
