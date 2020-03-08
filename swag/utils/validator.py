FITTER = 0
PREDICTOR = 1
MEASURE = 2
MODEL = 3
OPTIMIZER = 4

VALID_METHODS = {
    "sklearn": {
        "fit": FITTER,
        "predict": PREDICTOR,
        "predict_prob": PREDICTOR,
        "mean_squared_error": MEASURE,
        "r2_score": MEASURE,
        "mean_absolute_error": MEASURE,
        "GridSearchCV": OPTIMIZER,
        "RandomizedSearchCV": OPTIMIZER
    },
    "xgboost": {
        "fit": FITTER,
        "predict": PREDICTOR,
    }
}


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
