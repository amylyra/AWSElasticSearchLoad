AWSElasticSearchLoad
====================

Load processed reviews to AWS ElasticSearch Service

To create AWS connection, use AWSConnection
---------------------

.. code:: python

    from AWSAccess.signin import AWSConnection
    from elasticsearch import Elasticsearch
    
    _HOST = os.environ.get("ESHOST")

    es_client = Elasticsearch(connection_class=AWSConnection,
                              region=_REGION,
                              host=_HOST)
    

AWSConnection will return a ElasticSearch Client that Accept
AWS credientials. Default is AWS environmental variable.
Could set secrete key at AWSConnection.secret and access key at 
AWSconnection.key
