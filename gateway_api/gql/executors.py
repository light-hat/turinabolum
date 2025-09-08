from gql.clients import get_opensearch_client
from opensearchpy import Q, Search


class OpenSearchExecutor:
    def __init__(self, indices: list[str]):
        self.client = get_opensearch_client()
        self.indices = indices
        self.search = Search(using=self.client, index=",".join(indices))
        self.aggs = {}

    def apply_filters(self, **filters):
        for field, value in filters.items():
            if value is not None:
                if isinstance(value, dict):
                    if "gt" in value:
                        self.search = self.search.filter(
                            "range", **{field: {"gt": value["gt"]}}
                        )
                else:
                    self.search = self.search.filter("term", **{field: value})

    def apply_query_string(self, query_string: str):
        if query_string:
            self.search = self.search.query("query_string", query=query_string)

    def add_aggregation(self, name, agg_type, field=None, body=None):
        if agg_type == "terms" and field:
            self.aggs[name] = {"terms": {"field": field}}
        elif body:
            self.aggs[name] = body

    def execute(self, size=50, from_=0):
        if self.aggs:
            self.search.aggs.bucket("global_agg", "global")
            for name, body in self.aggs.items():
                self.search.aggs["global_agg"].bucket(name, body)

        response = self.search[size : size + from_].execute()
        return response
