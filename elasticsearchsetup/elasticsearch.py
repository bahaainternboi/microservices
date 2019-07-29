from elasticsearch import Elasticsearch

class elasticSearchFactory(object):
    def __init__(self, host: str, port: int):
        self.host= host
        self.port= port

    def create(self) -> Elasticsearch:
        return Elasticsearch(
            [{'host': self.host, 'port': self.port}]
        )

class elasticSearchIndex(object):
    def __init__(self, elasticfactory: elasticSearchFactory, indexname: str, doctype: str, indexmapper: dict):
        self.elasticfactory= elasticfactory
        self.indexname= indexname
        self.doctype= doctype
        self.indexmapper= indexmapper

    def connection(self) -> Elasticsearch:
        if not self.instance:
            self.instasnce= self.elasticfactory.create()

            if not self.instance.indices.exist(self.index_name):
                self.instance.indices.create(
                    index= self.indexname,
                    body= self.indexmapper
                )
        return self.instance

    def index(self, payload: dict) -> bool:
        return self.connection().index(
            index= self.indexname,
            doc_type= self.doctype,
            body= payload
        )

    def existsbyurl(self, url: str) -> bool:
        matches = self.connection.search(
            index= self.indexname,
            doc_type= self.doctype,
            body= {
                "query": {
                    "query_string": {
                        "query": 'url:"{}"'.format(url)
                    }
                }
            }
        )

        hits= matches['hits']['hits']

        if hits:
            return True

        return False