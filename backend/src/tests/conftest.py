from fastapi.testclient import TestClient
from fastapi import Depends, FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from src.db.database import Base
from src.crud.users import get_user_by_username, create_user, get_db, authenticate_user, get_password_hash
from src.api import users
import src.schemas as schemas

def start_application():
    app = FastAPI()
    app.include_router(users.router)
    return app

engine = create_engine(
    "postgresql://postgres:haslo123@localhost:5555/webowka_project_zaliczeniowy_test"
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_app():
    Base.metadata.create_all(engine)  # Create the tables.
    app = start_application()
    yield app
    Base.metadata.drop_all(engine)
    
@pytest.fixture(scope="function")
def test_db(test_app):
    db = TestingSessionLocal()
    try: 
        yield db
    finally:
        db.close()
        
@pytest.fixture(scope="function")
def client(test_app, test_db):
    def _get_test_db():
        try:
            yield test_db
        finally:
            pass
    test_app.dependency_overrides[get_db] = _get_test_db
    with TestClient(test_app) as client:
        yield client
             
def user_authentication_headers(client, username: str, password: str):
    data = {"username": username, "password": password}
    headers = client.headers
    r = client.post("users/token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers

def authentication_token_from_username(client, test_db, username: str):
    user = get_user_by_username(test_db, username)
    if not user:
        user_in_create = schemas.UserCreate(
            username=username, name="tomek", surname="b",
            email="tomekb", password="haslo123")
        create_user(test_db, user_in_create)
    return user_authentication_headers(client, username=username, password="haslo123")

@pytest.fixture(scope="function")    
def normal_user_token_headers(test_app, test_db, client):
    return  authentication_token_from_username(client, test_db, "TEST_USERNAME")

