# Setting up Typesense

<img src="https://avatars.githubusercontent.com/u/19822348?s=200&v=4" width="80">

## Installing Typesense

### Using Docker

```shell script
docker pull typesense/typesense:0.21.0
```

Configure APK Key

```shell script
export TYPESENSE_API_KEY=any_api_key
```

Configure a data directory that will be used to restore data if the server crashes or needs to be restarted for some reason.

```shell script

```

```shell script
mkdir /data/typesense-data
```

Run image in detached mode. 
Include data directory path (point to volumne mount) and api key.


```shell script
docker run -d -p 8108:8108 -v/data/typesense-data:/data typesense/typesense:0.21.0 \
  --data-dir /data --api-key=$TYPESENSE_API_KEY 
```

## Configure collections

```shell script
curl "http://localhost:8108/collections" \
    -X POST \
    -H "Content-Type: application/json" \
    -H "X-TYPESENSE-API-KEY: $TYPESENSE_API_KEY" \
    -d '{
        "name": "products_01",
        "fields": [                    
            {"name": "id", "type": "string"},
            {"name": "name", "type": "string", "facet": true},
            {"name": "slug", "type": "string"},
            {"name": "categories", "type": "string[]", "optional": true},
            {"name": "purchases", "type": "int32"},
            {"name": "price", "type": "int32"},
            {"name": "pretty_price", "type": "string"},
            {"name": "shop_name", "type": "string"},
            {"name": "shop_image_url", "type": "string"},
            {"name": "shop_url", "type": "string"},
            {"name": "header_image_url", "type": "string", "optional": true},
            {"name": "discoverable", "type": "bool"},
            {"name": "available", "type": "bool"}
            ],
        "default_sorting_field": "purchases"
    }'
```

## Create alias

Typesense alias are virtual names that points to the actual collection name. 

Useful when you need to reindex a new collection without disrupting the collection in production.

```shell script
curl "http://localhost:8108/aliases/alias_name_here" -X PUT \
    -H "Content-Type: application/json" \
    -H "X-TYPESENSE-API-KEY: $TYPESENSE_KEY" -d '{
        "collection_name": "actual_collection_name_here"
    }'
```

## Index collection

```shell script
curl "http://localhost:8108/collections/products_01/documents?action=upsert" -X POST \
        -H "Content-Type: application/json" \
        -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}" \
        -d '{
          "id": "124",
          "name": "Stark X1",
          "slug": "Stark",
          "purchases": 12,
					"price": 5000,
          "pretty_price": "SGD 5000"
          "shop_name": "Tony Pte"
          "shop_image_url": "https://cdn.adgo.io/pte.png"
          "shop_url": "https://www.adgo.io.tony"
          "discoverable": true,
          "available": true
        }'
```

## Search Collection

```shell script
curl -H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}" \
"http://localhost:8108/collections/products_01/documents/search\
?q=stark&query_by=name&filter_by=price:>100\
&sort_by=purchases:desc"
```

## Backup Typesense

As indexed data are in-memory, it is important to perform regular snapshots of the current engine state to prevent total lost of your data in the event of a server failure.

Typically, snapshots should be stored in a secured location that will not be affected by any downtime.
In the case of a server failure, once Typesense is back online, it will automatically detect for any snapshot based on the data-directory configured and restore them.

```shell script
curl "http://localhost:8108/operations/snapshot?snapshot_path=/data/typesense-data" -X POST \
-H "Content-Type: application/json" \
-H "X-TYPESENSE-API-KEY: ${TYPESENSE_API_KEY}"
```
