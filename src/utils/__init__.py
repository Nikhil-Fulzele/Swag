from src.utils.elastic_search import ElasticSearchHelper
from src.utils.mlflow_client import MlflowClient


def send_to_es(params_dic):
    es_helper = ElasticSearchHelper()
    es_helper.upload(params_dic)
