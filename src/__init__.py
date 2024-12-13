from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account


# Globals
load_dotenv()
DRIVE_API_KEYS_FILE = os.getenv("DRIVE_API_CLIENT_FILE_PATH")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")

# Googledrive API setup

service_account_keys_file = DRIVE_API_KEYS_FILE

SCOPES = ["https://www.googleapis.com/auth/drive"]

credentials = service_account.Credentials.from_service_account_file(
    service_account_keys_file, scopes=SCOPES
)

SERVICE = build("drive", "v3", credentials=credentials)


# Database setup
DB_URL = f"postgresql+psycopg2://postgres:{DB_PASS}@localhost:5432/{DB_NAME}"
ENGINE = create_engine(DB_URL, isolation_level="AUTOCOMMIT")

# ETL Model Configuration
# Logic code will refer to what process to occur during transformation.
MODEL_CONFIG = {
    "dim_employees": {
        "merge_key_left": "employee_name",
        "merge_key_right": "employee_name",
        "columns_to_drop": ["employee_name", "job_title"],
        "logic_code": 1,
    },
    "dim_promotions": {
        "merge_key_left": "promo_name",
        "merge_key_right": "promotion_name",
        "columns_to_drop": [
            "promo_name",
            "promotion_name",
            "discount_percentage",
            "description",
        ],
        "logic_code": 1,
    },
    "dim_payment_methods": {
        "merge_key_left": "payment_method",
        "merge_key_right": "payment_method",
        "columns_to_drop": ["payment_method"],
        "logic_code": 1,
    },
    "dim_dates": {
        "merge_key_left": "date_id",
        "merge_key_right": "date_id",
        "columns_to_drop": ["date_raw"],
        "logic_code": 3,
    },
    "dim_products": {
        "merge_key_left": "product_name",
        "merge_key_right": "product_name",
        "columns_to_drop": [
            "price_per_unit",
            "product_name",
            "product_price",
            "category",
            "_merge",
        ],
        "logic_code": 2,
        "join_key_left": ["product_name", "price_per_unit"],
        "join_key_right": ["product_name", "product_price"],
        "model_join_columns": ["product_key", "product_name", "product_price"],
    },
}
