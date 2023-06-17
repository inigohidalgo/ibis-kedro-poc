# Ibis Kedro PoC

Small proof-of-concept kedro pipeline loading data from SQL using [`kedro-ibis-dataset`](https://pypi.org/project/kedro-ibis-dataset/)

## How to run

### 1. Install project

```bash
python -m pip install .
```


### 2. Run pipeline
```bash
python -m kedro run --pipeline ingest
```