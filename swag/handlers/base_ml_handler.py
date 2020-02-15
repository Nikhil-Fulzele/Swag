from collections import OrderedDict
from datetime import datetime
from ..utils import remove_ids
from ..store.relational_store import Store


class Param:
    def __init__(self, run_id: str, model_id: str, param_name: str, param_value: any, optimizer_id: str = None,
                 db_conn: Store = None) -> None:
        """

        :param run_id: Run ID for this params
        :param model_id: Unique ID of the model, generated using utils.model_id_generator
        :param param_name: Name of the parameter, e.g. random_state, kernel, n_jobs
        :param param_value: Value of this parameter, e.g. 10, rbf, -1
        """
        self.run_id = run_id
        self.model_id = model_id
        self.param_name = param_name
        self.param_value = param_value
        self.db_conn = db_conn
        self.optimizer_id = optimizer_id

    def get_run_id(self) -> str:
        """

        :return: Run ID for this params
        """
        return self.run_id

    def get_model_id(self) -> str:
        """

        :return: Model ID
        """
        return self.model_id

    def get_optimizer_id(self) -> str:
        return self.optimizer_id

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
            "run_id": self.get_run_id(),
            "model_id": self.get_model_id(),
            "param_name": self.get_param_name(),
            "param_value": self.get_param_value(),
            "optimizer_id": self.get_optimizer_id()
        }

    def get_param_tuple(self) -> tuple:
        """

        :return: Tuple of Param info in the order
        (
            Run ID,
            Model ID,
            Param Name,
            Param Value,
            Optimizer ID
        )
        """
        return (
            self.get_run_id(),
            self.get_model_id(),
            self.get_param_name(),
            self.get_param_value(),
            self.get_optimizer_id()
        )

    def load_into_db(self) -> None:
        if not self.db_conn:
            self.db_conn.insert_into_db(
                "params",
                run_id=self.get_run_id(),
                model_id=self.get_model_id(),
                param_name=self.get_param_name(),
                param_value=self.get_param_value(),
                optimizer_id=self.get_optimizer_id()
            )


class Metrics:
    def __init__(self, run_id: str, model_id: str, metric_name: str, metric_value: float,
                 db_conn: Store = None) -> None:
        """

        :param run_id: Run ID for this metrics
        :param model_id: Unique ID of the model, generated using utils.model_id_generator
        :param metric_name: Name of the metric, e.g. AUC, Accuracy, F1-Score
        :param metric_value: Value of this metric, e.g. 0.1, 90, 0.98
        """
        self.run_id = run_id
        self.model_id = model_id
        self.metric_name = metric_name
        self.metric_value = metric_value
        self.db_conn = db_conn

    def get_run_id(self) -> str:
        """

        :return: Run ID for this metrics
        """
        return self.run_id

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
            "run_id": self.get_run_id(),
            "model_id": self.get_model_id(),
            "metric_name": self.get_metric_name(),
            "metric_value": self.get_metric_value()
        }

    def get_metric_tuple(self) -> tuple:
        """

        :return: Tuple of Metric info in order
        (
            Run ID,
            Model ID,
            Metric Name,
            Metric Value
        )
        """
        return (
            self.get_run_id(),
            self.get_model_id(),
            self.get_metric_name(),
            self.get_metric_value()
        )

    def load_into_db(self) -> None:
        if self.db_conn:
            self.db_conn.insert_into_db(
                "metric",
                run_id=self.get_run_id(),
                model_id=self.get_model_id(),
                metric_name=self.get_metric_name(),
                metric_value=self.get_metric_value()
            )


class OptimizerInfo:
    def __init__(self, model_id: str, optimizer_id: str, optimizer_name: str, module_name: str,
                 db_conn: Store = None) -> None:
        """

        :param optimizer_name: Name of the optimizer
        :param module_name: Name of the module e.g. sklearn.model_selection
        """
        self.model_id = model_id
        self.optimizer_id = optimizer_id
        self.optimizer_name = optimizer_name
        self.module_name = module_name
        self.db_conn = db_conn

    def get_model_id(self) -> str:
        return self.model_id

    def get_optimizer_id(self) -> str:
        return self.optimizer_id

    def get_optimizer_name(self) -> str:
        """

        :return: Optimizer name
        """
        return self.optimizer_name

    def get_module_name(self) -> str:
        """

        :return: Module name
        """
        return self.module_name

    def get_optimizer_info_dict(self) -> dict:
        """

        :return: Dictionary of Optimizer Info
        """
        return {
            "optimizer_name": self.get_optimizer_name(),
            "module_name": self.get_module_name()
        }

    def get_optimizer_info_tuple(self) -> tuple:
        """

        :return: Tuple of Optimizer Info in order
            Optimizer Name,
            Module name
        """
        return (
            self.get_optimizer_name(),
            self.get_module_name()
        )

    def load_into_db(self) -> None:
        if self.db_conn:
            self.db_conn.insert_into_db(
                "optimizer",
                model_id=self.get_model_id(),
                module_name=self.get_module_name(),
                optimizer_name=self.get_optimizer_name(),
                optimizer_id=self.get_optimizer_id()
            )


