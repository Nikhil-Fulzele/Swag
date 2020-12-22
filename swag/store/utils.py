# TODO: include foreign key
# TODO: add create index
# TODO: standardized create table query
# TODO: create new file for all custom exception definitions

from .schema_defination import *
from ..utils.swag_exception import PrimaryKeyAlreadyExistsException

data_type_mapping = {
    INT: "INT",
    FLOAT: "FLOAT",
    STR: "VARCHAR",
    DATE: "timestamp"
}


def get_type(data_type):
    return data_type_mapping[data_type]


def schema_parser(input_schema):
    _is_prime_set = False
    final_schema = []
    for columns in input_schema:
        token_list = list()

        token_list.append(columns["column_name"])

        column_type = get_type(columns["data_type"])
        token_list.append(column_type)

        if column_type == "VARCHAR":
            size = "(" + str(columns["size"]) + ")"
            token_list[-1] += size

        if columns["is_not_null"]:
            token_list.append("NOT NULL")

        if columns["is_primary_key"]:
            if _is_prime_set:
                raise PrimaryKeyAlreadyExistsException("Table cannot have multiple primary keys")
            if not columns["is_not_null"]:
                token_list.append("NOT NULL")
            _is_prime_set = True
            token_list.append("PRIMARY KEY")
        final_schema.append(" ".join(token_list))

    return ", ".join(final_schema)


def create_table_query(table_name):
    _schema = schema[table_name]
    query = '''CREATE TABLE {}({})'''.format(table_name, schema_parser(_schema))
    return query


def insert_data_query(table_name, **kwargs):
    columns_names = ", ".join(kwargs.keys())
    columns_values = ", ".join(["'"+str(val)+"'" if type(val) in [str, type(None)] else str(val)
                                for val in kwargs.values()])
    query = """INSERT INTO {}({}) VALUES({}) """.format(table_name, columns_names, columns_values)
    return query
