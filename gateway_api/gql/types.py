import graphene


class PostType(graphene.ObjectType):
    """
    GraphQL-тип, соответствующий документу в индексе 'post' OpenSearch.
    """

    id = graphene.ID(required=True)
    title = graphene.String()
    content = graphene.String()
    author_id = graphene.Int()
    created_at = graphene.String()


class UserType(graphene.ObjectType):
    """
    GraphQL-тип, соответствующий документу в индексе 'user' OpenSearch.
    """

    id = graphene.ID(required=True)
    username = graphene.String()
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()


class SearchResultItem(graphene.Union):
    """
    Union-тип, который может возвращать либо PostType, либо UserType.
    Система определяет конкретный тип на основе поля '_index' в ответе от OpenSearch.
    """

    class Meta:
        types = (PostType, UserType)

    @classmethod
    def resolve_type(cls, instance, info):
        """
        Определяет, какой GraphQL-тип использовать для данного результата.
        """
        if instance.get("_index") == "post":
            return PostType
        elif instance.get("_index") == "user":
            return UserType
        return None
