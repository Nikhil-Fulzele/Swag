from .base_relational_store import BaseStore


class Store:
    def __init__(self, **kwargs):
        backend_store = kwargs.pop("backend_store")

        if backend_store == "SQLite":
            import sqlite3
            self.conn = BaseStore(**kwargs, database_obj=sqlite3)

        if backend_store == "PostgreSQL":
            import psycopg2
            self.conn = BaseStore(**kwargs, database_obj=psycopg2)

        if backend_store == "MSSQL":
            import mysql.connector
            self.conn = BaseStore(**kwargs, database_obj=mysql.connector)
