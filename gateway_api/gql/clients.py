import logging

from django.conf import settings
from opensearchpy import OpenSearch

logger = logging.getLogger(__name__)

_client = None


def get_opensearch_client() -> OpenSearch:
    global _client
    if _client is None:
        _client = OpenSearch(
            hosts=settings.OPENSEARCH_HOSTS,
            http_auth=settings.OPENSEARCH_AUTH,
            use_ssl=settings.OPENSEARCH_USE_SSL,
            verify_certs=settings.OPENSEARCH_VERIFY_CERTS,
        )
    return _client
