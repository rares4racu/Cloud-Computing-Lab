from google.cloud import datastore

client = datastore.Client()
KIND = "clients"

def get_clients():
    query = client.query(kind=KIND)
    return [{"id": str(entity.key.id), **dict(entity)} for entity in query.fetch()]

def get_client_id(id_client: str):
    key = client.key(KIND, int(id_client))
    entity = client.get(key)
    if entity:
        return [{"id": str(entity.key.id), **dict(entity)}]
    return []

def get_client_name(name: str):
    query = client.query(kind=KIND)
    query.add_filter("name", "=", name)
    return [{"id": str(entity.key.id), **dict(entity)} for entity in query.fetch()]

def insert_client(client_data: dict):
    key = client.key(KIND, int(client_data["id"]))
    entity = datastore.Entity(key=key)
    entity.update({
        "status": client_data["status"],
        "name": client_data["name"],
        "emailAddress": client_data["emailAddress"]
    })
    client.put(entity)

def update_client(id_client: str, data: dict):
    key = client.key(KIND, int(id_client))
    entity = client.get(key)
    if entity:
        entity.update({
            "status": data.get("status", entity.get("status")),
            "name": data.get("name", entity.get("name")),
            "emailAddress": data.get("emailAddress", entity.get("emailAddress"))
        })
        client.put(entity)

def delete_client(id_client: str):
    key = client.key(KIND, int(id_client))
    client.delete(key)