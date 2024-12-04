import pandas as pd


def update_start_date(df: pd.DataFrame):
    most_recent_end_date = df.loc[~df["is_current"], "end_date"].max()
    df.loc[df["is_current"], "start_date"] = most_recent_end_date
    return df


def quick_merge(df1, df2, type_="inner", left_key=None, right_key=None):
    combined_df = pd.merge(df1, df2, how=type_, left_on=left_key, right_on=right_key)
    return combined_df
