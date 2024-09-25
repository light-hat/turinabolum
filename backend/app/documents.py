from django_elasticsearch_dsl import Document, Index
from .models import MyModel

models_index = Index('models_index')

@models_index.document
class MyModelDocument(Document):
    class Django:
        model = MyModel
        fields = ['name', 'description']
