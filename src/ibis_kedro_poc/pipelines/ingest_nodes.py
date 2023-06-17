import ibis
import pandas as pd

def create_dataframe() -> pd.DataFrame:
    test_data = pd.DataFrame({
    "date": pd.date_range("2022-01-01", "2022-01-10"),
    "group": ["A","A","A","A","A","B","B","B","B","B",],
    "value":[1,2,3,4,5,6,7,8,9,10]
})
    return test_data

def filter_dates(data: ibis.table, start_date: str, end_date: str) -> ibis.table:
    return data.filter([data.date >= start_date, data.date <= end_date])


def ibis_table_to_df(data: ibis.table) -> pd.DataFrame:
    return data.to_pandas()