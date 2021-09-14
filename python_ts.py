import typesense
import os
import logging

logger = logging.getLogger(__name__)

TYPESENSE_API_KEY = os.environ.get("TYPESENSE_API_KEY")
TYPESENSE_HOST = os.environ.get("TYPESENSE_HOST", "localhost")
ALIAS_NAME = "products"

client = typesense.Client(
    {
        "api_key": TYPESENSE_API_KEY,
        "nodes": [{"host": TYPESENSE_HOST, "port": "8108", "protocol": "http"}],
        "connection_timeout_seconds": 2,
    }
)

alias_data = client.aliases[ALIAS_NAME].retrieve()
collection_name = alias_data["collection_name"]

results = client.collections[collection_name].documents.search({"q": "*"})

logger.info(results)
