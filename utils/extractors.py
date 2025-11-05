import os
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
from dotenv import load_dotenv
load_dotenv()

db_url = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT', 15432)}/{os.getenv('DB_NAME')}"
engine = create_engine(db_url)

def fetch_categories():
    query = """
            select \
              * \
            from analytics.dim_budget_categories \
            """
    df_cat = pd.read_sql(query, engine).set_index('category_id')
    return df_cat

def fetch_sample_transactions(source='sapphire_reserve', limit=10):
    # Query the database
    query = f"""
            select transaction_id, \
                   transaction_date, \
                   transaction_description, \
                   amount \
            from analytics.fct_transactions \
            where source = '{source}' \
            limit {limit} \
            """
    df_trans = pd.read_sql(query, engine).set_index('transaction_id')
    return df_trans