import graphene
from graphene_django.types import DjangoObjectType
from app.models import *


class CaseType(DjangoObjectType):
    class Meta:
        model = Case


class DumpType(DjangoObjectType):
    class Meta:
        model = Dump


class DeviceType(DjangoObjectType):
    class Meta:
        model = Device


class DeviceUserType(DjangoObjectType):
    class Meta:
        model = DeviceUser


class CyberAttackType(DjangoObjectType):
    class Meta:
        model = CyberAttack


class CompromiseIndicatorType(DjangoObjectType):
    class Meta:
        model = CompromiseIndicator


class CreateDumpMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    dump = graphene.Field(DumpType)

    def mutate(self, info, name, description):
        dump = Dump.objects.create(name=name, description=description)
        # Запускаем Celery задачу
        #process_task.delay(dump.id)
        return CreateDumpMutation(dump=dump)


class Query(graphene.ObjectType):
    dump = graphene.Field(DumpType, id=graphene.Int(required=True))
    dumps = graphene.List(DumpType)

    def resolve_dump(self, info, id):
        try:
            return Dump.objects.get(pk=id)
        except Dump.DoesNotExist:
            return None

    def resolve_dumps(self, info):
        return Dump.objects.all()

class Mutation(graphene.ObjectType):
    handle_dump = CreateDumpMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
