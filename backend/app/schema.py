import graphene
from graphene_django.types import DjangoObjectType
from .models import MyModel

class MyModelType(DjangoObjectType):
    class Meta:
        model = MyModel

class Query(graphene.ObjectType):
    all_models = graphene.List(MyModelType)

    def resolve_all_models(self, info, **kwargs):
        return MyModel.objects.all()

class Mutation(graphene.ObjectType):
    # Мутации здесь
    pass
