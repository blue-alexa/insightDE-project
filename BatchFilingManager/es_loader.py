import logging
import elasticsearch

from config import ELASTIC_URI

class ESLoader(object):
    def __init__(self):
        self.conn = elasticsearch.Elasticsearch([ELASTIC_URI])
        self.logger = logging.getLogger("BatchFilingManager.es_loader")

    def create_mapping(self, index_name, type_name, mapping):
        # remove index if exist
        if self.conn.indices.exists(index_name):
            self.conn.indices.delete(index_name)

        # create index
        self.conn.indices.create(index_name)
        self.conn.cluster.health(wait_for_status="yellow")

        # create mapping
        self.conn.indices.put_mapping(index=index_name, doc_type=type_name, body=mapping)
        self.logger.info(f"Mapping created {mapping}")

    def insert(self, index_name, type_name, id, body):
        self.conn.index(index=index_name, doc_type=type_name, id=id, body=body)
        self.logger.info(f"Inserted {id} to ElasticSearch")

