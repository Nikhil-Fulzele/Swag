from time import time
from pprint import pprint

from .utils import send_to_es
from .utils import get_unique_id
from .utils import is_valid_entry, get_entry_type
from .utils import FITTER, MEASURE, OPTIMIZER
from .utils import get_pandas_dataframe
from .utils.visualization import display_experiment
from .handlers.ml_handler import Experiment
from .handlers.sklearn_handler import SklearnHandler
from .handlers.xgboost_handler import XgboostHandler

from .store.relational_store import Store


class Swag:
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
        self.swag_info = None   # TODO: deprecate this variable
        self.__MAPPER__ = {
            "sklearn": SklearnHandler,
            "xgboost": XgboostHandler
        }
        self.cached_handler = dict()

    def swag(self, func, run_name=None):
        def wrap(*args):
            method_name = func.__name__

            package_name = func.__module__.split('.')[0]

            _handler = self.cached_handler.get(package_name)
            if not _handler:
                _handler = self.__MAPPER__.get(package_name)(self.experiment, self.db_conn)
                self.cached_handler[package_name] = _handler

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
                    payload_dict = _handler.log_optimizer(run_name, func, package_name, start_time, end_time, output)
                else:
                    payload_dict = _handler.log_model_fitting(run_name, func, package_name, start_time, end_time)
                self.swag_info = payload_dict

            if method_type == MEASURE:
                payload_dict = _handler.log_model_measure(method_name, output)
                self.swag_info = payload_dict

            return output

        return wrap

    def load(self):
        # TODO: deprecate this method
        send_to_es(self.swag_info)

    def get_json(self):
        # TODO: deprecate this method
        return self.swag_info

    def get_swag_dataframe(self, experiment_id=None, experiment_name=None, run_id=None, run_name=None):
        # TODO: change the definition
        if not experiment_id and not experiment_name and not run_id and not run_name:
            result_set = self.db_conn.store.get_all_experiment()
            return get_pandas_dataframe(result_set)

        if experiment_id:
            result_set = self.db_conn.store.get_runs_by_experiment_id(experiment_id)
            return get_pandas_dataframe(result_set)

        if experiment_name:
            result_set = self.db_conn.store.get_runs_by_experiment_name(experiment_name)
            return get_pandas_dataframe(result_set)

        if run_id:
            result_set = self.db_conn.store.get_models_by_run_id(run_id)
            model_df = get_pandas_dataframe(result_set)

            result_set = self.db_conn.store.get_params_by_run_id(run_id)
            param_df = get_pandas_dataframe(result_set)

            result_set = self.db_conn.store.get_metrics_by_run_id(run_id)
            metric_df = get_pandas_dataframe(result_set)

            return model_df, param_df, metric_df

        if run_name:
            result_set = self.db_conn.store.get_models_by_run_name(run_name)
            model_df = get_pandas_dataframe(result_set)

            result_set = self.db_conn.store.get_params_by_run_name(run_name)
            param_df = get_pandas_dataframe(result_set)

            result_set = self.db_conn.store.get_metrics_by_run_name(run_name)
            metric_df = get_pandas_dataframe(result_set)

            return model_df, param_df, metric_df

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
