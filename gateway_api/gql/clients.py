import logging

from django.conf import settings
from opensearchpy import OpenSearch

logger = logging.getLogger(__name__)

_opensearch_client = None


def get_opensearch_client():
    """
    Создает и возвращает клиент OpenSearch.
    Использует синглтон-паттерн для избежания множественных подключений.
    """
    global _opensearch_client
    if _opensearch_client is None:
        try:
            _opensearch_client = OpenSearch(**settings.OPENSEARCH_CONFIG)
            info = _opensearch_client.info()
            logger.info(f"Успешно подключились к OpenSearch: {info}")
        except Exception as e:
            logger.error(f"Ошибка подключения к OpenSearch: {e}")
            raise
    return _opensearch_client
