
VALID_METHODS = {
    "sklearn": ["fit", "predict", "predict_prob"]
}


def is_valid_package(package_name):
    if not VALID_METHODS.get(package_name, None):
        return True
    return False


def is_valid_method(package_name, method_name):
    if is_valid_package(package_name) and method_name in VALID_METHODS[package_name]:
        return True
    return False
