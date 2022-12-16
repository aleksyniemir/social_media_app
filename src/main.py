from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from src.api import users
from src.db.database import Base, engine
# uncomment at the end of the project
#import logging.config
#import logging
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

app = FastAPI()

app.include_router(users.router)

# uncomment at the end of the project
# logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
# logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

@app.get("/")
async def hello():
    return "Hello!"



