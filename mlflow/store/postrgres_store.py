import psycopg2

from mlflow.store.abstract_store import AbstractStore
from mlflow.utils.postgres_utils import PostgresDB


EXPERIMENTS_SCHEMA = """
id SERIAL PRIMARY KEY,
name TEXT
"""
METRICS_SCHEMA = """
id SERIAL PRIMARY KEY,
run_uuid CHAR(32),
key TEXT,
value FLOAT8
"""
PARAMS_SCHEMA = """
id SERIAL PRIMARY KEY,
run_uuid CHAR(32),
key TEXT,
value TEXT
"""
RUN_SCHEMA = """
id SERIAL PRIMARY KEY,
run_uuid CHAR(32),
experiment_id INT4,
name TEXT
source_type INT2,
source_name TEXT,
user_id TEXT,
status INT2,
start_time INT8,
end_time INT8,
source_version TEXT
entry_point_name TEXT
"""
ARTIFACTS_SCHEMA = """
id SERIAL PRIMARY KEY
"""


class PostgresStore(AbstractStore):
    EXPERIMENTS_TABLE_NAME = "mlflow_experiments"
    ARTIFACTS_TABLE_NAME = "mlflow_artifacts"
    METRICS_TABLE_NAME = "mlflow_metrics"
    PARAMS_TABLE_NAME = "mlflow_params"

    EXPERIMENTS_TABLE_SCHEMA = EXPERIMENTS_SCHEMA
    ARTIFACTS_TABLE_SCHEMA = ARTIFACTS_SCHEMA
    METRICS_TABLE_SCHEMA = METRICS_SCHEMA
    PARAMS_TABLE_SCHEMA = PARAMS_SCHEMA

    def __init__(self, connection_uri):
        self._uri = connection_uri
        self._db = PostgresDB(self._uri)
        if not self._db.table_exists(PostgresStore.EXPERIMENTS_TABLE_NAME):
            self._db.create_table(PostgresStore.EXPERIMENTS_TABLE_NAME,
                                  PostgresStore.EXPERIMENTS_TABLE_SCHEMA)