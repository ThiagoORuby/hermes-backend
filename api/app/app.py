from http import HTTPStatus

from fastapi import FastAPI

app = FastAPI(title="Hermes Backend")


@app.get("/", status_code=HTTPStatus.OK)
def read_root():
    return {"message": "Hello, World!"}
