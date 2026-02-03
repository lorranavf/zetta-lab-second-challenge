def test_create_task(task):
    assert "id" in task

def test_read_task(client, task):
    task_id = task['id']
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == task_id

def test_update_task(client, task):
    task_id = task['id']
    response = client.put(f'/tasks/{task_id}', json={
        'title': 'Updated task Title',
        'description': 'Updated description'
    })
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id

def test_delete_task(client, task):
    task_id = task['id']
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 204


def test_read_nonexistent_task(client):
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    response = client.get(f'/tasks/{non_existent_id}')
    assert response.status_code == 404

def test_update_nonexistent_task(client):
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    response = client.put(f'/tasks/{non_existent_id}', json={
        'title': 'Should Not Work',
        'description': 'This task does not exist'
    })
    assert response.status_code == 404

def test_delete_nonexistent_task(client):
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    response = client.delete(f'/tasks/{non_existent_id}')
    assert response.status_code == 404
    