class Optimizer(OptimizerInfo):
    __param = OrderedDict()

    def add_param(self, param_name: str, param_value: any) -> None:
        param = Param("", "", param_name, str(param_value))
        self.__param[param_name] = param

    def get_param(self, param_name: str) -> Param:
        return self.__param[param_name]

    def get_optimizer_dict(self) -> dict:
        optimizer_info = self.get_optimizer_info_dict()

        param_info = [
            remove_ids(self.get_param(i).get_param_dict(), ["model_id", "run_id"])
            for i in self.__param
        ]

        return {
            "optimizer": optimizer_info,
            "param_info": param_info
        }

    def get_optimizer_tuple(self) -> tuple:
        optimizer_info = self.get_optimizer_info_tuple()

        param_info = (
            self.get_param(i).get_param_tuple()
            for i in self.__param
        )

        return (
            optimizer_info,
            param_info
        )


class ModelMeta:
    def __init__(self, run_id: str, model_name: str, model_id: str, module_name: str, package_name: str,
                 package_version: str, optimizer: [Optimizer, None] = None, db_conn: Store = None) -> None:
        """

        :param run_id: Run ID of this model
        :param model_name: Name of the model, e.g. RandomForestClassifier, MLPRegressor, etc...
        :param model_id: Unique ID of the model, generated using utils.model_id_generator
        :param module_name: Name of the module, eg. sklearn.neural_network, sklearn.svm, etc...
        :param package_name: Name of the package, e.g. sklearn, keras, etc...
        :param package_version: Package version, 0.22, 2.0, etc...
        """
        self.run_id = run_id
        self.model_name = model_name
        self.model_id = model_id
        self.module_name = module_name
        self.package_name = package_name
        self.package_version = package_version
        self.optimizer = optimizer
        self.db_conn = db_conn

    def get_run_id(self) -> str:
        """

        :return: Model's run id
        """
        return self.run_id

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

    def get_optimizer(self) -> [Optimizer, None]:
        """

        :return: Optimizer used
        """
        return self.optimizer

    def get_model_meta_dict(self) -> dict:
        """

        :return: Dictionary of Model meta info
        """
        optimizer_obj = self.get_optimizer()
        optimizer = optimizer_obj.get_optimizer_dict() if optimizer_obj else None
        return {
            "run_id": self.get_run_id(),
            "model_name": self.get_model_name(),
            "model_id": self.get_model_id(),
            "module_name": self.get_module_name(),
            "package_name": self.get_package_name(),
            "package_version": self.get_package_version(),
            "optimizer": optimizer
        }

    def get_model_meta_tuple(self) -> tuple:
        """

        :return: Tuple of Model meta info in the order
        (
            RUN ID,
            Model Name,
            Model ID,
            Module Name,
            Package Name,
            Package Version,
            Optimizer
        )
        """
        optimizer_obj = self.get_optimizer()
        optimizer = optimizer_obj.get_optimizer_tuple() if optimizer_obj else None
        return (
            self.get_run_id(),
            self.get_model_name(),
            self.get_model_id(),
            self.get_module_name(),
            self.get_package_name(),
            self.get_package_version(),
            optimizer
        )

    def load_into_db(self) -> None:
        if self.db_conn:
            self.db_conn.insert_into_db(
                "model",
                run_id=self.get_run_id(),
                model_name=self.get_model_name(),
                model_id=self.get_model_id(),
                module_name=self.get_module_name(),
                package_name=self.get_package_name(),
                package_version=self.get_package_version()
            )


