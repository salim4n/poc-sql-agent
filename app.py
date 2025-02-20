import gradio as gr
from tools import FreightAgent, EXAMPLE_QUERIES
from utils import initialize_database
from smolagents import CodeAgent, HfApiModel, GradioUI
import os
from dotenv import load_dotenv
from sql_data import sql_query, get_schema, get_csv_as_dataframe

# Load environment variables
load_dotenv()

# Initialize the database if it doesn't exist
if not os.path.exists("freights.db"):
    csv_url = "https://huggingface.co/datasets/sasu-SpidR/fretmaritime/resolve/main/freights.csv"
    initialize_database(csv_url)

# Create the main agent
model_id = "meta-llama/Llama-3.3-70B-Instruct"
model = HfApiModel(model_id=model_id, token=os.environ["HF_API_KEY"])

agent = CodeAgent(tools=[sql_query, get_schema, get_csv_as_dataframe], model=model)

if __name__ == "__main__":
    GradioUI(agent).launch()
