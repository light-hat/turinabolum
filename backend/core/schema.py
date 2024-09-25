import graphene
from app.schema import Query as AppQuery, Mutation as AppMutation


class Query(AppQuery, graphene.ObjectType):
    pass


class Mutation(AppMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
