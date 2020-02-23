"""
reference: https://www.tutorialspoint.com/python_data_access/python_mysql_create_table.htm
"""
from abc import abstractmethod
from .utils import create_table_query, insert_data_query
from .schema_defination import schema
from ..swag_config import DATABASE


class TableAlreadyExists(Exception):
    def __init__(self, message):
        self.message = message


class NoActvieDBConnection(Exception):
    def __init__(self, message):
        self.message = message


class BaseStore:
    # TODO: Add exception handling
    _already_initialized = False

    def __init__(self, host=None, port=None, username=None, password=None, database="swag"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.active_connection = None

    def connect(self):
        if not self._already_initialized:
            self._already_initialized = True
            self.active_connection = self.create_connection()
        return self.active_connection

    @abstractmethod
    def create_connection(self):
        pass

    def close_connection(self):
        if not self.active_connection:
            raise NoActvieDBConnection("No active database found")
        self.active_connection.close()
        self._already_initialized = False

    def _create_table(self, table_name):
        query = create_table_query(table_name)
        try:
            self.execute(query)
        except Exception:
            pass

    def create_tables(self):
        for table_name in schema.keys():
            self._create_table(table_name)

    def insert_data(self, table_name, **kwargs):
        query = insert_data_query(table_name, **kwargs)
        return self.execute(query)

    def get_all_experiment(self):
        query = """SELECT * FROM experiment"""
        return self.execute(query)

    def get_experiment_by_name(self, experiment_name):
        query = """SELECT * FROM experiment WHERE experiment_name = '{}'
        """.format(experiment_name)
        return self.execute(query)

    def get_experiment_by_id(self, experiment_id):
        query = """SELECT * FROM experiment WHERE experiment_id = '{}'
        """.format(experiment_id)
        return self.execute(query)

    def get_total_experiments(self):
        query = """SELECT COUNT(*) FROM experiment"""
        return self.execute(query)

    def get_unique_experiment_names(self):
        query = """SELECT DISTINCT(experiment_name) FROM experiment"""
        return self.execute(query)

    def get_runs_by_name(self, run_name):
        query = """SELECT * FROM run WHERE run_name = '{}'
        """.format(run_name)
        return self.execute(query)

    def get_runs_by_id(self, run_id):
        query = """SELECT * FROM run WHERE run_id = '{}'
        """.format(run_id)
        return self.execute(query)

    def get_runs_by_experiment_name(self, experiment_name):
        query = """SELECT * FROM run WHERE experiment_id IN (
        SELECT experiment_id FROM experiment WHERE experiment_name = '{}'
        )""".format(experiment_name)
        return self.execute(query)

    def get_runs_by_experiment_id(self, experiment_id):
        query = """SELECT * FROM run WHERE experiment_id IN (
        SELECT experiment_id FROM experiment WHERE experiment_id = '{}'
        )""".format(experiment_id)
        return self.execute(query)

    def get_models_by_run_name(self, run_name):
        query = """SELECT * FROM model WHERE run_id IN (
        SELECT run_id FROM run WHERE run_name = '{}'
        )""".format(run_name)
        return self.execute(query)

    def get_models_by_run_id(self, run_id):
        query = """SELECT * FROM model WHERE run_id IN (
        SELECT run_id FROM run WHERE run_id = '{}'
        )""".format(run_id)
        return self.execute(query)

    def get_params_by_run_name(self, run_name):
        query = """SELECT * FROM params WHERE run_id IN (
        SELECT run_id FROM run WHERE run_name = '{}'
        )""".format(run_name)
        return self.execute(query)

    def get_params_by_run_id(self, run_id):
        query = """SELECT * FROM params WHERE run_id IN (
        SELECT run_id FROM run WHERE run_id = '{}'
        )""".format(run_id)
        return self.execute(query)

    def get_params_by_model_name(self, model_name):
        query = """SELECT * FROM params WHERE model_id IN (
        SELECT model_id FROM model WHERE model_name = '{}'
        )""".format(model_name)
        return self.execute(query)

    def get_params_by_model_id(self, model_id):
        query = """SELECT * FROM params WHERE model_id IN (
        SELECT model_id FROM model WHERE model_id = '{}'
        )""".format(model_id)
        return self.execute(query)

    def get_metrics_by_run_name(self, run_name):
        query = """SELECT * FROM metric WHERE run_id IN (
        SELECT run_id FROM run WHERE run_name = '{}'
        )""".format(run_name)
        return self.execute(query)

    def get_metrics_by_run_id(self, run_id):
        query = """SELECT * FROM metric WHERE run_id IN (
        SELECT run_id FROM run WHERE run_id = '{}'
        )""".format(run_id)
        return self.execute(query)

    def get_metrics_by_model_name(self, model_name):
        query = """SELECT * FROM metric WHERE model_id IN (
        SELECT model_id FROM model WHERE model_name = '{}'
        )""".format(model_name)
        return self.execute(query)

    def get_metrics_by_model_id(self, model_id):
        query = """SELECT * FROM metric WHERE model_id IN (
        SELECT model_id FROM model WHERE model_id = '{}'
        )""".format(model_id)
        return self.execute(query)

    def get_optimizer_by_name(self, optimizer_name):
        query = """SELECT * FROM optimizer WHERE optimizer_name = '{}'
        """.format(optimizer_name)
        return self.execute(query)

    def get_optimizer_by_id(self, optimizer_id):
        query = """SELECT * FROM optimizer WHERE optimizer_id = '{}'
        """.format(optimizer_id)
        return self.execute(query)

    def get_optimizer_by_model_name(self, model_name):
        query = """SELECT * FROM optimizer WHERE model_id IN (
        SELECT model_id FROM model WHERE model_name = '{}'
        )""".format(model_name)
        return self.execute(query)

    def get_optimizer_by_model_id(self, model_id):
        query = """SELECT * FROM optimizer WHERE model_id IN (
        SELECT model_id FROM model WHERE model_id = '{}'
        )""".format(model_id)
        return self.execute(query)

    def get_optimizer_params_by_optimizer_id(self, optimizer_id):
        query = """SELECT * FROM optimizer_params WHERE optimizer_id = '{}'
        """.format(optimizer_id)
        return self.execute(query)

    def get_optimizer_params_by_optimizer_name(self, optimizer_name):
        query = """SELECT * FROM optimizer_params WHERE optimizer_name = '{}'
        """.format(optimizer_name)
        return self.execute(query)

    def get_run_metric_given_experiment_name(self, experiment_name):
        query = '''
        With k AS (
            SELECT experiment_id
            FROM experiment
            WHERE experiment_name = '{}'
        ),
        l AS (
            SELECT run_id, experiment_id, triggered_time
            FROM run
        ),
        m AS (
            SELECT metric_name, metric_value, run_id
            FROM metric
        )
        SELECT m.metric_name, m.metric_value, l.run_id, l.triggered_time
        FROM l 
        JOIN k ON l.experiment_id == k.experiment_id 
        JOIN m ON l.run_id == m.run_id
        ORDER BY l.triggered_time ASC
        '''.format(experiment_name)
        return self.execute(query)

    def get_run_metric_given_experiment_id(self, experiment_id):
        query = '''        
        WITH l AS (
            SELECT run_id, experiment_id, triggered_time
            FROM run
            WHERE experiment_id = '{}'
        ),
        m AS (
            SELECT metric_name, metric_value, run_id
            FROM metric
        )
        SELECT m.metric_name, m.metric_value, l.run_id, l.triggered_time
        FROM l 
        JOIN m ON l.run_id == m.run_id
        ORDER BY l.triggered_time ASC
        '''.format(experiment_id)
        return self.execute(query)

    def get_run_params_given_experiment_name(self, experiment_name):
        query = '''
        With k AS (
            SELECT experiment_id
            FROM experiment
            WHERE experiment_name = '{}'
        ),
        l AS (
            SELECT run_id, experiment_id, triggered_time
            FROM run
        ),
        m AS (
            SELECT param_name, param_value, run_id
            FROM params
        )
        SELECT m.param_name, m.param_value, l.run_id, l.triggered_time
        FROM l 
        JOIN k ON l.experiment_id == k.experiment_id 
        JOIN m ON l.run_id == m.run_id
        ORDER BY l.triggered_time ASC
        '''.format(experiment_name)
        return self.execute(query)

    def get_run_params_given_experiment_id(self, experiment_id):
        query = '''
        WITH l AS (
            SELECT run_id, experiment_id, triggered_time
            FROM run
            WHERE experiment_id = '{}'
        ),
        m AS (
            SELECT param_name, param_value, run_id
            FROM params
        )
        SELECT m.param_name, m.param_value, l.run_id, l.triggered_time
        FROM l 
        JOIN m ON l.run_id == m.run_id
        ORDER BY l.triggered_time ASC
        '''.format(experiment_id, experiment_id)
        return self.execute(query)

    def execute(self, query):
        cursor = self.active_connection.cursor()
        cursor.execute(query)
        self.active_connection.commit()
        return cursor


class SQLiteStore(BaseStore):
    import sqlite3

    def create_connection(self):
        database_details = DATABASE["SQLite"]
        sql_path = database_details["PATH"] + "/" + self.database + ".db"
        conn = self.sqlite3.connect(sql_path)
        return conn


class PostgreSQLStore(BaseStore):
    import psycopg2

    def create_connection(self):
        database_details = DATABASE["PostgreSQL"]
        conn = self.psycopg2.connect(
            database=self.database,
            user=database_details["USER"],
            password=database_details["PASSWORD"],
            host=database_details["HOST"],
            port=database_details["PORT"]
        )
        return conn


class MYSQLStore(BaseStore):
    from mysql import connector

    def create_connection(self):
        database_details = DATABASE["MSSQL"]
        conn = self.connector.connect(
            user=database_details["USER"],
            password=database_details["PASSWORD"],
            host=database_details["HOST"]
        )

        conn.autocommit = True

        query = "CREATE database {}".format(self.database)

        cursor = conn.cursor()
        cursor.execute(query)

        conn.close()

        conn = self.connector.connect(
            user=database_details["USER"],
            password=database_details["PASSWORD"],
            host=database_details["HOST"],
            database=self.database
        )

        return conn

