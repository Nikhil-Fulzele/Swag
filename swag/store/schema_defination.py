from datetime import datetime

INT = int()
FLOAT = float()
STR = str()
DATE = datetime
BOOL = bool()

"""
schema has following format
<table_name> : [
        {
            column_name: <column_name>, 
            data_type: <data_type>,
            size: <size>,
            is_primary_key: BOOL,
            is_foreign_key: BOOL,
            is_not_null: BOOL,
            is_index: BOOL
        }
    ]
}
"""
schema = {
    "experiment": [
        {
            "column_name": "experiment_id",
            "data_type": STR,
            "size": 32,
            "is_primary_key": True,
            "is_foreign_key": False,
            "is_not_null": True,
            "is_index": True
        },
        {
            "column_name": "experiment_name",
            "data_type": STR,
            "size": 100,
            "is_primary_key": False,
            "is_foreign_key": False,
            "is_not_null": True,
            "is_index": True
        }
    ],
    "run": [
        {
            "column_name": "experiment_id",
            "data_type": STR,
            "size": 32,
            "is_primary_key": False,
            "is_foreign_key": True,
            "is_not_null": True,
            "is_index": True
        },
        {
            "column_name": "run_name",
            "data_type": STR,
            "size": 100,
            "is_primary_key": False,
            "is_foreign_key": False,
            "is_not_null": False,
            "is_index": False
        },
        {
            "column_name": "run_id",
            "data_type": STR,
            "size": 32,
            "is_primary_key": True,
            "is_foreign_key": False,
            "is_not_null": True,
            "is_index": True
        },
        {
            "column_name": "triggered_time",
            "data_type": DATE,
            "size": None,
            "is_primary_key": False,
            "is_foreign_key": False,
            "is_not_null": False,
            "is_index": False
        },
        {
            "column_name": "execution_time",
            "data_type": FLOAT,
            "size": None,
            "is_primary_key": False,
            "is_foreign_key": False,
            "is_not_null": False,
            "is_index": False
        },
    ],
    "model": [
        {
            "column_name": "run_id",
            "data_type": STR,
            "size": 32,
            "is_primary_key": False,
            "is_foreign_key": True,
            "is_not_null": True,
            "is_index": True
        },
        {
            "column_name": "model_name",
            "data_type": STR,
            "size": 100,
            "is_primary_key": False,
            "is_foreign_key": False,
            "is_not_null": True,
            "is_index": True
        },
        {
            "column_name": "model_id",
            "data_type": STR,
            "size": 32,
            "is_primary_key": True,
            "is_foreign_key": False,
            "is_not_null": True,
            "is_index": True
        },
        {
            "column_name": "module_name",
            "data_type": STR,
            "size": 100,
            "is_primary_key": False,
            "is_foreign_key": False,
            "is_not_null": False,
            "is_index": False
        },
        {
            "column_name": "package_name",
            "data_type": STR,
            "size": 100,
            "is_primary_key": False,
            "is_foreign_key": False,
            "is_not_null": False,
            "is_index": False
        },
        {
            "column_name": "package_version",
            "data_type": STR,
            "size": 20,
            "is_primary_key": False,
            "is_foreign_key": False,
            "is_not_null": False,
            "is_index": False
        },
        {
            "column_name": "optimizer_id",
            "data_type": STR,
            "size": 32,
            "is_primary_key": False,
            "is_foreign_key": True,
            "is_not_null": False,
            "is_index": False
        }
    ],
    "metric": [
        {
            "column_name": "run_id",
            "data_type": STR,
            "size": 32,
            "is_primary_key": False,
            "is_foreign_key": True,
            "is_not_null": True,
            "is_index": True
        },
        {
            "column_name": "model_id",
            "data_type": STR,
            "size": 32,
            "is_primary_key": False,
            "is_foreign_key": True,
            "is_not_null": True,
            "is_index": True
        },
        {
            "column_name": "metric_name",
            "data_type": STR,
            "size": 20,
            "is_primary_key": False,
            "is_foreign_key": False,
            "is_not_null": True,
            "is_index": False
        },
        {
            "column_name": "metric_value",
            "data_type": FLOAT,
            "size": None,
            "is_primary_key": False,
            "is_foreign_key": False,
            "is_not_null": False,
            "is_index": False
        }
    ],
    "params": [
        {
            "column_name": "run_id",
            "data_type": STR,
            "size": 32,
            "is_primary_key": False,
            "is_foreign_key": True,
            "is_not_null": True,
            "is_index": True
        },
        {
            "column_name": "model_id",
            "data_type": STR,
            "size": 32,
            "is_primary_key": False,
            "is_foreign_key": True,
            "is_not_null": True,
            "is_index": True
        },
        {
            "column_name": "param_name",
            "data_type": STR,
            "size": 20,
            "is_primary_key": False,
            "is_foreign_key": False,
            "is_not_null": True,
            "is_index": False
        },
        {
            "column_name": "param_value",
            "data_type": STR,
            "size": None,
            "is_primary_key": False,
            "is_foreign_key": False,
            "is_not_null": False,
            "is_index": False
        },
        {
            "column_name": "optimizer_id",
            "data_type": STR,
            "size": 32,
            "is_primary_key": False,
            "is_foreign_key": False,
            "is_not_null": False,
            "is_index": True
        }
    ],
    "optimizer": [
        {
            "column_name": "optimizer_name",
            "data_type": STR,
            "size": 20,
            "is_primary_key": False,
            "is_foreign_key": False,
            "is_not_null": True,
            "is_index": True
        },
        {
            "column_name": "optimizer_id",
            "data_type": STR,
            "size": 32,
            "is_primary_key": True,
            "is_foreign_key": False,
            "is_not_null": True,
            "is_index": True
        },
        {
            "column_name": "module_name",
            "data_type": STR,
            "size": 20,
            "is_primary_key": False,
            "is_foreign_key": False,
            "is_not_null": False,
            "is_index": False
        }
    ]
}