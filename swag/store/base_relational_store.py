
class BaseStore:
    _already_initialized = False

    def __init__(self, host, port, username, password, database_obj, database):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database_obj = database_obj
        self.database = database
        self.active_connection = None

    def connect(self):
        if not self._already_initialized:
            self._already_initialized = True
            self.active_connection = self.create_connection()
        return self.active_connection

    def create_connection(self):
        conn = self.database_obj.connect(
            database=self.database,
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port
        )
        conn.autocommit = True
        return conn

    def crate_database(self, db_name):
        query = "CREATE database {}".format(db_name)
        self.execute(query)

    def close_connection(self):
        self.active_connection.close()
        self._already_initialized = False

    def create_table(self, table_name, table_schema):
        query = "CREATE TABLE {}({})".format(table_name, table_schema)
        self.execute(query)

    def get_cursor(self):
        return self.active_connection.cursor()

    def insert_data(self, table_name, columns, values):
        query = "INSERT INTO {}({}) VALUES {}".format(table_name, columns, values)
        self.execute(query)

    def execute(self, query):
        cursor = self.get_cursor()
        cursor.execute(query)
        return cursor


class BaseDataBaseOperations:
    # TODO: Separate Experiment and Run info from exp and runs
    # TODO: Schema and Insertion into table
    # TODO: Add exception handling
    def __init__(self, store_conn):
        self.store_conn = store_conn

    def insert_data(self, table_name, **kwargs):
        columns_names = ", ".join(kwargs.keys())
        columns_values = ", ".join([str(val) for val in kwargs.values()])
        query = """INSERT INTO {}({}) VALUES({}) """.format(table_name, columns_names, columns_values)
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
        SELECT experiment_id FROM experiment WHERE experiment_name = {}
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
        cursor = self.store_conn.execute(query)
        return cursor.fetchall()
