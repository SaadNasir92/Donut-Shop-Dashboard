import pandas as pd


class Dimension_Modeler:
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe
        self.dimension_data_folder_path = "datasets/dimensions/"

    # Key adjustment is to allow flexibility in what order we want keys in.
    def make_id_col(self, key_name, key_adjustment=0):
        self.df[key_name] = (self.df.index + 1) + key_adjustment
        final_df = self.rearrange_cols(key_name)
        self.df = final_df
        return final_df

    def rearrange_cols(self, primary_key: str):
        new_order = [primary_key] + [
            col for col in self.df.columns if col != primary_key
        ]
        final_df = self.df[new_order]
        return final_df

    def make_csv(self, file_name):
        print(f"{file_name}.csv created in {self.dimension_data_folder_path}")
        return self.df.to_csv(
            f"{self.dimension_data_folder_path}{file_name}.csv", index=False
        )
