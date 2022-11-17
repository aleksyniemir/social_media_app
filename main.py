from fastapi import FastAPI
import logging

app = FastAPI()

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/userssss")
def get_user(id: int):
    logging.info(f"Searching for an user with id = {id}")
    return {"user": "olek"}

@app.post("/post")
def create_post(): ...
    