import graphene

from .clients import get_opensearch_client
from .types import SearchResultItem


class Query(graphene.ObjectType):
    """
    Main Query GraphQL class.
    """

    search = graphene.List(
        SearchResultItem,
        required=True,
        query_string=graphene.String(required=True),
        indices=graphene.List(graphene.String, default_value=["post", "user"]),
        size=graphene.Int(default_value=10),
        from_=graphene.Int(default_value=0, name="from"),
        description="Search by selected OpenSearch indexes",
    )

    def resolve_search(self, info, query_string, indices, size, from_, **kwargs):
        """
        Resolver for fiels 'search'.
        Execute multi-search request to OpenSearch.
        """
        if not info.context.user.is_authenticated:
            raise graphene.PermissionDenied("Need authentication.")

        client = get_opensearch_client()

        body = []
        for index in indices:
            body.append({"index": index})
            body.append(
                {
                    "query": {"query_string": {"query": query_string}},
                    "from": from_,
                    "size": size,
                }
            )

        response = client.msearch(body=body)

        results = []
        for resp in response["responses"]:
            if "hits" in resp and "hits" in resp["hits"]:
                for hit in resp["hits"]["hits"]:
                    hit["_source"]["_index"] = hit["_index"]
                    results.append(hit["_source"])

        return results


schema = graphene.Schema(query=Query)
