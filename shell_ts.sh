export TYPESENSE_API_KEY=abcd
collection_name=$(curl -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}" \
    -s "http://localhost:8108/aliases/products" | jq -r ".collection_name")
echo $collection_name

curl -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}" \
"http://localhost:8108/collections/$collection_name/documents/search\
?q=*"


