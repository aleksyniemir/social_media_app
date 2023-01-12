from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from src.api import users
from src.api import posts
from src.db.database import Base, engine
# uncomment at the end of the project
#import logging.config
#import logging
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

# import src.models as models
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)

origins = [
    "null",
    "http://127.0.0.1",
    "http://127.0.0.1:8000/",
    "http://127.0.0.1:8080/",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# uncomment at the end of the project
# logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
# logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

@app.get("/")
async def hello():
    return "Hello!"



