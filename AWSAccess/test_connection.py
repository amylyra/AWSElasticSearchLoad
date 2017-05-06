import os
import unittest
from signin import AWSConnection
from elasticsearch import Elasticsearch


class TestAWSESConnection(unittest.TestCase):

    def test_es():
        es = Elasticsearch(connection_class=AWSConnection,
                           region='us-west-2',
                           host=os.environ.get("ESHOST"))
        search = es.search()
        info = es.info()
        self.assertEquals(1.0, es.search()['hits']['hits'][0]['_score'])
        self.assertEquals('BTicYwG', es.info()['name'])
