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

DATABASE = {
    "SQLite": {
        "PATH": "/tmp"
    }
}
