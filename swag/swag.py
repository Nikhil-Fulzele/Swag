from time import time
from pprint import pprint

from .utils import send_to_es
from .utils import get_unique_id
from .utils import is_valid_entry, get_entry_type
from .utils import FITTER, MEASURE, OPTIMIZER

from .handlers.base_ml_handler import Experiment
from .handlers import sklearn_handler

__MAPPER__ = {
    "sklearn": sklearn_handler
}


class Swag:
    # TODO: Resource consumption
    # TODO: Test cases
    # TODO: Define random states (if not provided) for reproducibility
    # TODO: Add pre-processing, pipeline, cross_validation, metrics, model_selection
    # TODO: Explore cross_validation defaults methods
    def __init__(self, experiment_name=None):
        if not experiment_name:
            raise ValueError("Experiment name is required")
        self.experiment = Experiment(experiment_name, get_unique_id())
        self.experiment_name = self.experiment.get_experiment_name()
        self.swag_info = None

    def swag(self, func, run_name=None):
        def wrap(*args):

            method_name = func.__name__

            package_name = func.__module__.split('.')[0]

            start_time = time()
            output = func(*args)
            end_time = time()

            if not is_valid_entry(package_name, method_name):
                return output

            method_type = get_entry_type(package_name, method_name)

            if method_type == FITTER:
                model_name = func.__self__.__class__.__name__
                class_type = get_entry_type(package_name, model_name)
                if class_type == OPTIMIZER:
                    payload_dict = __MAPPER__.get(package_name).log_optimizer(self.experiment, run_name, func,
                                                                              package_name,
                                                                              start_time, end_time, output)
                else:
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
