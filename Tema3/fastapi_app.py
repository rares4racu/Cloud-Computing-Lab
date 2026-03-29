from typing import Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from database.db import *
from services.tasks_service import create_task
from services.storage_service import upload_avatar

appFast = FastAPI()

appFast.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

appFast.mount("/static", StaticFiles(directory="static"), name="static")

class Client(BaseModel):
    id: int
    status: str
    name: str
    emailAddress: str


# ───── GET ─────
@appFast.get("/clients")
def get_clients_fastapi(id: Optional[int] = None, name: Optional[str] = None):
    if id is not None:
        return get_client_id(id)
    if name is not None:
        return get_client_name(name)
    return get_clients()


# ───── POST ─────
@appFast.post("/clients")
def post_clients_fastapi(client: Client):
    insert_client(client.model_dump())
    create_task({"action": "created", "client_id": client.id, "name": client.name})
    return {"message": "Client created"}


# ───── POST upload avatar ─────
@appFast.post("/clients/{client_id}/avatar")
def upload_client_avatar(client_id: int, file: UploadFile = File(...)):
    url = upload_avatar(file, client_id)
    update_client(str(client_id), {"avatarUrl": url})
    return {"message": "Avatar uploaded", "url": url}


# ───── PUT ─────
@appFast.put("/clients")
def put_clients_fastapi(client: Client, id: Optional[int] = None):
    if id is not None:
        update_client(str(id), client.model_dump())
        create_task({"action": "updated", "client_id": id})
        return {"message": "Client updated"}
    insert_client(client.model_dump())
    return {"message": "Client added"}


# ───── DELETE ─────
@appFast.delete("/clients")
def delete_clients_fastapi(id: int = None):
    if id is None:
        raise HTTPException(status_code=400, detail="No id provided")
    delete_client(str(id))
    create_task({"action": "deleted", "client_id": id})
    return {"message": "Client deleted"}


# ───── Task handler ─────
@appFast.post("/task-handler")
async def task_handler(payload: dict):
    print(f"[TASK] Action: {payload.get('action')} | Client: {payload.get('client_id')}")
    return {"status": "processed"}