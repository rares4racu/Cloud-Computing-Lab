from google.cloud import secretmanager
import os

PROJECT = os.environ.get("GCP_PROJECT", "project-73f86bbc-37a9-4385-af6")

def get_secret(secret_name: str) -> str:
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT}/secrets/{secret_name}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")