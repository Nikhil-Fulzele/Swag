from abc import abstractmethod
from time import time

from .utils import get_unique_id
from .utils import get_pandas_dataframe
from .utils.swag_exception import ArgumentMissingException
from .utils.visualization import display_experiment
from .handlers.ml_handler import Experiment
from .handlers.sklearn_handler import SklearnHandler
from .handlers.xgboost_handler import XgboostHandler

from .store.relational_store import Store


class BaseSwag:
    # TODO: Resource consumption
    # TODO: Test cases
    # TODO: Define random states (if not provided) for reproducibility
    # TODO: Add pipeline
    def __init__(self, experiment_name=None, database_engine="SQLite"):
        if not experiment_name:
            raise ValueError("Experiment name is required")
        self.db_conn = Store(database_engine) if database_engine else None
        self.experiment = Experiment(experiment_name, get_unique_id(), self.db_conn)
        self.experiment_name = self.experiment.get_experiment_name()
        self.__MAPPER__ = {
            "sklearn": SklearnHandler,
            "xgboost": XgboostHandler
        }
        self.cached_handler = dict()

    def _get_package_name(self, func):
        package_name = func.__module__.split('.')[0]
        return package_name

    def _create_or_get_handler(self, func):
        # get the package name
        package_name = self._get_package_name(func)

        # get the handler
        _handler = self.cached_handler.get(package_name)
        if not _handler or self.__MAPPER__.get(package_name):
            _handler = self.__MAPPER__.get(package_name)(self.experiment, self.db_conn)
            self.cached_handler[package_name] = _handler
        else:
            print("Handler for package {} is not present".format(package_name))
        return package_name, _handler

    def _execute_func(self, func):
        def wrap(*args, **kwargs):

            start_time = time()
            output = func(*args, **kwargs)
            end_time = time()

            return output, start_time, end_time

        return wrap

    @abstractmethod
    def fit(self, model, X, y):
        pass

    def _fit(self, func, *args, **kwargs):

        package_name, _handler = self._create_or_get_handler(func)

        output, start_time, end_time = self._execute_func(func)(*args, **kwargs)

        # log the model params
        payload_dict = _handler.log_model_fitting(None, func, package_name, start_time, end_time)

        self.swag_info = payload_dict

        return output

    def fit_predict(self, func, *args, **kwargs):
        print("""This method is not yet implemented.
        The params and metrics won't be logged""")
        return func(*args, **kwargs)

    @abstractmethod
    def evaluate(self, func, *args, **kwargs):
        pass

    def _evaluate(self, func, *args, **kwargs):
        _, _handler = self._create_or_get_handler(func)

        output, _, _ = self._execute_func(func)(*args, **kwargs)

        payload_dict = _handler.log_model_measure(func.__name__, output)
        self.swag_info = payload_dict

    def swag(self, class_instance, func, run_name):
        package_name = func.__module__.split('.')[0]

        _handler = self.cached_handler.get(package_name)
        if not _handler:
            _handler = self.__MAPPER__.get(package_name)(self.experiment, self.db_conn)
            self.cached_handler[package_name] = _handler

        _ = _handler.log_model_fitting(run_name, class_instance, package_name, 0, 0)

    def _get_info_by_run_name(self, run_name):
        result_set = self.db_conn.store.get_models_by_run_name(run_name)
        model_df = get_pandas_dataframe(result_set)

        result_set = self.db_conn.store.get_params_by_run_name(run_name)
        param_df = get_pandas_dataframe(result_set)

        result_set = self.db_conn.store.get_metrics_by_run_name(run_name)
        metric_df = get_pandas_dataframe(result_set)

        return model_df, param_df, metric_df

    def _get_info_by_run_id(self, run_id):
        result_set = self.db_conn.store.get_models_by_run_id(run_id)
        model_df = get_pandas_dataframe(result_set)

        result_set = self.db_conn.store.get_params_by_run_id(run_id)
        param_df = get_pandas_dataframe(result_set)

        result_set = self.db_conn.store.get_metrics_by_run_id(run_id)
        metric_df = get_pandas_dataframe(result_set)

        return model_df, param_df, metric_df

    def get_run_info(self, run_id=None, run_name=None):
        if not run_name and not run_id:
            raise ArgumentMissingException("Arguments cannot be Empty: Either run_id or run_name is required")

        if run_id:
            return self._get_info_by_run_id(run_id)

        return self._get_info_by_run_name(run_name)

    def get_experiment_info(self, experiment_id=None, experiment_name=None):
        if not experiment_id and not experiment_name:
            result_set = self.db_conn.store.get_all_experiment()
            return get_pandas_dataframe(result_set)

        if experiment_id:
            result_set = self.db_conn.store.get_runs_by_experiment_id(experiment_id)
            return get_pandas_dataframe(result_set)

        if experiment_name:
            result_set = self.db_conn.store.get_runs_by_experiment_name(experiment_name)
            return get_pandas_dataframe(result_set)

    def visualize_experiment(self, experiment_name=None, experiment_id=None):
        if not experiment_name and not experiment_id:
            raise Exception("Please Provide Experiment Name or Experiment ID ")

        kind_mapper_id = {
            'metrics': self.db_conn.store.get_run_metric_given_experiment_id,
            'params': self.db_conn.store.get_run_params_given_experiment_id
        }

        kind_mapper_name = {
            'metrics': self.db_conn.store.get_run_metric_given_experiment_name,
            'params': self.db_conn.store.get_run_params_given_experiment_name
        }

        for kind in ['metrics', 'params']:
            if experiment_id:
                result_set = kind_mapper_id[kind](experiment_id)
            else:
                result_set = kind_mapper_name[kind](experiment_name)

            df = get_pandas_dataframe(result_set)

            if kind == 'metrics':
                display_experiment(
                    df,
                    group_key="metric_name",
                    x_axis="run_id",
                    y_axis="metric_value",
                    title="Metric vs Runs"
                )

            if kind == 'params':
                display_experiment(
                    df,
                    group_key="param_name",
                    x_axis="run_id",
                    y_axis="param_value",
                    title="Params vs Runs"
                )
