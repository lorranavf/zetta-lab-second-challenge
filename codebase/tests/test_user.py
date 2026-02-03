def test_create_user(user):
    assert "id" in user

def test_read_user(client, user):
    user_id = user["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id

def test_update_user(client, user):
    user_id = user["id"]
    response = client.put(f"/users/{user_id}", json={
        "firstname": "updated_user",
    })
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id

def test_delete_user(client, user):
    user_id = user["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404

def test_list_users(client, user):
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data
    assert data["total"] >= 1
    assert isinstance(data["items"], list)

def test_list_projects_by_user_id(client, user):
    user_id = user["id"]
    response = client.get(f"/users/{user_id}/projects")
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data
    assert isinstance(data["items"], list)
    assert data["total"] == 0

def test_read_nonexistent_user(client):
    response = client.get("/users/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404

def test_update_nonexistent_user(client):
    response = client.put("/users/00000000-0000-0000-0000-000000000000", json={
        "firstname": "nonexistent_user",
    })
    assert response.status_code == 404

def test_delete_nonexistent_user(client):
    response = client.delete("/users/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404  


