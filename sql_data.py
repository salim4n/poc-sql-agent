from sqlalchemy import create_engine, text
from smolagents import tool
import os
import pandas as pd

# Create database engine
engine = create_engine("sqlite:///freights.db")


@tool
def sql_query(query: str) -> str:
    """
    Allows you to perform SQL queries on the freights table. Returns a string representation of the result.
    The table is named 'freights'. Its description is as follows:
        Columns:
        - departure: DateTime (Date and time of departure)
        - origin_port_locode: String (Origin port code)
        - origin_port_name: String (Name of the origin port)
        - destination_port: String (Destination port code)
        - destination_port_name: String (Name of the destination port)
        - dv20rate: Float (Rate for 20ft container in USD)
        - dv40rate: Float (Rate for 40ft container in USD)
        - currency: String (Currency of the rates)
        - inserted_on: DateTime (Date when the rate was inserted)
    Args:
        query: The query to perform. This should be correct SQL.
    Returns:
        A string representation of the result of the query.
    """
    try:
        with engine.connect() as con:
            result = con.execute(text(query))
            rows = [dict(row._mapping) for row in result]

            if not rows:
                return "Aucun résultat trouvé."

            # Convert to markdown table
            headers = list(rows[0].keys())
            table = "| " + " | ".join(headers) + " |\n"
            table += "| " + " | ".join(["---" for _ in headers]) + " |\n"

            for row in rows:
                table += "| " + " | ".join(str(row[h]) for h in headers) + " |\n"

            return table

    except Exception as e:
        return f"Error executing query: {str(e)}"


@tool
def get_schema() -> str:
    """
    Returns the schema of the freights table.
    """
    return """
    Table: freights
    Columns:
    - departure: DateTime (Date and time of departure)
    - origin_port_locode: String (Origin port code)
    - origin_port_name: String (Name of the origin port)
    - destination_port: String (Destination port code)
    - destination_port_name: String (Name of the destination port)
    - dv20rate: Float (Rate for 20ft container in USD)
    - dv40rate: Float (Rate for 40ft container in USD)
    - currency: String (Currency of the rates)
    - inserted_on: DateTime (Date when the rate was inserted)
    """


@tool
def get_csv_as_dataframe() -> str:
    """
    Returns a string representation of the freights table as a CSV file.
    """
    df = pd.read_sql_table("freights", engine)
    return df.to_csv(index=False)
