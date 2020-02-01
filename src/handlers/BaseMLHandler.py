from collections import OrderedDict

from src.utils.unique_id_generator import  get_unique_id


class ModelMeta:
    def __init__(self, model_name: str, model_id: str, module_name: str, package_name: str,
                 package_version: str) -> None:
        """

        :param model_name: Name of the model, e.g. RandomForestClassifier, MLPRegressor, etc...
        :param model_id: Unique ID of the model, generated using utils.model_id_generator
        :param module_name: Name of the module, eg. sklearn.neural_network, sklearn.svm, etc...
        :param package_name: Name of the package, e.g. sklearn, keras, etc...
        :param package_version: Package version, 0.22, 2.0, etc...
        """
        self.model_name = model_name
        self.model_id = model_id
        self.module_name = module_name
        self.package_name = package_name
        self.package_version = package_version

    def get_model_name(self) -> str:
        """

        :return: Model name
        """
        return self.model_name

    def get_model_id(self) -> str:
        """

        :return: Model ID
        """
        return self.model_id

    def get_module_name(self) -> str:
        """

        :return: Module name
        """
        return self.module_name

    def get_package_name(self) -> str:
        """

        :return: Package name
        """
        return self.package_name

    def get_package_version(self) -> str:
        """

        :return: Package version
        """
        return self.package_version

    def get_model_meta_dict(self) -> dict:
        """

        :return: Dictionary of Model meta info
        """
        return {
            "model_name": self.get_model_name(),
            "model_id": self.get_model_id(),
            "module_name": self.get_module_name(),
            "package_name": self.get_package_name(),
            "package_version": self.get_package_version()
        }

    def get_model_meta_tuple(self) -> tuple:
        """

        :return: Tuple of Model meta info in the order
        (
            Model Name,
            Model ID,
            Module Name,
            Package Name,
            Package Version
        )
        """
        return (
            self.get_model_name(),
            self.get_model_id(),
            self.get_module_name(),
            self.get_package_name(),
            self.get_package_version()
        )


class Param:
    def __init__(self, model_id: str, param_name: str, param_value: any) -> None:
        """

        :param model_id: Unique ID of the model, generated using utils.model_id_generator
        :param param_name: Name of the parameter, e.g. random_state, kernel, n_jobs
        :param param_value: Value of this parameter, e.g. 10, rbf, -1
        """
        self.model_id = model_id
        self.param_name = param_name
        self.param_value = param_value

    def get_model_id(self) -> str:
        """

        :return: Model ID
        """
        return self.model_id

    def get_param_name(self) -> str:
        """

        :return: Parameter Name
        """
        return self.param_name

    def get_param_value(self) -> any:
        """

        :return: Parameter Value
        """
        return self.param_value

    def get_param_dict(self) -> dict:
        """

        :return: Dictionary of Param info
        """
        return {
            "model_id": self.get_model_id(),
            "param_name": self.get_param_name(),
            "param_value": self.get_param_value()
        }

    def get_param_tuple(self) -> tuple:
        """

        :return: Tuple of Param info in the order
        (
            Model ID,
            Param Name,
            Param Value
        )
        """
        return (
            self.get_model_id(),
            self.get_param_name(),
            self.get_param_value()
        )


class Metrics:
    def __init__(self, model_id: str, metric_name: str, metric_value: float):
        """

        :param model_id: Unique ID of the model, generated using utils.model_id_generator
        :param metric_name: Name of the metric, e.g. AUC, Accuracy, F1-Score
        :param metric_value: Value of this metric, e.g. 0.1, 90, 0.98
        """
        self.model_id = model_id
        self.metric_name = metric_name
        self.metric_value = metric_value

    def get_model_id(self) -> str:
        """

        :return: Model ID
        """
        return self.model_id

    def get_metric_name(self) -> str:
        """

        :return: Metric Name
        """
        return self.metric_name

    def get_metric_value(self) -> float:
        """

        :return: Metric Value
        """
        return self.metric_value

    def get_metric_dict(self) -> dict:
        """

        :return: Dictionary of Metric info
        """
        return {
            "model_id": self.get_model_id(),
            "metric_name": self.get_metric_name(),
            "metric_value": self.get_metric_value()
        }

    def get_metric_tuple(self) -> tuple:
        """

        :return: Tuple of Metric info in order
        (
            Model ID,
            Metric Name,
            Metric Value
        )
        """
        return (
            self.get_model_id(),
            self.get_metric_name(),
            self.get_metric_value()
        )


