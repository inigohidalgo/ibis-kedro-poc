import ibis
import pandas as pd


def filter_dates(data: ibis.table, start_date: str, end_date: str) -> ibis.table:
    return data.filter([data.date >= start_date, data.date <= end_date])


def ibis_table_to_df(data: ibis.table) -> pd.DataFrame:
    return data.execute()