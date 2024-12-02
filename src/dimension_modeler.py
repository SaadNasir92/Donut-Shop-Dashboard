import pandas as pd


class Dimension_Modeler:
    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe
        self.dimension_data_folder_path = "datasets/dimensions/"

    def make_id_col(self):
        self.df["id"] = self.df.index + 1
        dataframe = self.rearrange_cols("id")
        return dataframe

    def rearrange_cols(self, primary_key: str):
        new_order = [primary_key] + [
            col for col in self.df.columns if col != primary_key
        ]
        df = self.df[new_order]
        return df

    def make_csv(self, file_name):
        print(f"{file_name}.csv created in {self.dimension_data_folder_path}")
        return self.df.to_csv(
            f"{self.dimension_data_folder_path}{file_name}.csv", index=False
        )
