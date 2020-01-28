import requests


BASE_URL = "localhost:8888"


class MlflowClient:
    def __init__(self):
        self.base_url = BASE_URL
        pass

    def create_experiment(self, experiment_name):
        pass

    def create_run(self, run_name):
        pass

    def track_params(self, exp_id, run_id, **kwargs):
        pass

    def track_metrics(self, exp_id, run_id, **kwargs):
        pass

    def track_model(self, exp_id, run_id, **kwargs):
        pass

    def track_execution_time(self, exp_id, run_id, delta_time):
        pass
