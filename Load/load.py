import logging
import os
import json

# sys.path.append('../')
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk

from .AWSAccess.signin import AWSConnection

_INDEX_NAME = 'ds1'
_TYPE_NAME = 'review'
_ESREGION = 'us-west-2'
_HOST = os.environ.get("ESHOST")


def getmultifield(field_name, string_keyword='keyword'):
    """Define multifield mapping

    Args:
        field_name: Name for the field that needed to be
                    indexded in different ways
        string_keyword: 'keyword' is the default value
                        'string' is depreciated for 5.X

    Return:
        A dict mapping a field to both keyword and text
    """
    multiple_field = {
        'properties': {
            field_name: {
                'type': 'text',
                'fields': {
                    'raw': {
                        'type': string_keyword,
                        'index': 'not_analyzed'
                    }
                }
            }
        }
    }
    return multiple_field


def ulta_mapping():
    review_mappings = {
        'reviews': {
            'name': getmultifield('name'),
            'category': getmultifield('category'),
            'regimen': {'type': 'text'},
            'size': {'type': 'keyword'},
            'cons': getmultifield('cons'),
            'pros': getmultifield('pros'),
            'best_uses': getmultifield('best_uses'),
            'brand': {'type': 'brand'},
            'num_reviews': {'type': 'integer'},
            'review_rating': {'type': 'float'},
            'details': getmultifield('details'),
            'ingredient': getmultifield('ingredient'),
            'price': {'type': 'integer'},
            'description': {'type': 'text'},
            'review_pros': getmultifield('review_pros'),
            'review_cons': getmultifield('review_cons'),
            'review_bestuses': getmultifield('review_bestuses'),
            'review_rating_score': {'type', 'float'},
            'review_title': getmultifield('review_title'),
            'review_text': getmultifield('review_text'),
            'review_author_name': {'type', 'keyword'},
            'review_state': {'type', 'keyword'},
            'review_location': {'type', 'keyword'},
            'review_date': {'type', 'date'},
            'review_author_type': getmultifield('review_author_type')
        }
    }
    return review_mappings


def create_review_index(client, review_mapping_format, index=_INDEX_NAME):
    """Create Mapping Analyzer and empty index
    """

    analysis = {
        'char_filter': {
            'replace': {
                'type': 'mapping',
                'mappings': [
                    '&=> and '
                ]
            }
        },
        'filter': {
            'word_delimiter': {
                'type': 'word_delimiter',
                'split_on_numerics': false,
                'split_on_case_change': true,
                'generate_word_parts': true,
                'generate_number_parts': true,
                'catenate_all': true,
                'preserve_original': true,
                'catenate_numbers': true
            }
        },
        'analyzer': {
            'default': {
                'type': 'custom',
                'char_filter': [
                    'html_strip',
                    'replace'
                ],
                'tokenizer': 'whitespace',
                'filter': [
                    'lowercase',
                    'word_delimiter'
                ]
            }
        }
    }

    create_index_body = {
        'settings': {
            'number_of_shards': 1,
            'number_of_replicas': 0,

            'analysis': analysis
        },
        'mappings': ulta_mappings
    }

    try:
        client.indices.create(
            index = index,
            body = create_index_body
        )
    except TransportError as e:
        if e.error == 'index_already_exists_exception' :
            client.indices.delete(index)
        else:
            raise
    return


def parse_ultaReviews(filename):
    """Get through the ulta reviews and generate a document per review
    containing all the metadata
    """
    with open(filename) as f:
        data = json.load(f)


def load_ultaReviews(client, path=None, index=_INDEX_NAME):
    """Parsing a review from one source and load it into elastic
    using 'client'. If the index does not exists, abort
    """
    filename='../../Data/ulta_serum_processed_new.json'
    parse_ultaReviews(filename)


def clear_index(client, index=_INDEX_NAME):
    """If the index exits, delete
    """
    pass


if __name__ == '__main__':
    tracer = logging.getLogger('elasticsearch.trace')
    es_client = Elasticsearch(connection_class=AWSConnection,
                              region=_ESREGION,
                              host=_HOST)
    load_ultaReviews(es_client)
    #now we run a test to count the documents
    #print(es_client.count(index=_INDEX_NAME)['count'], 'documents in index')
