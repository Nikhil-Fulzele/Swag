from ..swag_config import VALID_METHODS


def is_valid_package(package_name):
    if VALID_METHODS.get(package_name, None):
        return True
    return False


def is_valid_entry(package_name, entry_name):
    if is_valid_package(package_name) and entry_name in VALID_METHODS[package_name]:
        return True
    return False


def get_entry_type(package_name, entry_name):
    if is_valid_entry(package_name, entry_name):
        return VALID_METHODS[package_name][entry_name]
    return None
