from datetime import datetime
from sqlalchemy.sql import select

from src.crud.users import get_password_hash
import src.models as models
import src.schemas as schemas
    
def test_get_users(normal_user_token_headers, test_db, client):
    stmt = select(models.User)
    users = test_db.scalars(stmt).all()
    users_serialized = schemas.UserList(users=users)
    
    response = client.get("/users/", headers=normal_user_token_headers)
    
    assert response.status_code == 200
    assert users_serialized == response.json()
    
def test_get_user(normal_user_token_headers, test_db, client):
    username = f'olekniemirka+{datetime.now()}'
    email = f'aaaaaaaaaaa+{datetime.now()}'
    password = get_password_hash("haslo123")
    user = models.User(
        username= username,
        name='olek',
        surname='niemirka',
        email=email,
        hashed_password=password
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    user_id = user.id
    
    response = client.get(f"/users/{user_id}", headers=normal_user_token_headers)
    user_dict = response.json()
    
    assert response.status_code == 200
    assert user_dict["id"] == user_id
    assert user_dict["username"] == username
    assert user_dict["name"] == "olek"
    assert user_dict["surname"] == "niemirka"
    assert user_dict["email"] == email
    assert user_dict["hashed_password"] == password
    
def test_get_user_me(normal_user_token_headers, test_db, client):
    username = f'TEST_USERNAME'
    email = f'tomekb'
    stmt = select(models.User).where(models.User.username == username)
    user = test_db.scalar(stmt)
    user_id = user.id
    hashed_password = user.hashed_password
    
    response = client.get(f"/users/me", headers=normal_user_token_headers)
    user_dict = response.json()
    
    assert response.status_code == 200
    assert user_dict["id"] == user_id
    assert user_dict["username"] == username
    assert user_dict["name"] == "tomek"
    assert user_dict["surname"] == "b"
    assert user_dict["email"] == email
    assert user_dict["hashed_password"] == hashed_password
    
def test_add_user(normal_user_token_headers, test_db, client):
    username = f'olekniemirka+{datetime.now()}'
    email = f'aaaaaaaaaaa+{datetime.now()}'
    user = {
        "username": username,
        "name":'olek',
        "surname":'niemirka',
        "email":email,
        "password":'haslo123'
    }
    
    response = client.post(f"/users/add", headers=normal_user_token_headers, json=user)
    user_dict = response.json()
    
    assert response.status_code == 201
    assert user_dict == {
        "username": username,
        "name":'olek',
        "surname":'niemirka',
        "email":email,
        "password":'haslo123'
    }
    
def test_remove_user(normal_user_token_headers, test_db, client):
    username = f'olekniemirka+{datetime.now()}'
    email = f'aaaaaaaaaaa+{datetime.now()}'
    password = get_password_hash("haslo123")
    user = models.User(
        username= username,
        name='olek',
        surname='niemirka',
        email=email,
        hashed_password=password
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    user_id = user.id
    
    response = client.delete(f"/users/remove/{user_id}", headers=normal_user_token_headers)
    
    assert response.status_code == 202
    assert response.json() == {'message': 'User was succesfully removed.'}
    stmt = select(models.User).where(models.User.id == user_id)
    assert test_db.scalar(stmt) == None # get user by id == None
    
    
