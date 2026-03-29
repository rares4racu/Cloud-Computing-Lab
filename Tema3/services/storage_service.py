from google.cloud import storage
import uuid
import os

BUCKET = os.environ.get("BUCKET_NAME", "clients-avatars-bucket")

def upload_avatar(file, client_id: int) -> str:
    client = storage.Client()
    bucket = client.bucket(BUCKET)
    blob_name = f"avatars/{client_id}_{uuid.uuid4().hex}"
    blob = bucket.blob(blob_name)
    blob.upload_from_file(file.file, content_type=file.content_type)
    blob.make_public()
    return blob.public_url