from google.cloud import tasks_v2
import json
import os

PROJECT  = os.environ.get("GCP_PROJECT",  "project-73f86bbc-37a9-4385-af6")
LOCATION = os.environ.get("GCP_LOCATION", "europe-west3")
QUEUE    = os.environ.get("TASK_QUEUE",   "clients-queue")

def create_task(payload: dict):
    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(PROJECT, LOCATION, QUEUE)
    task = {
        "http_request": {
            "http_method": tasks_v2.HttpMethod.POST,
            "url": f"https://project-73f86bbc-37a9-4385-af6.appspot.com/task-handler",
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(payload).encode()
        }
    }
    client.create_task(request={"parent": parent, "task": task})