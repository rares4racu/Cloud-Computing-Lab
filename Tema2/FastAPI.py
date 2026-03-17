from typing import Optional
from fastapi import FastAPI, HTTPException
from APIDatabase import *
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

appFast = FastAPI()


appFast.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Client(BaseModel):
    id: int
    status: str
    name: str
    emailAddress: str


"""
GET
"""


@appFast.get("/clients")
def get_clients_fastapi(id: Optional[int] = None, name: Optional[str] = None):
    if id is not None:
        return get_client_id(id)
    if name is not None:
        return get_client_name(name)
    return get_clients()


"""
POST
"""


@appFast.post("/clients")
def post_clients_fastapi(client: Client):
    if client is None:
        raise HTTPException(status_code=400, detail="No information provided")
    required_fields = ["id", "status", "name", "emailAddress"]
    client_fin = client.model_dump()
    for field in required_fields:
        if field not in client_fin:
            raise HTTPException(status_code=400, detail=f"Field {field} is required")
    insert_client(client.model_dump())
    return {"message": "Client created"}

"""
PUT
"""


@appFast.put("/clients")
def put_clients_fastapi(client: Client, id: Optional[int] = None):
    if client is None:
        raise HTTPException(status_code=400, detail="No information provided")
    if id is not None:
        update_client(id, client.model_dump())
        return {"message": "Client updated"}
    client_fin = client.model_dump()
    required_fields = ["id", "status", "name", "emailAddress"]
    for field in required_fields:
        if field not in client_fin:
            raise HTTPException(status_code=400, detail=f"Field {field} is required")
    insert_client(client.model_dump())
    return {"message": "Client added"}


"""
DELETE
"""


@appFast.delete("/clients")
def delete_clients_fastapi(id: int = None):
    if id is None:
        raise HTTPException(status_code=400, detail="No id provided")
    delete_client(id)
    return {"message": "Client deleted"}
