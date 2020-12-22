from uuid import uuid4
from time import time


def get_unique_id(func: any = None) -> str:
    if not func:
        return uuid4().hex
    return str(hash(func))+uuid4().hex


def get_run_name(run_id: str) -> str:
    return "RUN_{}".format(run_id)
