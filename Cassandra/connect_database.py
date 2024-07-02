from astrapy import DataAPIClient

# Initialize the client
client = DataAPIClient("AstraCS:XdxTDjYFgkGWWaKusHQtMLQL:1eda724ac3bc5f931c1afb62b378aed0098bfe1e0d524fe69c5dbc1e6ddc5da5")

# Correct way to get the database (keyspace) object
db = client.get_database_by_api_endpoint(
    "https://fd531734-29b2-4f64-a298-f12b2f81ebc8-us-east-2.apps.astra.datastax.com"
)


# List collection names (note the absence of `.mercadolivre`)
print(f"Connected to Astra DB: {db.list_collection_names()}") 