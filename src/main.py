from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from src.api import users
from db.database import Base, engine
import logging.config
import logging

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/")
async def hello():
    return "Hello!"



