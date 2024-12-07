import pandas as pd


class ETLManager:
    def __init__(self, processing_files: list[dict]) -> None:
        self.files_to_process: list[dict] = processing_files
        self.transformed_data: dict = {}
        self.logs_file = "datasets/client_shared/logs/etl_logs.txt"
        self.fact_dim_model_location = "datasets/fact_dimensions_models/"

    def log_process(self, info):
        with open(self.logs_file, "a") as file:
            file.write(f"{info}\n")

    def if_exists(self, new_csv_path: str, model_csv_name: str, col_name: str) -> bool:
        model_file_path = f"{self.fact_dim_model_location}{model_csv_name}.csv"
        model_df = pd.read_csv(model_file_path)
        df = pd.read_csv(new_csv_path)

        for name in df[col_name].unique():
            if name not in model_df[col_name].values:
                self.log_process(f"{name} not found.")
                # Perform add fucntion.
        return True

    def perform_merge(
        self, new_df: pd.DataFrame, model_df: pd.DataFrame, merge_key: str
    ) -> pd.DataFrame:
        final_df = pd.merge(new_df, model_df, how="inner", on=merge_key)
        return final_df

    def drop_columns(self, cols_to_drop: list[str], dataframe: pd.DataFrame):
        return dataframe.drop(columns=cols_to_drop)
