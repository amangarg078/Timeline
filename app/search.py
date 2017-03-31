from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
import models

connections.create_connection()


class PostIndex(DocType):
    user = Text()
    date_created = Date()
    description = Text()

    class Meta:
        index = 'post-index'


def bulk_indexing():
    PostIndex.init()
    es = Elasticsearch(timeout=30)
    bulk(client=es, actions=(b.indexing() for b in models.Post.objects.all().iterator()))


def user_search(user):
    s = Search().filter('term', user=user)
    response = s.execute()
    return response


def desc_search(description):
    s = Search().filter('term', description=description)
    response = s.execute()
    return response