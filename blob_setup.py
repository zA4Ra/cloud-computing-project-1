from azure.storage.blob import BlobServiceClient

# Connect to Azurite
connection_string = "UseDevelopmentStorage=true"

blob_service_client = BlobServiceClient.from_connection_string(
    connection_string
)

# Access the existing container
container_name = "diet-data"

container_client = blob_service_client.get_container_client(
    container_name
)

# Upload All_Diets.csv
blob_client = blob_service_client.get_blob_client(
    container=container_name,
    blob="All_Diets.csv"
)

with open("All_Diets.csv", "rb") as data:
    blob_client.upload_blob(data, overwrite=True)

print("All_Diets.csv uploaded successfully!")

print("\nFiles in Blob Storage:")

for blob in container_client.list_blobs():
    print(blob.name)