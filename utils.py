import pandas as pd
import sqlite3
import requests
from typing import List, Dict, Any
import os
from sqlalchemy import create_engine, Column, Float, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create base class for declarative models
Base = declarative_base()


class Freight(Base):
    """SQLAlchemy model for freight data"""

    __tablename__ = "freights"

    id = Column(Integer, primary_key=True)
    departure = Column(DateTime)
    origin_port_locode = Column(String)
    origin_port_name = Column(String)
    destination_port = Column(String)
    destination_port_name = Column(String)
    dv20rate = Column(Float)
    dv40rate = Column(Float)
    currency = Column(String)
    inserted_on = Column(DateTime)


def download_csv(url: str, local_path: str = "freights.csv") -> str:
    """
    Download CSV file from Hugging Face and save it locally
    """
    response = requests.get(url)
    with open(local_path, "wb") as f:
        f.write(response.content)
    return local_path


def create_database(db_name: str = "freights.db") -> None:
    """
    Create SQLite database and necessary tables
    """
    engine = create_engine(f"sqlite:///{db_name}")
    Base.metadata.create_all(engine)


def load_csv_to_db(csv_path: str, db_name: str = "freights.db") -> None:
    """
    Load CSV data into SQLite database
    """
    # Read CSV
    df = pd.read_csv(csv_path, parse_dates=["departure", "inserted_on"])

    # Connect to database
    engine = create_engine(f"sqlite:///{db_name}")

    # Save to database
    df.to_sql("freights", engine, if_exists="replace", index=False)


def initialize_database(csv_url: str) -> None:
    """
    Initialize the database by downloading CSV and loading data.
    Args:
        csv_url: URL of the CSV file to download and load.
    """
    # Download CSV
    csv_path = download_csv(csv_url)

    # Create and load database
    create_database()
    load_csv_to_db(csv_path)
    print("Database initialized.")

    # Clean up CSV file
    if os.path.exists(csv_path):
        os.remove(csv_path)
