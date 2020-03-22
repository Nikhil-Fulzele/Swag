from abc import abstractmethod


class BaseHandler:
    def __init__(self, experiment=None, db_conn=None):
        self.experiment = experiment
        self.db_conn = db_conn

    @abstractmethod
    def log_model_fitting(self, run_name, func, package_name, start_time, end_time):
        pass

    @abstractmethod
    def log_model_measure(self, metric_name, metric_value):
        pass

    def log_optimizer(self, run_name, func, package_name, start_time, end_time, output):
        pass
