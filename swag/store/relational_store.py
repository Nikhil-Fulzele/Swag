"""
reference: https://www.tutorialspoint.com/python_data_access/python_mysql_create_table.htm
"""
from abc import abstractmethod
from .utils import create_table_query, insert_data_query
from .schema_defination import schema
from configparser import RawConfigParser

config = RawConfigParser()
config_file_path = '../swag.config'
config.read(config_file_path)


class BaseStore:
    # TODO: Add exception handling
    _already_initialized = False

    def __init__(self, host, port, username, password, database="swag"):
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
        self.active_connection.close()
        self._already_initialized = False

    def _create_table(self, table_name):
        query = create_table_query(table_name)
        self.execute(query)

    def create_tables(self):
        for table_name in schema.keys():
            self._create_table(table_name)

    def get_cursor(self):
        return self.active_connection.cursor()

    def insert_data(self, table_name, **kwargs):
        query = insert_data_query(table_name, **kwargs)
        return self.execute(query)

    def get_all_experiment(self):
        query = """SELECT * FROM experiment"""
        return self.execute(query)

    def get_experiment_by_name(self, experiment_name):
        query = """SELECT * FROM experiment WHERE experiment_name = {}
        """.format(experiment_name)
        return self.execute(query)

    def get_experiment_by_id(self, experiment_id):
        query = """SELECT * FROM experiment WHERE experiment_id = {}
        """.format(experiment_id)
        return self.execute(query)

    def get_total_experiments(self):
        query = """SELECT COUNT(*) FROM experiment"""
        return self.execute(query)

    def get_runs_by_name(self, run_name):
        query = """SELECT * FROM runs WHERE run_name = {}
        """.format(run_name)
        return self.execute(query)

    def get_runs_by_id(self, run_id):
        query = """SELECT * FROM runs WHERE run_id = {}
        """.format(run_id)
        return self.execute(query)

    def get_runs_by_experiment_name(self, experiment_name):
        query = """SELECT * FROM runs WHERE experiment_id IN (
        SELECT experiment_id FROM experiment WHERE experiment_name = {}
        )""".format(experiment_name)
        return self.execute(query)

    def get_runs_by_experiment_id(self, experiment_id):
        query = """SELECT * FROM runs WHERE experiment_id IN (
        SELECT experiment_id FROM experiment WHERE experiment_id = {}
        )""".format(experiment_id)
        return self.execute(query)

    def get_models_by_run_name(self, run_name):
        query = """SELECT * FROM model WHERE run_id IN (
        SELECT run_id FROM runs WHERE run_name = {}
        )""".format(run_name)
        return self.execute(query)

    def get_models_by_run_id(self, run_id):
        query = """SELECT * FROM model WHERE run_id IN (
        SELECT run_id FROM runs WHERE run_id = {}
        )""".format(run_id)
        return self.execute(query)

    def get_params_by_run_name(self, run_name):
        query = """SELECT * FROM params WHERE run_id IN (
        SELECT run_id FROM runs WHERE run_name = {}
        )""".format(run_name)
        return self.execute(query)

    def get_params_by_run_id(self, run_id):
        query = """SELECT * FROM params WHERE run_id IN (
        SELECT run_id FROM runs WHERE run_id = {}
        )""".format(run_id)
        return self.execute(query)

    def get_params_by_model_name(self, model_name):
        query = """SELECT * FROM params WHERE model_id IN (
        SELECT model_id FROM model WHERE model_name = {}
        )""".format(model_name)
        return self.execute(query)

    def get_params_by_model_id(self, model_id):
        query = """SELECT * FROM params WHERE model_id IN (
        SELECT model_id FROM model WHERE model_id = {}
        )""".format(model_id)
        return self.execute(query)

    def get_metrics_by_run_name(self, run_name):
        query = """SELECT * FROM metrics WHERE run_id IN (
        SELECT run_id FROM runs WHERE run_name = {}
        )""".format(run_name)
        return self.execute(query)

    def get_metrics_by_run_id(self, run_id):
        query = """SELECT * FROM metrics WHERE run_id IN (
        SELECT run_id FROM runs WHERE run_id = {}
        )""".format(run_id)
        return self.execute(query)

    def get_metrics_by_model_name(self, model_name):
        query = """SELECT * FROM metrics WHERE model_id IN (
        SELECT model_id FROM model WHERE model_name = {}
        )""".format(model_name)
        return self.execute(query)

    def get_metrics_by_model_id(self, model_id):
        query = """SELECT * FROM metrics WHERE model_id IN (
        SELECT model_id FROM model WHERE model_id = {}
        )""".format(model_id)
        return self.execute(query)

    def get_optimizer_by_name(self, optimizer_name):
        query = """SELECT * FROM optimizer WHERE optimizer_name = {}
        """.format(optimizer_name)
        return self.execute(query)

    def get_optimizer_by_id(self, optimizer_id):
        query = """SELECT * FROM optimizer WHERE optimizer_id = {}
        """.format(optimizer_id)
        return self.execute(query)

    def get_optimizer_by_model_name(self, model_name):
        query = """SELECT * FROM optimizer WHERE model_id IN (
        SELECT model_id FROM model WHERE model_name = {}
        )""".format(model_name)
        return self.execute(query)

    def get_optimizer_by_model_id(self, model_id):
        query = """SELECT * FROM optimizer WHERE model_id IN (
        SELECT model_id FROM model WHERE model_id = {}
        )""".format(model_id)
        return self.execute(query)

    def get_optimizer_params_by_optimizer_id(self, optimizer_id):
        query = """SELECT * FROM optimizer_params WHERE optimizer_id = {}
        """.format(optimizer_id)
        return self.execute(query)

    def get_optimizer_params_by_optimizer_name(self, optimizer_name):
        query = """SELECT * FROM optimizer_params WHERE optimizer_name = {}
        """.format(optimizer_name)
        return self.execute(query)

    def execute(self, query):
        cursor = self.get_cursor()
        cursor.execute(query)
        return cursor


class SQLiteStore(BaseStore):
    import sqlite3

    def create_connection(self):
        _database = dict(config.items("DATABASE"))
        database_details = _database["SQLite"]
        sql_path = database_details["PATH"] + "/" + self.database + ".db"
        conn = self.sqlite3.connect(sql_path)
        return conn


class PostgreSQLStore(BaseStore):
    import psycopg2

    def create_connection(self):
        _database = dict(config.items("DATABASE"))
        database_details = _database["PostgreSQL"]
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
        _database = dict(config.items("DATABASE"))
        database_details = _database["MSSQL"]
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
