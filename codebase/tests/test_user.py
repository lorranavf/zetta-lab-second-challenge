from app.services.security import SecurityService

def test_create_user(user):
    assert "id" in user

def test_read_user(auth_client, user):
    user_id = user["id"]
    response = auth_client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id

def test_update_user(auth_client, user):
    user_id = user["id"]
    response = auth_client.put(f"/users/{user_id}", json={
        "firstname": "updated_user",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id

def test_delete_user(auth_client, user):
    user_id = user["id"]
    response = auth_client.delete(f"/users/{user_id}")
    assert response.status_code == 204


def test_list_users(auth_client):
    response = auth_client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data
    assert data["total"] >= 1
    assert isinstance(data["items"], list)

def test_list_projects_by_user_id(auth_client, user):
    user_id = user["id"]
    response = auth_client.get(f"/users/{user_id}/projects")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data
    assert isinstance(data["items"], list)
    assert data["total"] == 0

def test_read_nonexistent_user(auth_client):
    response = auth_client.get("/users/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404

def test_update_nonexistent_user(auth_client):
    response = auth_client.put("/users/00000000-0000-0000-0000-000000000000", json={
        "firstname": "nonexistent_user",
    })
    assert response.status_code == 404

def test_delete_nonexistent_user(auth_client):
    response = auth_client.delete("/users/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404  


def test_user_crud_hashes_password_manually(db_session):
    from app.crud import user 
    from app.schemas import UserUpdate
    
    password_bruta = 'secret_password_123'

    data = {
        'firstname': 'Hook',
        'lastname': 'Test',
        'email': 'hook@test.com',
        'password': password_bruta
    }

    raw_data = UserUpdate(**data).model_dump()
    
    processed_data = user.before_update(raw_data)
    
    assert processed_data['password'] != password_bruta
    
    assert SecurityService.verify_password(
        plain_password=password_bruta, 
        hashed_password=processed_data['password']
    )

def test_user_trying_to_update_another_user(auth_client, another_user):
    user_id = another_user["id"]
    response = auth_client.put(f"/users/{user_id}", json={
        'firstname': 'Other',
        'lastname': 'User',
        'email': 'other.user@example.com',
        'password': 'otherpassword123'
    })
    assert response.status_code == 404
