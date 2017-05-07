import os
import unittest
from signin import AWSConnection
from elasticsearch import Elasticsearch


class TestAWSESConnection(unittest.TestCase):

    def test_es(self):
        es = Elasticsearch(connection_class=AWSConnection,
                           region='us-west-2',
                           host=os.environ.get("ESHOST"))
        search = es.search()
        info = es.info()
        self.assertEquals(1.0, search['hits']['hits'][0]['_score'])
        self.assertEquals('BTicYwG', info['name'])


if __name__ == '__main__':
    unittest.main()
