from abc import abstractmethod


class BaseHandler:
    def __init__(self, experiment=None, db_conn=None):
        self.experiment = experiment
        self.db_conn = db_conn

    @abstractmethod
    def log_model_fitting(self, run_name, func, package_name, start_time, end_time):
        pass

    def log_model_measure(self, metric_name, metric_value):
        """
        In current implementation, all the metrics are associated with the latest run object in experiment object
        """
        run_obj = self.experiment.get_run_at(-1)
        run_obj.add_metric(metric_name, metric_value)
        return self.experiment.get_experiment_dict()

    def log_optimizer(self, run_name, func, package_name, start_time, end_time, output):
        pass
