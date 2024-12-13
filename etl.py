from src.client_manager import ClientManager
from src.etl_manager import ETLManager
from src import MODEL_CONFIG
import pandas as pd
import time

start_time = time.perf_counter()

google_drive_client = ClientManager()

end_time_google_drive = time.perf_counter()

elapsed_time_google_drive = end_time_google_drive - start_time

google_drive_client.log_process(
    f"Total file lookup & extraction processing time: {round(elapsed_time_google_drive, 4)} seconds."
)
google_drive_client.log_process("******************" * 50)

etl_manager = ETLManager(google_drive_client.files_to_process)

transformation_time_stamp = google_drive_client.time_stamp

for file in etl_manager.files_to_process:
    new_file = file["name"]
    to_be_processed_df = pd.read_csv(new_file)
    to_be_processed_df = etl_manager.fix_dim_promotions(to_be_processed_df)
    to_be_processed_df = etl_manager.create_date_ids(to_be_processed_df)

    for model_name, model_config in MODEL_CONFIG.items():
        model_file = f"{etl_manager.fact_dim_model_location}{model_name}.csv"
        model_df = pd.read_csv(model_file)

        if etl_manager.if_exists(
            to_be_processed_df,
            model_df,
            model_config["merge_key_left"],
            model_config["merge_key_right"],
        ):
            if model_config["logic_code"] == 1:
                etl_manager.log_process(
                    f"Merging new data with respective model: {model_name}."
                )
                merged_df = etl_manager.perform_merge(
                    to_be_processed_df,
                    model_df,
                    model_config["merge_key_left"],
                    model_config["merge_key_right"],
                )
                final_df = etl_manager.drop_columns(
                    model_config["columns_to_drop"], merged_df
                )
                to_be_processed_df = final_df
                etl_manager.log_process(f"{model_name} merge complete.")

            elif model_config["logic_code"] == 2:
                etl_manager.log_process(
                    f"Merging new data with respective model: {model_name}."
                )
                merged_df = etl_manager.handle_dim_products(
                    to_be_processed_df,
                    model_df[model_config["model_join_columns"]],
                    model_config["join_key_left"],
                    model_config["join_key_right"],
                )
                if etl_manager.if_exists_products(merged_df):
                    final_df = etl_manager.drop_columns(
                        model_config["columns_to_drop"], merged_df
                    )
                to_be_processed_df = final_df
                etl_manager.log_process(f"{model_name} merge complete.")

            else:
                etl_manager.log_process(
                    f"Merging new data with respective model: {model_name}."
                )
                to_be_processed_df = etl_manager.drop_columns(
                    model_config["columns_to_drop"], to_be_processed_df
                )
                etl_manager.log_process(f"{model_name} merge complete.")


end_time_etl = time.perf_counter()
elapsed_time_etl = end_time_etl - start_time

etl_manager.log_process(
    f"Transformation for all {len(etl_manager.files_to_process)} file(s): completed at {transformation_time_stamp}."
)
etl_manager.log_process(
    f"Total transformation processing time: {round(elapsed_time_etl, 4)} seconds."
)
etl_manager.log_process("***********************************************" * 50)
