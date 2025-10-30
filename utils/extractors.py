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
            select parents.id      as parent_id, \
                   parents.name    as parent_name, \
                   categories.id   as category_id, \
                   categories.name as category_name
            from categories
                     left join categories as parents on coalesce(categories.parent_id, categories.id) = parents.id
            order by parents.id, categories.id \
            """
    df_cat = pd.read_sql(query, engine)
    return df_cat

def fetch_sample_transactions(limit=10):
    # Query the database
    query = f"""
            select transactions.id,
                   transaction_date,
                   description,
                   amount,
                   categories.name as category_name
            from transactions
                     left join categories on transactions.category_id = categories.id
            where account_id = 2 \
              and amount < 0
            order by transaction_date desc, description, id
            limit {limit} \
            """
    df_trans = pd.read_sql(query, engine).set_index('id')
    return df_trans