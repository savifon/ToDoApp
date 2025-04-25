from fastapi import status

from .utils import *
from routers.todos import get_db, get_current_user

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_read_all_authenticated(test_todo):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data[0]["title"] == "Learn to code!"

def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["title"] == "Learn to code!"

def test_read_one_authenticated_not_found():
    response = client.get("/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'ToDo not found.'}

def test_create_todo(test_todo):
    request_data={
        'title': 'New Todo!',
        'description': 'New todo description',
        'priority': 5,
        'complete': False
    }
    response = client.post('/todo/', json=request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(ToDos).filter(ToDos.id == 2).first()
    assert model.title == request_data.get('title')