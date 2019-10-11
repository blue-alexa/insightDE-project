import logging
import elasticsearch

from EdgarManagers.config import ELASTIC_URI

class ESLoader(object):
    def __init__(self):
        self.conn = elasticsearch.Elasticsearch([ELASTIC_URI])
        self.logger = logging.getLogger("DailyJobs.es_loader")

    def insert(self, index_name, type_name, id, body):
        self.conn.index(index=index_name, doc_type=type_name, id=id, body=body)
        self.logger.info(f"Inserted {id} to ElasticSearch")