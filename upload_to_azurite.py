from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError, ServiceRequestError
import os
import sys
import time

# Same settings as lambda_function.py
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING", "UseDevelopmentStorage=true")
container_name = os.getenv("CONTAINER_NAME", "diet-data")
blob_name = os.getenv("BLOB_NAME", "All_Diets.csv")

# CSV file path can be given when running the script
if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    file_path = "All_Diets.csv"

blob_service_client = BlobServiceClient.from_connection_string(connection_string)

# Try a few times in case Azurite is still starting up
for attempt in range(15):
    try:
        try:
            blob_service_client.create_container(container_name)
            print("Container created:", container_name)
        except ResourceExistsError:
            print("Container already exists:", container_name)

        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        print(f"Uploaded {file_path} to Azurite Blob Storage!")
        break
    except ServiceRequestError:
        print("Azurite is not ready yet, trying again...")
        time.sleep(2)
else:
    print("Could not connect to Azurite.")
    sys.exit(1)
