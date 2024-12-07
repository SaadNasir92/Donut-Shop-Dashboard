from src.client_manager import ClientManager
from src.etl_manager import ETLManager
from src import MODEL_CONFIG
import pandas as pd


google_drive_client = ClientManager()
etl_manager = ETLManager(google_drive_client.files_to_process)

for file in etl_manager.files_to_process:
    new_file = file["name"]
    to_be_processed_df = pd.read_csv(new_file)

    for model_name, model_config in MODEL_CONFIG.items():
        model_file = f"{etl_manager.fact_dim_model_location}{model_name}.csv"
        model_df = pd.read_csv(model_file)

        if etl_manager.if_exists(new_file, model_name, model_config["merge_key"]):
            merged_df = etl_manager.perform_merge(
                to_be_processed_df, model_df, model_config["merge_key"]
            )
            final_df = etl_manager.drop_columns(
                model_config["columns_to_drop"], merged_df
            )
            to_be_processed_df = final_df
