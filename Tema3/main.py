import uvicorn
from fastapi_app import appFast

if __name__ == "__main__":
    uvicorn.run("main:appFast", host="0.0.0.0", port=8080)