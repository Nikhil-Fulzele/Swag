from inspect import getfullargspec
import sklearn
import pandas as pd

from ..utils import get_unique_id, get_run_name
from ..handlers.ml_handler import Run, Optimizer
from ..handlers.base_handler import BaseHandler


class SklearnHandler(BaseHandler):

    def log_model_fitting(self, run_name, func, package_name, start_time, end_time):

        module_name = func.__module__.split('._')[0]

        model_name = func.__self__.__class__.__name__

        package_version = sklearn.__version__

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

        specs = getfullargspec(func.__self__.__class__)
        for param_name, default_value in zip(specs.args[1:], specs.defaults):
            param_value = func.__self__.__dict__[param_name]
            default_flag = default_value != param_value
            run.add_param(param_name, param_value, default_flag)

        self.experiment.add_run(run)

        return self.experiment.get_experiment_dict()

    def log_model_measure(self, metric_name, metric_value):
        """
        In current implementation, all the metrics are associated with the latest run object in experiment object
        """
        run_obj = self.experiment.get_run_at(-1)
        run_obj.add_metric(metric_name, metric_value)
        return self.experiment.get_experiment_dict()

    def log_optimizer(self, run_name, func, package_name, start_time, end_time, output):

        optimizer_module_name = func.__module__.split('._')[0]

        optimizer_model_name = func.__self__.__class__.__name__

        optimizer_uid = get_unique_id(func)

        package_version = sklearn.__version__

        optimizer = Optimizer(optimizer_uid, optimizer_model_name, optimizer_module_name, self.db_conn)

        filter_params = ["estimator", "param_grid", "param_distributions"]

        spec = getfullargspec(func.__self__.__class__)
        for param_name, default_value in zip(spec.args[1:], spec.defaults):
            if param_name in filter_params:
                continue
            param_value = func.__self__.__dict__[param_name]
            default_flag = default_value != param_value
            optimizer.add_param(param_name, param_value, default_flag)

        triggered_time = start_time

        execution_time = end_time - start_time

        experiment_id = self.experiment.get_experiment_id()

        optimizer_metrics = output.cv_results_

        best_index = output.best_index_  # use this to move the metrics and param as the last run entry in the exp

        df = pd.DataFrame(optimizer_metrics)
        metric_list = df.drop(df.filter(regex='param|rank').columns, axis=1).to_dict(orient='records')
        metric_list.append(metric_list.pop(best_index))  # moving the best metric to last position

        param_list = optimizer_metrics['params']
        param_list.append(param_list.pop(best_index))  # moving the best params to the last position

        model = func.__self__.__dict__["estimator"]

        spec = getfullargspec(model.__class__)

        model_params = {
            k: model.__dict__[k] for k in spec.args[1:]
        }
        for rm_params in param_list[-1].keys():
            model_params.pop(rm_params)

        model_name = model.__class__.__name__
        module_name = model.__module__.split('._')[0]

        for idx, (params, metrics) in enumerate(zip(param_list, metric_list)):

            model_uid = get_unique_id(func) + "_{}".format(idx)

            run_id = get_unique_id()

            if not run_name:
                run_name = get_run_name(run_id)

            run = Run(experiment_id, run_name, run_id, triggered_time, execution_time, db_conn)
            run.add_model(
                model_name, model_uid, module_name, package_name, package_version, optimizer
            )

            params.update(model_params)

            for param_name in params:
                param_value = params[param_name]
                default_flag = param_name not in model_params
                run.add_param(param_name, param_value, default_flag)

            for metric_name in metrics:
                metric_value = metrics[metric_name]
                run.add_metric(metric_name, metric_value)

            self.experiment.add_run(run)

        return self.experiment.get_experiment_dict()
