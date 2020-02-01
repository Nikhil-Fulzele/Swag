from uuid import uuid4


def get_unique_id(func: any = None) -> str:
    if not func:
        return uuid4().hex
    return str(hash(func.__self__))
