import pandas as pd


class ETLManager:
    def __init__(self, processing_files: list[dict]) -> None:
        self.files_to_process: list[dict] = processing_files
        self.transformed_data: dict = {}

        self.logs_file = "datasets/client_shared/logs/etl_logs.txt"
        self.fact_dim_model_location = "datasets/fact_dimensions_models/"

        self.log_process("Performing Transformations...")

    def log_process(self, info):
        with open(self.logs_file, "a") as file:
            file.write(f"{info}\n")

    def if_exists(
        self,
        new_df: pd.DataFrame,
        model_df: pd.DataFrame,
        left_col_name: str,
        right_col_name: str,
    ) -> bool:
        for value in new_df[left_col_name].unique():
            if value not in model_df[right_col_name].values:
                self.log_process(f"{value} not found.")
                # Perform add fucntion.
            else:
                pass

        return True

    def perform_merge(
        self,
        new_df: pd.DataFrame,
        model_df: pd.DataFrame,
        left_key: str | list[str],
        right_key: str | list[str],
        type_: str = "inner",
    ) -> pd.DataFrame:
        final_df = pd.merge(
            new_df, model_df, how=type_, left_on=left_key, right_on=right_key
        )
        return final_df

    def drop_columns(self, cols_to_drop: list[str], dataframe: pd.DataFrame):
        return dataframe.drop(columns=cols_to_drop)

    def fix_dim_promotions(self, dataframe: pd.DataFrame):
        dataframe["promo_name"] = dataframe["promo_name"].str.upper()
        dataframe["promo_name"] = dataframe["promo_name"].fillna("NO PROMO")
        return dataframe

    def handle_dim_products(self, left_df, right_df, left_keys, right_keys) -> bool:
        merged_df = pd.merge(
            left_df,
            right_df,
            how="left",
            left_on=left_keys,
            right_on=right_keys,
            indicator=True,
        )
        return merged_df

    def if_exists_products(self, df):
        if len(df.loc[df["_merge"] == "left_only", :]) == 0:
            self.log_process("All product & price combos current...")
            return True
        else:
            pass
            # Add price & do SCD2 logic.
