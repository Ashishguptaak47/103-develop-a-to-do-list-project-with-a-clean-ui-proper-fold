import pytest
from main import app, todos

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Reset state before each test
        global todos, next_id
        todos.clear()
        todos.extend([
            {"id": 1, "title": "Test Task 1", "completed": False}
        ])
        yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Test Task 1' in response.data

def test_add_todo(client):
    response = client.post('/add', data={"title": "New Integration Test Task"}, follow_redirects=True)
    assert response.status_code == 200
    assert b'New Integration Test Task' in response.data

def test_toggle_todo(client):
    response = client.post('/toggle/1')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert json_data['completed'] is True

def test_delete_todo(client):
    response = client.post('/delete/1', follow_redirects=True)
    assert response.status_code == 200
    assert b'Test Task 1' not in response.data
