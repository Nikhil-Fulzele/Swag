from time import time
from inspect import getfullargspec
import pandas as pd
from src.utils import send_to_es

VALID_METHODS = ["fit", "predict", "predict_prob"]


class Swag:
    # TODO: Introduce metric as a param of validation
    # TODO: Define schema for payload - decouple model-info, training-params and validation-metrics
    def __init__(self, experiment_name=None):
        if not experiment_name:
            raise ValueError("Experiment name is required")
        self.experiment_name = experiment_name
        self.run_info = pd.DataFrame()

    def swag(self, func):
        def wrap(*args):

            method_name = func.__name__
            print("Method Name: {}".format(method_name))

            start_time = time()
            s = func(*args)
            end_time = time()

            if method_name not in VALID_METHODS:
                return s

            model_uid = "{}_{}".format(id(func.__self__), hash(func.__self__))
            print("Model: {}".format(model_uid))

            print("Triggered Time: {}".format(int(start_time)))

            delta_time = end_time - start_time
            print("Execution Time: {} sec".format(delta_time))

            package_name = func.__module__.split('.')[0]
            print("Package Name: {}".format(package_name))

            module_name = func.__module__.split('._')[0]
            print("Module Name: {}".format(module_name))

            model_name = func.__self__.__class__.__name__
            print("Model: {}".format(model_name))

            _params = [i for i in getfullargspec(func.__self__.__class__).args[1:]]
            payload_dic = {k: func.__self__.__dict__[k] for k in _params}

            payload_dic.update({
                "triggered_time": int(start_time),
                "experiment_name": self.experiment_name,
                "execution_time": delta_time,
                "method": method_name,
                "package_name": package_name,
                "module_name": module_name,
                "model_name": model_name,
                "model_uid": model_uid
            })

            send_to_es(payload_dic)

            run_info = pd.Series(payload_dic)
            self.run_info = self.run_info.append(run_info, ignore_index=True)

            return s

        return wrap

    def show(self):
        print(self.run_info.T)

