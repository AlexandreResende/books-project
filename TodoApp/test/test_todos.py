from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from pytest import fixture
from fastapi.testclient import TestClient
from fastapi import status

from Auth.authService import get_current_user
from database import Base, get_db

from main import app
from models import Todos

# create a test database in the following path
SQLALCHEMY_DATABASE_URL = 'sqlite:///./testdb.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return { 'username': 'johndoe', 'roles': 'developer', 'id': 1 }

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

client = TestClient(app)

@fixture
def test_todo():
    todo = Todos(
        title='Learn to code',
        description='Need to learn everyday',
        priority=1,
        completed=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()

    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()

def test_read_all_authenticated(test_todo):
    response = client.get('/todos')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'todos': [
            { 'title': 'Learn to code', 'description': 'Need to learn everyday', 'priority': 1, 'completed': False, 'owner_id': 1, 'id': 1 }
        ]
    }

def test_read_one_authenticated(test_todo):
    response = client.get('/todos/1')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == { 'title': 'Learn to code', 'description': 'Need to learn everyday', 'priority': 1, 'completed': False, 'owner_id': 1, 'id': 1 }

def test_read_one_authenticated_not_found(test_todo):
    response = client.get('/todos/2')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        'detail': 'Todo not found'
    }

def test_create_authenticated(test_todo):
    request_data = {
        'title': 'Learn to code',
        'description': 'Need to learn everyday',
        'priority': 1,
        'completed': False,
    }
    response = client.post('/todos', json=request_data)

    assert response.status_code == status.HTTP_201_CREATED

    # testing if the record is in the DB
    # db = TestingSessionLocal()
    # model = db.query(Todos).filter(Todos.id == 2).first()
    # assert model.title == 'Learn to code'

def test_create_authenticated_with_invalid_data(test_todo):
    request_data = {
        'title': 'Learn to code',
        'description': 'Need to learn everyday',
        'priority': 10,
        'completed': False,
    }
    response = client.post('/todos', json=request_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

def test_update_authenticated_with_valid_data(test_todo):
    request_data = {
        'title': 'Learn to code with projects',
    }
    response = client.put('/todos/1', json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_update_authenticated_not_found(test_todo):
    request_data = {
        'title': 'Learn to code with projects',
    }
    response = client.put('/todos/2', json=request_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == { 'detail': 'Record not found' }

def test_update_authenticated_with_invalid_data(test_todo):
    request_data = {
        'priority': 10
    }
    response = client.put('/todos/1', json=request_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT