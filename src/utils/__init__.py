from src.utils.elastic_search import *
from src.utils.mlflow_client import *
from src.utils.unique_id_generator import *
from src.utils.validator import *


def send_to_es(params_dic):
    es_helper = ElasticSearchHelper()
    es_helper.upload(params_dic)
