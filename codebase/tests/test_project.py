def test_create_project(project):
    assert "id" in project

def test_read_project(client, project):
    project_id = project['id']
    response = client.get(f'/projects/{project_id}')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == project_id

def test_update_project(client, project):
    project_id = project['id']
    response = client.put(f'/projects/{project_id}', json={
        'title': 'Updated Project Title',
        'description': 'Updated description'
    })
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == project_id

def test_delete_project(client, project):
    project_id = project['id']
    response = client.delete(f'/projects/{project_id}')
    assert response.status_code == 204

def test_list_tasks_by_project_id(client, project):
    project_id = project['id']
    response = client.get(f'/projects/{project_id}/tasks')
    assert response.status_code == 200
    data = response.json()
    assert "total" in data
    assert "items" in data
    assert data["total"] == 0


def test_read_nonexistent_project(client):
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f'/projects/{non_existent_id}')
    assert response.status_code == 404

def test_update_nonexistent_project(client):
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    response = client.put(f'/projects/{non_existent_id}', json={
        'title': 'Should Not Work',
        'description': 'This project does not exist'
    })
    assert response.status_code == 404

def test_delete_nonexistent_project(client):
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f'/projects/{non_existent_id}')
    assert response.status_code == 404

# def test_list_tasks_by_nonexistent_project_id(client):
#     non_existent_id = "00000000-0000-0000-0000-000000000000"
#     response = client.get(f'/projects/{non_existent_id}/tasks')
#     assert response.status_code == 200
#     data = response.json()
#     assert data == []
    