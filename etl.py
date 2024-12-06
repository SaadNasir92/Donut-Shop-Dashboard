from src.client_manager import ClientManager
from src.database_manager import DatabaseManager
from src.etl_manager import ETLManager
import pandas as pd

google_drive_client = ClientManager()

files_to_process_raw = google_drive_client.files_to_process
files_to_process = [
    f"{google_drive_client.to_be_processed_folder}{file}"
    for file in files_to_process_raw
]
