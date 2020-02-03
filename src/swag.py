from time import time
from pprint import pprint

from src.utils import send_to_es
from src.utils import get_unique_id
from src.utils import is_valid_method, get_method_type
from src.utils import FITTER, MEASURE

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
        self.swag_info = None

    def swag(self, func, run_name=None):
        def wrap(*args):

            method_name = func.__name__
            print("Method Name: {}".format(method_name))

            package_name = func.__module__.split('.')[0]
            print("Package Name: {}".format(package_name))

            start_time = time()
            output = func(*args)
            end_time = time()

            if not is_valid_method(package_name, method_name):
                return output

            method_type = get_method_type(package_name, method_name)
            if method_type == FITTER:

                payload_dict = __MAPPER__.get(package_name).log_model_fitting(self.experiment, run_name, func,
                                                                              package_name, start_time, end_time)
                self.swag_info = payload_dict

            if method_type == MEASURE:

                payload_dict = __MAPPER__.get(package_name).log_model_measure(self.experiment, method_name,
                                                                              output)
                self.swag_info = payload_dict

            return output

        return wrap

    def load(self):
        send_to_es(self.swag_info)

    def show(self):
        pprint(self.swag_info)

    def get_exp(self):
        return self.swag_info
