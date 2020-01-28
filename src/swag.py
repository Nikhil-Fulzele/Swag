from time import time
from inspect import getfullargspec
from inspect import getmembers
import pandas as pd


class Swag:
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
            print("Model: {}".format(func.__self__))
            params = [i for i in getfullargspec(s.__init__).args[1:]]
            params_dic = {k: s.__dict__[k] for k in params}
            params_dic.update({"execution_time": delta_time})

            run_info = pd.Series(params_dic)
            self.run_info = self.run_info.append(run_info, ignore_index=True)

            return s

        return wrap

    def show(self):
        print(self.run_info.T)