class ExperimentInfo:
    def __init__(self, experiment_name: str, experiment_id: str) -> None:
        self.experiment_name = experiment_name
        self.experiment_id = experiment_id

    def get_experiment_name(self) -> str:
        return self.experiment_name

    def get_experiment_id(self) -> str:
        return self.experiment_id

    def get_experiment_info_dict(self) -> dict:
        return {
            "experiment_name": self.experiment_name,
            "experiment_id": self.experiment_id
        }

    def get_experiment_info_tuple(self) -> tuple:
        return (
            self.experiment_name,
            self.experiment_id
        )


class RunInfo:
    def __init__(self, run_name: str, run_id: str, triggered_time: int, execution_time: float) -> None:
        self.run_name = run_name
        self.run_id = run_id
        self.triggered_time = triggered_time
        self.execution_time = execution_time

    def get_run_name(self) -> str:
        return self.run_name

    def get_run_id(self) -> str:
        return self.run_id

    def get_triggered_time(self) -> int:
        return self.triggered_time

    def get_execution_time(self) -> float:
        return self.execution_time

    def get_run_info_dict(self) -> dict:
        return {
            "run_name": self.run_name,
            "run_id": self.run_id,
            "triggered_time": self.triggered_time,
            "execution_time": self.execution_time
        }

    def get_run_info_tuple(self) -> tuple:
        return (
            self.run_name,
            self.run_id,
            self.triggered_time,
            self.execution_time
        )


class Run(RunInfo):
    __model = None
    __param = OrderedDict()
    __metric = OrderedDict()

    def add_model(self, model_name: str, model_id: str, module_name: str, package_name: str,
                  package_version: str) -> None:
        self.__model = ModelMeta(model_name, model_id, module_name, package_name, package_version)

    def get_model(self) -> ModelMeta:
        return self.__model

    def add_param(self, param_name: str, param_value: any) -> None:
        param = Param(self.__model.get_model_id(), param_name, param_value)
        self.__param[param_name] = param

    def get_param(self, param_name: str) -> Param:
        return self.__param[param_name]

    def add_metric(self, metric_name: str, metric_value: float) -> None:
        metric = Metrics(self.__model.get_model_id(), metric_name, metric_value)
        self.__metric[metric_name] = metric

    def get_metric(self, metric_name: str) -> Metrics:
        return self.__metric[metric_name]

    def get_run_dict(self) -> dict:
        run_info = self.get_run_info_dict()
        model_info = self.get_model().get_model_meta_dict()

        param_info = [self.get_param(i).get_param_dict() for i in self.__param]
        metric_info = [self.get_metric(i).get_metric_dict() for i in self.__metric]

        return {
            "run_info": run_info,
            "model_info": model_info,
            "param_info": param_info,
            "metric_info": metric_info
        }

    def get_run_tuple(self) -> tuple:
        run_info = self.get_run_info_tuple()
        model_info = self.get_model().get_model_meta_tuple()

        param_info = (self.get_param(i).get_param_tuple() for i in self.__param)
        metric_info = (self.get_metric(i).get_metric_tuple() for i in self.__metric)

        return (
            run_info, model_info, param_info, metric_info
        )


class Experiment(ExperimentInfo):
    __run = OrderedDict()
    __mapper = {}

    def add_run(self, run_name: str, run_id: str, run_object: Run) -> None:
        __key = get_unique_id
        self.__mapper[run_name] = self.__mapper[run_id] = __key
        self.__run[__key] = run_object

    def get_run_by_name(self, run_name: str) -> dict:
        run_obj = self.__run.get(self.__mapper.get(run_name, None), None)
        if run_obj:
            return run_obj.get_run_dict()

    def get_run_by_id(self, run_id: str) -> dict:
        run_obj = self.__run.get(self.__mapper.get(run_id, None), None)
        if run_obj:
            return run_obj.get_run_dict()

    def get_experiment_dict(self) -> dict:
        experiment_info = self.get_experiment_info_dict()

        runs_info = [self.__run[i].get_run_dict() for i in self.__run]

        return {
            "experiment_info": experiment_info,
            "runs_info": runs_info
        }

    def get_experiment_tuple(self) -> tuple:
        experiment_info = self.get_experiment_info_tuple()

        runs_info = (self.__run[i].get_run_tuple() for i in self.__run)

        return (
            experiment_info,
            runs_info
        )
