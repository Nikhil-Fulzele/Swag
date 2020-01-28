from time import time
from inspect import getfullargspec
import pandas as pd
from src.utils import send_to_es


class Swag:
    # TODO: Intelligent way to detect fit and predict method and use this as a type
    # TODO: Associate relation between fit and predict
    # TODO: Introduce metric as a param of predict
    def __init__(self, experiment_name=None):
        if not experiment_name:
            raise ValueError("Experiment name is required")
        self.experiment_name = experiment_name
        self.run_info = pd.DataFrame()

    def swag(self, func):
        def wrap(*args):

            start_time = time()
            s = func(*args)
            end_time = time()
            delta_time = end_time - start_time
            print("Execution Time: {} sec".format(delta_time))

            package_name = func.__module__.split('.')[0]
            print("Package Name: {}".format(package_name))

            module_name = func.__module__
            print("Module Name: {}".format(module_name))

            model_name = func.__self__.__class__.__name__
            print("Model: {}".format(model_name))

            params = [i for i in getfullargspec(s.__init__).args[1:]]
            params_dic = {k: s.__dict__[k] for k in params}

            params_dic.update({
                "experiment_name": self.experiment_name,
                "execution_time": delta_time,
                "package_name": package_name,
                "module_name": module_name,
                "model_name": model_name
            })

            send_to_es(params_dic)

            run_info = pd.Series(params_dic)
            self.run_info = self.run_info.append(run_info, ignore_index=True)

            return s

        return wrap

    def show(self):
        print(self.run_info.T)

