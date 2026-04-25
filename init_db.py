# script used to setup cosmos DB when init_container spins up


from azure.cosmos import CosmosClient, PartitionKey
import os                                                                                # allows script to read environment variables

# retrieves these values from the containers OS. Check the container_app block on main to find them                  # extracts env variables and stores as python variables
COSMOS_ENDPOINT = os.environ['COSMOS_ENDPOINT']
COSMOS_KEY = os.environ['COSMOS_KEY']
DATABASE_NAME = os.environ['COSMOS_DB_NAME']
CONTAINER_NAME = os.environ['COSMOS_CONTAINER_NAME']

try:
    # Initialize Cosmos client
    client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)

    # Create database if not exists
    database = client.create_database_if_not_exists(id=DATABASE_NAME)

    # Create container if not exists with id as partition key
    container = database.create_container_if_not_exists(
        id=CONTAINER_NAME,
        partition_key=PartitionKey(path="/id"),                                                               # distributes data based on ID field in each doc
        offer_throughput=400                                                                                  # sets the request units per second
    )

    print("Cosmos DB database and container setup complete.")

except Exception as e:
    print("Cosmos DB initialization failed:", e)
    exit(1)


# CosmosClient is your access badge and PartitionKey defines how mail is sorted into boxes