# djohodo/db.py
from pathlib import Path
import duckdb
import pandas as pd
from djohodo.config import WAREHOUSE_PATH


def get_connection():
    """Retourne une connexion DuckDB."""
    return duckdb.connect(str(WAREHOUSE_PATH))


def load_job_category_counts():
    con = get_connection()
    df = con.execute("SELECT * FROM gold_job_category_counts ORDER BY count DESC").df()
    con.close()
    return df


def load_job_categories_df() -> pd.DataFrame:
    """
    Charge les données nécessaires pour le graphique des job_category.
    """
    con = get_connection()
    query = """
    SELECT 
        j.job_id,
        j.job_category,
        j.job_sector,
        sk.skill_slug
    FROM stg_job j
    LEFT JOIN stg_job_skill js ON j.job_id = js.job_id
    LEFT JOIN stg_skill sk ON js.skill_id = sk.skill_id
    """
    df = con.sql(query).df()
    con.close()
    return df
