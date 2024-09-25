from celery import shared_task
from elasticsearch import Elasticsearch
from .models import MyModel

@shared_task
def index_model(instance_id):
    es = Elasticsearch(['elasticsearch:9200'])
    instance = MyModel.objects.get(id=instance_id)
    doc = {
        'name': instance.name,
        'description': instance.description,
    }
    es.index(index='models_index', id=instance.id, body=doc)
