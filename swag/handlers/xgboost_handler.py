import inspect
from inspect import getfullargspec
import xgboost

from ..utils import get_unique_id, get_run_name
from ..handlers.ml_handler import Run
from ..handlers.base_handler import BaseHandler


class XgboostHandler(BaseHandler):

    def log_model_fitting(self, run_name, func, package_name, start_time, end_time):

        module_name = func.__module__.split('.')[0]

        model_name = func.__self__.__class__.__name__

        package_version = xgboost.__version__

        run_id = get_unique_id()

        if not run_name:
            run_name = get_run_name(run_id)

        model_uid = get_unique_id(func)

        triggered_time = start_time

        execution_time = end_time - start_time

        experiment_id = self.experiment.get_experiment_id()

        run = Run(experiment_id, run_name, run_id, triggered_time, execution_time, self.db_conn)

        run.add_model(
            model_name, model_uid, module_name, package_name, package_version
        )

        set_params_dict = func.__self__.__dict__
        default_param_dict = dict()
        for _cls in inspect.getmro(func.__self__.__class__):
            specs = getfullargspec(_cls)
            if _cls.__name__ == 'BaseEstimator':
                break
            for param_name, default_value in zip(specs.args[1:], specs.defaults):
                if param_name in default_param_dict:
                    continue
                default_param_dict[param_name] = default_value

        for param_name, default_value in default_param_dict.items():
            param_value = set_params_dict[param_name]
            if param_name == 'missing':
                param_value = None
            default_flag = default_value != param_value
            run.add_param(param_name, param_value, default_flag)

        self.experiment.add_run(run)

        return self.experiment.get_experiment_dict()





