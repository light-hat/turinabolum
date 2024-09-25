import graphene
from graphene_django.types import DjangoObjectType
from app.models import Case, Dump, Device, DeviceUser, CyberAttack, CompromiseIndicator

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

class Query(graphene.ObjectType):
    all_cases = graphene.List(CaseType)
    case = graphene.Field(CaseType, id=graphene.UUID())
    all_dumps = graphene.List(DumpType)
    dump = graphene.Field(DumpType, id=graphene.UUID())

    def resolve_all_cases(self, info, **kwargs):
        return Case.objects.all()

    def resolve_case(self, info, id):
        return Case.objects.get(id=id)

    def resolve_all_dumps(self, info, **kwargs):
        return Dump.objects.all()

    def resolve_dump(self, info, id):
        return Dump.objects.get(id=id)

'''class Mutation(graphene.ObjectType):
    create_case = graphene.Field(CaseType, name=graphene.String(), description=graphene.String())

    def resolve_create_case(self, info, name, description):
        case = Case(name=name, description=description)
        case.save()
        return case'''

schema = graphene.Schema(query=Query) # , mutation=Mutation)
