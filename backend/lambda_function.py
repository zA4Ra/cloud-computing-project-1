from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import json


def lambda_handler():
    # Azurite Blob Storage settings
    connection_string = "UseDevelopmentStorage=true"
    container_name = "diet-data"
    blob_name = "All_Diets.csv"

    # Connect to Azurite
    blob_service_client = BlobServiceClient.from_connection_string(
        connection_string
    )

    # Connect to All_Diets.csv in Blob Storage
    blob_client = blob_service_client.get_blob_client(
        container=container_name,
        blob=blob_name
    )

    # Download the CSV from Blob Storage
    downloaded_blob = blob_client.download_blob()
    csv_data = downloaded_blob.readall()

    print("All_Diets.csv downloaded successfully from Blob Storage!")

    # Read the downloaded CSV using Pandas
    df = pd.read_csv(io.BytesIO(csv_data))

    print(f"Loaded {len(df)} rows from the CSV.")

    # Calculate average macros for each diet type
    average_macros = df.groupby("Diet_type")[
        ["Protein(g)", "Carbs(g)", "Fat(g)"]
    ].mean()

    print("\nAverage macros by diet type:")
    print(average_macros)

    # Convert results to a dictionary
    results = average_macros.round(2).to_dict(orient="index")

    # Save processed results to a JSON file
    with open("results.json", "w") as file:
        json.dump(results, file, indent=4)

    print("\nResults saved successfully to results.json!")

    return results


# Run the function locally
if __name__ == "__main__":
    lambda_handler()