class ExperimentInfo:
    def __init__(self, experiment_name: str, experiment_id: str, db_conn: Store = None) -> None:
        self.experiment_name = experiment_name
        self.experiment_id = experiment_id
        self.db_conn = db_conn

    def get_experiment_name(self) -> str:
        return self.experiment_name

    def get_experiment_id(self) -> str:
        return self.experiment_id

    def get_experiment_info_dict(self) -> dict:
        return {
            "experiment_name": self.get_experiment_name(),
            "experiment_id": self.get_experiment_id()
        }

    def get_experiment_info_tuple(self) -> tuple:
        return (
            self.get_experiment_name(),
            self.get_experiment_id()
        )

    def load_into_db(self) -> None:
        if self.db_conn:
            self.db_conn.insert_into_db(
                "experiment",
                experiment_id=self.get_experiment_id(),
                experiment_name=self.get_experiment_name()
            )


class RunInfo:
    def __init__(self, experiment_id: str, run_name: str, run_id: str, triggered_time: datetime,
                 execution_time: float, db_conn: Store = None) -> None:
        self.experiment_id = experiment_id
        self.run_name = run_name
        self.run_id = run_id
        self.triggered_time = triggered_time
        self.execution_time = execution_time
        self.db_conn = db_conn

    def get_experiment_id(self) -> str:
        return self.experiment_id

    def get_run_name(self) -> str:
        return self.run_name

    def get_run_id(self) -> str:
        return self.run_id

    def get_triggered_time(self) -> datetime:
        return self.triggered_time

    def get_execution_time(self) -> float:
        return self.execution_time

    def get_run_info_dict(self) -> dict:
        return {
            "experiment_id": self.get_experiment_id(),
            "run_name": self.get_run_name(),
            "run_id": self.get_run_id(),
            "triggered_time": self.get_triggered_time(),
            "execution_time": self.get_execution_time()
        }

    def get_run_info_tuple(self) -> tuple:
        return (
            self.get_experiment_id(),
            self.get_run_name(),
            self.get_run_id(),
            self.get_triggered_time(),
            self.get_execution_time()
        )

    def load_into_db(self) -> None:
        if self.db_conn:
            self.db_conn.insert_into_db(
                "run",
                experiment_id=self.get_experiment_id(),
                run_name=self.get_run_name(),
                run_id=self.get_run_id(),
                triggered_time=self.get_triggered_time(),
                execution_time=self.get_execution_time()
            )


class Run(RunInfo):
    __model = None
    __param = OrderedDict()
    __metric = OrderedDict()

    def add_model(self, model_name: str, model_id: str, module_name: str, package_name: str,
                  package_version: str, optimizer: [str, None] = None) -> None:
        self.__model = ModelMeta(self.get_run_id(), model_name, model_id, module_name, package_name,
                                 package_version, optimizer)

    def get_model(self) -> ModelMeta:
        return self.__model

    def add_param(self, param_name: str, param_value: any) -> None:
        param = Param(self.get_run_id(), self.__model.get_model_id(), param_name, str(param_value))
        self.__param[param_name] = param

    def get_param(self, param_name: str) -> Param:
        return self.__param[param_name]

    def add_metric(self, metric_name: str, metric_value: float) -> None:
        metric = Metrics(self.get_run_id(), self.__model.get_model_id(), metric_name, metric_value)
        self.__metric[metric_name] = metric

    def get_metric(self, metric_name: str) -> Metrics:
        return self.__metric[metric_name]

    def get_run_dict(self) -> dict:

        run_info = remove_ids(self.get_run_info_dict(), ["experiment_id"])
        model_info = remove_ids(self.get_model().get_model_meta_dict(), ["run_id"])

        param_info = [
            remove_ids(self.get_param(i).get_param_dict(), ["model_id", "run_id"])
            for i in self.__param
        ]
        metric_info = [
            remove_ids(self.get_metric(i).get_metric_dict(), ["model_id", "run_id"])
            for i in self.__metric
        ]

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
            run_info,
            model_info,
            param_info,
            metric_info
        )


class Experiment(ExperimentInfo):
    __run = list()

    def add_run(self, run_object: Run) -> None:
        self.__run.append(run_object)

    def get_all_run(self) -> list:
        return self.__run

    def get_run_at(self, k) -> Run:
        return self.__run[k]

    def get_experiment_dict(self) -> dict:
        experiment_info = self.get_experiment_info_dict()

        runs_info = [i.get_run_dict() for i in self.__run]

        return {
            "experiment_info": experiment_info,
            "runs_info": runs_info
        }

    def get_experiment_tuple(self) -> tuple:
        experiment_info = self.get_experiment_info_tuple()

        runs_info = (i.get_run_tuple() for i in self.__run)

        return (
                experiment_info,
                runs_info
        )
