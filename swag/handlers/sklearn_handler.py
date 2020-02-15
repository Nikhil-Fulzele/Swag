from inspect import getfullargspec
import datetime
import sklearn
import pandas as pd

from ..utils import get_unique_id, get_run_name
from ..handlers.base_ml_handler import Run, Optimizer


def log_model_fitting(experiment, run_name, func, package_name, start_time, end_time, db_conn):

    module_name = func.__module__.split('._')[0]

    model_name = func.__self__.__class__.__name__

    package_version = sklearn.__version__

    run_id = get_unique_id()

    if not run_name:
        run_name = get_run_name(run_id)

    model_uid = get_unique_id(func)

    triggered_time = datetime.datetime.fromtimestamp(start_time / 1e3)

    execution_time = end_time - start_time

    experiment_id = experiment.get_experiment_id()

    run = Run(experiment_id, run_name, run_id, triggered_time, execution_time, db_conn)

    run.add_model(
        model_name, model_uid, module_name, package_name, package_version
    )

    _params = [i for i in getfullargspec(func.__self__.__class__).args[1:]]
    for param_name in _params:
        param_value = func.__self__.__dict__[param_name]
        run.add_param(param_name, param_value)

    experiment.add_run(run)

    return experiment.get_experiment_dict()


def log_model_measure(experiment, metric_name, metric_value):
    """
    In current implementation, all the metrics are associated with the latest run object in experiment object
    """
    run_obj = experiment.get_run_at(-1)
    run_obj.add_metric(metric_name, metric_value)
    return experiment.get_experiment_dict()


def log_optimizer(experiment, run_name, func, package_name, start_time, end_time, output, db_conn):

    optimizer_module_name = func.__module__.split('._')[0]

    optimizer_model_name = func.__self__.__class__.__name__

    optimizer_uid = get_unique_id(func)

    package_version = sklearn.__version__

    optimizer = Optimizer(optimizer_uid, optimizer_model_name, optimizer_module_name, db_conn)

    filter_params = ["estimator", "param_grid", "param_distributions"]

    _params = [i for i in getfullargspec(func.__self__.__class__).args[1:] if i not in filter_params]
    for param_name in _params:
        param_value = func.__self__.__dict__[param_name]
        optimizer.add_param(param_name, param_value)

    triggered_time = datetime.datetime.fromtimestamp(start_time / 1e3)

    execution_time = end_time - start_time

    experiment_id = experiment.get_experiment_id()

    optimizer_metrics = output.cv_results_

    df = pd.DataFrame(optimizer_metrics)
    metric_list = df.drop(df.filter(regex='param|rank').columns, axis=1).to_dict(orient='records')

    param_list = optimizer_metrics['params']

    model = func.__self__.__dict__["estimator"]

    model_params = model.__dict__

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
            run.add_param(param_name, param_value)

        for metric_name in metrics:
            metric_value = metrics[metric_name]
            run.add_metric(metric_name, metric_value)

        experiment.add_run(run)

    return experiment.get_experiment_dict()
