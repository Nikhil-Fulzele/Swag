from src.store.elastic_search import *
from src.utils.unique_id_generator import *
from src.utils.validator import *


def send_to_es(params_dic):
    es_helper = ElasticSearchHelper()
    es_helper.upload(params_dic)


def remove_ids(dict_obj, filter_list):
    for key in filter_list:
        if dict_obj.get(key, None):
            dict_obj.pop(key)
    return dict_obj
