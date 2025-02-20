from smolagents import CodeAgent, HfApiModel
from sql_data import sql_query, get_schema
from sqlalchemy import create_engine, inspect, text
import os
from dotenv import load_dotenv
from typing import Dict, List, Any
import json

# Load environment variables
load_dotenv()

# Example queries that the agent can handle
EXAMPLE_QUERIES = [
    "Quels sont les tarifs moyens des conteneurs 20ft et 40ft entre tous les ports ?",
    "Quels sont les ports d'origine les plus fréquents ?",
    "Montre-moi les routes avec des tarifs élevés pour les conteneurs 40ft",
    "Quelle est l'évolution des prix au fil du temps pour la route Surabaya vers Nansha ?",
    "Quelles sont les destinations disponibles depuis Shanghai ?",
]


class FreightAgent:
    def __init__(self):
        self.setup_agent()

    def setup_agent(self) -> None:
        """
        Initialize the CodeAgent with SQL tools.
        Create a CodeAgent with two tools: `sql_query` and `get_schema`.
        `sql_query` allows to perform SQL queries on the freights table.
        `get_schema` returns the schema of the freights table.
        """
        self.agent = CodeAgent(
            tools=[sql_query, get_schema],
            model=HfApiModel("meta-llama/Llama-3.1-8B-Instruct"),
        )

    def query(self, question: str) -> str:
        """
        Ask a question about the freight data in natural language
        """
        return self.agent.run(question)
