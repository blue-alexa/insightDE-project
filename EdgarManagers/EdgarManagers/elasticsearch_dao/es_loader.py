import logging

import elasticsearch

from EdgarManagers.config import ELASTIC_URI

class ESLoader(object):
    def __init__(self):
        self.conn = elasticsearch.Elasticsearch([ELASTIC_URI])
        self.logger = logging.getLogger("DailyJobs.es_loader")

    def create_index(self, index_name):
        if not self.conn.indices.exists(index_name):
            self.conn.indices.create(index_name)
            self.logger.info(f"Index {index_name} created")
        else:
            self.logger.info(f"Index {index_name} already exists.")

    def create_mapping(self, index_name, type_name, mapping):
        self.conn.indices.put_mapping(index=index_name, doc_type=type_name, body=mapping)
        self.logger.info(f"Mapping for Index {index_name} Type {type_name} created")

    def insert(self, index_name, type_name, id, body):
        self.conn.index(index=index_name, doc_type=type_name, id=id, body=body)
        self.logger.info(f"Inserted {id} to ElasticSearch")