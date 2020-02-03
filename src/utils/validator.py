FITTER = 0
PREDICTOR = 1
MEASURE = 2
OPTIMIZER = 3


VALID_METHODS = {
    "sklearn": {
        "fit": FITTER,
        "predict": PREDICTOR,
        "predict_prob": PREDICTOR,
        "mean_squared_error": MEASURE,
        "r2_score": MEASURE,
        "mean_absolute_error": MEASURE
    }
}


def is_valid_package(package_name):
    if VALID_METHODS.get(package_name, None):
        return True
    return False


def is_valid_method(package_name, method_name):
    if is_valid_package(package_name) and method_name in VALID_METHODS[package_name]:
        return True
    return False


def get_method_type(package_name, method_name):
    if is_valid_method(package_name, method_name):
        return VALID_METHODS[package_name][method_name]
    return None

