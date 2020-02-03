from inspect import getfullargspec
import datetime
import sklearn

from src.utils import get_unique_id, get_run_name
from src.handlers.base_ml_handler import Run


def log_model_fitting(experiment, run_name, func, package_name, start_time, end_time):

    run_id = get_unique_id()

    if not run_name:
        run_name = get_run_name(run_id)

    model_uid = get_unique_id(func)

    triggered_time = datetime.datetime.fromtimestamp(start_time / 1e3)

    execution_time = end_time - start_time

    module_name = func.__module__.split('._')[0]
    print("Module Name: {}".format(module_name))

    model_name = func.__self__.__class__.__name__
    print("Model Name: {}".format(model_name))

    package_version = sklearn.__version__
    print("Package Version: {}".format(package_name))

    experiment_id = experiment.get_experiment_id()

    run = Run(experiment_id, run_name, run_id, triggered_time, execution_time)
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
    run_obj = experiment.get_run_at(-1)
    run_obj.add_metric(metric_name, metric_value)
    return experiment.get_experiment_dict()
