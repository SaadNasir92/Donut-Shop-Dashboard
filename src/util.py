import pandas as pd


def update_start_date(df: pd.DataFrame):
    most_recent_end_date = df.loc[~df["is_current"], "end_date"].max()
    df.loc[df["is_current"], "start_date"] = most_recent_end_date
    return df
