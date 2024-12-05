from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2 import service_account
import io
from googleapiclient.http import MediaIoBaseDownload
import pandas as pd

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
