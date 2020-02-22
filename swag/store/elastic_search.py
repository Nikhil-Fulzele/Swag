# https://elk-docker.readthedocs.io
import os
from elasticsearch import Elasticsearch

ES_URL = os.getenv("ES_URL", "127.0.0.1")
ES_PORT = os.getenv("ES_PORT", 9200)
ES_END_POINT = ":".join([ES_URL, str(ES_PORT)])
ES_INDEX = os.getenv("ES_INDEX", "swagger_test")


class ElasticSearchHelper:
    # TODO: Make the class singleton
    # TODO: Add getter
    # TODO: deprecate this class
    es_conn = Elasticsearch(ES_END_POINT)

    def _create_index(self):
        if not self.es_conn.indices.exists(index=ES_INDEX):
            self.es_conn.indices.create(index=ES_INDEX, ignore=400)

    def upload(self, data):
        self._create_index()
        return self.es_conn.index(index=ES_INDEX, body=data)

    def get(self, experiment_name):
        pass
