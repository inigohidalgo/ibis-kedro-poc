from kedro.pipeline import node, Pipeline

from .ingest_nodes import create_dataframe, filter_dates, ibis_table_to_df

ingest_pipeline = Pipeline(
    [
        node(
            func=create_dataframe,
            inputs=None,
            outputs="raw_table",
        ),
        node(
            func=filter_dates,
            inputs=["raw_table", "params:date_from", "params:date_to"],
            outputs="filtered_data",
        ),
        node(
            func=ibis_table_to_df,
            inputs="filtered_data",
            outputs="data_df",
        )
    ]
)