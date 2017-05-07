import logging
import os

from AWSAccess.signin import AWSConnection

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk

_INDEX_NAME = 'ds1'
_TYPE_NAME = 'review'
_ESREGION = 'us-west-2'
_HOST = os.environ.get("ESHOST")

def create_review_index(client, index=_INDEX_NAME):
    # Create Mapping Analyzer and empty index
    user_mapping = {
        '' 
    }

def parse_commits(head, name):
    """Get through the reviews and generate a document per review
    containing all the metadata
    """
    pass

def load_review(client, path=None, index=_INDEX_NAME):
    """Parsing a review from one source and load it into elastic
    using 'client'. If the index does not exists, abort
    """
    pass

def clear_index(client, index=_INDEX_NAME):
    """If the index exits, delete"""
    pass

if __name__ == '__main__':
    tracer = logging.getLogger('elasticsearch.trace')
    es_client = Elasticsearch(connection_class=AWSConnection,
                              region = _ESREGION,
                              host = _HOST)
