from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


load_dotenv()
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

DB_URL = f"postgresql+psycopg2://postgres:{DB_PASS}@localhost:5432/{DB_NAME}"
ENGINE = create_engine(DB_URL, isolation_level="AUTOCOMMIT")
