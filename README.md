# Ibis Kedro PoC

Small proof-of-concept kedro pipeline loading data from SQL using `kedro-ibis-dataset`

## Replication

### Initiate database

Run the first section of the notebook `"notebooks/230604-initial-testing.ipynb"` to recreate the database which is input for the pipeline

### Run data ingestion pipeline

```bash
python -m kedro run --pipeline ingest
```