import datetime
from time import time
import pandas as pd

from src.utils import send_to_es
from src.utils import get_unique_id
from src.utils import is_valid_method

from src.handlers.base_ml_handler import Experiment
from src.handlers import sklearn_handler

__MAPPER__ = {
    "sklearn": sklearn_handler
}


class Swag:
    # TODO: Introduce metric as a param of validation
    # TODO: Define schema for payload - decouple model-info, training-params and validation-metrics
    # TODO: Resource consumption
    # TODO: Test cases
    # TODO: Define random states (if not provided) for reproducibility
    # TODO: Add pre-processing, pipeline, cross_validation, metrics, model_selection
    # TODO: Explore cross_validation defaults methods
    # TODO: Add separate handlers for each packages
    # TODO: Add validator
    def __init__(self, experiment_name=None):
        if not experiment_name:
            raise ValueError("Experiment name is required")
        self.experiment = Experiment(experiment_name, get_unique_id())
        self.experiment_name = self.experiment.get_experiment_name()
        self.run_info = pd.DataFrame()

    def swag(self, func, run_name=None):
        def wrap(*args):

            method_name = func.__name__
            print("Method Name: {}".format(method_name))

            package_name = func.__module__.split('.')[0]
            print("Package Name: {}".format(package_name))

            start_time = time()
            s = func(*args)
            end_time = time()

            if not is_valid_method(package_name, method_name):
                return s

            payload_dic = __MAPPER__.get(package_name).log_run(self.experiment, run_name, func,  method_name,
                                                               package_name, start_time, end_time)

            send_to_es(payload_dic)

            run_info = pd.Series(payload_dic)
            self.run_info = self.run_info.append(run_info, ignore_index=True)
            print(payload_dic)

            return s

        return wrap

    def show(self):
        print(self.run_info.T)
