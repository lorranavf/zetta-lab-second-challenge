import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.app import app  
from app.clients.database import PostgresClient
from app.services.security import SecurityService 


URL = os.getenv("DATABASE_URL")

@pytest.fixture(scope="session")
def engine():
    return create_engine(URL, connect_args={"client_encoding":"utf8"})

@pytest.fixture(scope="session", autouse=True)
def setup_database(engine):
    Base = PostgresClient.base()
    Base.metadata.create_all(bind=engine)
    yield

@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = local(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db_session):

    def _get_db_session_(): yield db_session

    app.dependency_overrides[PostgresClient.db] = _get_db_session_
    
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def user(client):
    response = client.post('/users', json={
        'firstname': 'user',
        'lastname': 'test',
        'email': 'testuser@example.com',
        'password': 'securepassword'
    })
    return response.json()

@pytest.fixture(scope="function")
def another_user(client):
    response = client.post('/users', json={
        'firstname': 'another',
        'lastname': 'user',
        'email': 'anotheruser@example.com',
        'password': 'securepassword'
    })
    return response.json()

@pytest.fixture(scope="function")
def project(client, user):
    response = client.post('/projects', json={
        'title': 'Test Project',
        'description': 'This is a test project',
        'user_id': user['id']
    })
    return response.json()

@pytest.fixture(scope="function")
def task(client, project):
    response = client.post('/tasks', json={
        'title': 'Test Task',
        'description': 'This is a test task',
        'project_id': project['id']
    })
    return response.json()



@pytest.fixture(scope="function")
def user_token(user):
    access_token = SecurityService.create_access_token(data={"sub": user["id"]})
    return access_token


@pytest.fixture(scope="function")
def auth_client(client, user_token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {user_token}"
    }
    return client

@pytest.fixture(scope="function")
def user_credentials():
    return {
        'email': 'testuser@example.com',
        'password': 'securepassword'
    }