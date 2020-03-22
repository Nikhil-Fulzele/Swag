from .base_relational_store import SQLiteStore, PostgreSQLStore, MYSQLStore


class Store:
    def __init__(self, data_engine):
        self.data_engine = data_engine
        self.store = self._store()
        self.conn = self.store.connect()
        self.store.create_tables()

    def _store(self):
        store_mapping = {
            "SQLite": SQLiteStore,
            "PostgreSQL": PostgreSQLStore,
            "MYSQL": MYSQLStore
        }
        return store_mapping[self.data_engine]()

    def insert_into_db(self, table_name, **kwargs):
        self.store.insert_data(table_name, **kwargs)
