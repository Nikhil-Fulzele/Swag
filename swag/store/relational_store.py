from .base_relational_store import SQLiteStore, PostgreSQLStore, MYSQLStore


class Store:
    def __init__(self, data_engine):
        self.data_engine = data_engine
        self.conn = self._store()
        self.conn.create_tables()

    def _store(self):
        store_mapping = {
            "SQLite": SQLiteStore(),
            "PostgreSQL": PostgreSQLStore(),
            "MYSQL": MYSQLStore()
        }
        return store_mapping[self.data_engine].create_connection()

    def insert_into_db(self, table_name, **kwargs):
        self.conn.insert_data(table_name, **kwargs)
