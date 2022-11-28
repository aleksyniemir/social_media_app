from fastapi.testclient import TestClient
import pytest

from src.main import app
from src.crud.users import get_max_id, fake_users_db, get_user_by_username, create_user

client = TestClient(app)

def user_authentication_headers(username: str, password: str):
    data = {"username": username, "password": password}
    r = client.post("/token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers

def authentication_token_from_username(username: str):
    user = get_user_by_username(username)
    if not user:
        user_in_create = users.UserIn(
            username=username, name="tomek", surname="b",
            email="tomekb", role="user", password="haslo123")
        create_user(user_in_create)
    return user_authentication_headers(username=username, password="haslo123")

@pytest.fixture(scope="module")    
def normal_user_token_headers():
    return  authentication_token_from_username(username="TEST_USERNAME")
    
def test_get_user(normal_user_token_headers):
    u_id = get_max_id()
    user = {
        "id": u_id,
        "username": "tomekb",
        "name": "tomek",
        "surname": "b",
        "email": "tomek@com",
        "role": "user",
        "password": "haslo123"
    }
    fake_users_db.append(user)
    
    response = client.get(f"/user/{u_id}", headers=normal_user_token_headers)
    user_dict = response.json()
    
    assert user_dict["id"] == u_id
    assert user_dict["username"] == "tomekb"
    assert user_dict["name"] == "tomek"
    assert user_dict["surname"] == "b"
    assert user_dict["email"] == "tomek@com"
    assert user_dict["role"] == "user"
    assert user_dict["password"] == "haslo123"
    