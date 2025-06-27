from http import HTTPStatus

from fastapi import FastAPI

from . import router

app = FastAPI(title="Hermes Backend")


app.include_router(router.router)


@app.get("/", status_code=HTTPStatus.OK)
def read_root():
    return {"message": "Hello, World!"}
