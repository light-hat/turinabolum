import graphene
from graphene_django.types import DjangoObjectType
from app.models import *
from app.tasks import process_disk_dump

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

# Mutations (and mutants)

class CreateDumpMutation(graphene.Mutation):
    class Arguments:
        case = graphene.String(required=True)
        filename = graphene.String(required=True)
        dump_type = graphene.String(required=True)

    dump = graphene.Field(DumpType)
    
    def mutate(self, info, case, filename, dump_type):
        case_obj = Case.objects.get(id=case)
        dump = Dump.objects.create(
            case=case_obj,
            filename=filename,
            dump_type=dump_type,
            status='processing'
        )
        process_disk_dump.delay(dump.id)
        return CreateDumpMutation(dump=dump)

# END Mutations

class Query(graphene.ObjectType):
    dump = graphene.Field(DumpType, id=graphene.String(required=True))
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
