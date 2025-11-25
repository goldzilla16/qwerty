"""
Comprehensive unit tests for Flask Task Management API
Tests all endpoints with various scenarios and edge cases
Coverage target: >85%
"""

import pytest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.app import app as flask_app


@pytest.fixture
def app():
    """Create and configure test app"""
    flask_app.config['TESTING'] = True
    yield flask_app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create CLI runner"""
    return app.test_cli_runner()


class TestHomeAndHealth:
    """Tests for home and health endpoints"""

    def test_home_endpoint_returns_200(self, client):
        """Test home endpoint returns 200 status"""
        response = client.get('/')
        assert response.status_code == 200

    def test_home_endpoint_has_required_fields(self, client):
        """Test home endpoint returns required fields"""
        response = client.get('/')
        data = json.loads(response.data)
        assert 'name' in data
        assert 'version' in data
        assert 'endpoints' in data

    def test_home_endpoint_version(self, client):
        """Test home endpoint has correct version"""
        response = client.get('/')
        data = json.loads(response.data)
        assert data['version'] == '1.0.0'

    def test_health_check_returns_200(self, client):
        """Test health check returns 200"""
        response = client.get('/health')
        assert response.status_code == 200

    def test_health_check_has_status(self, client):
        """Test health check returns status"""
        response = client.get('/health')
        data = json.loads(response.data)
        assert data['status'] == 'healthy'

    def test_health_check_has_timestamp(self, client):
        """Test health check returns timestamp"""
        response = client.get('/health')
        data = json.loads(response.data)
        assert 'timestamp' in data


class TestGetTasks:
    """Tests for getting tasks"""

    def test_get_all_tasks_returns_200(self, client):
        """Test getting all tasks returns 200"""
        response = client.get('/api/tasks')
        assert response.status_code == 200

    def test_get_all_tasks_returns_list(self, client):
        """Test getting all tasks returns a list"""
        response = client.get('/api/tasks')
        data = json.loads(response.data)
        assert 'tasks' in data
        assert isinstance(data['tasks'], list)

    def test_get_all_tasks_returns_count(self, client):
        """Test getting all tasks includes count"""
        response = client.get('/api/tasks')
        data = json.loads(response.data)
        assert 'count' in data
        assert data['count'] > 0

    def test_get_specific_task_returns_200(self, client):
        """Test getting specific task returns 200"""
        response = client.get('/api/tasks/1')
        assert response.status_code == 200

    def test_get_specific_task_has_data(self, client):
        """Test specific task has required fields"""
        response = client.get('/api/tasks/1')
        data = json.loads(response.data)
        task = data['task']
        assert task['id'] == 1
        assert 'title' in task
        assert 'description' in task
        assert 'completed' in task
        assert 'created_at' in task

    def test_get_nonexistent_task_returns_404(self, client):
        """Test getting nonexistent task returns 404"""
        response = client.get('/api/tasks/9999')
        assert response.status_code == 404

    def test_get_nonexistent_task_has_error(self, client):
        """Test nonexistent task error message"""
        response = client.get('/api/tasks/9999')
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Task not found'

    def test_get_task_with_string_id_returns_404(self, client):
        """Test getting task with string ID"""
        response = client.get('/api/tasks/invalid')
        assert response.status_code == 404


class TestCreateTask:
    """Tests for creating tasks"""

    def test_create_task_with_title_returns_201(self, client):
        """Test creating task with title returns 201"""
        response = client.post('/api/tasks',
                              data=json.dumps({'title': 'New Task'}),
                              content_type='application/json')
        assert response.status_code == 201

    def test_create_task_returns_task_object(self, client):
        """Test created task has all fields"""
        response = client.post('/api/tasks',
                              data=json.dumps({'title': 'New Task'}),
                              content_type='application/json')
        data = json.loads(response.data)
        task = data['task']
        assert 'id' in task
        assert task['title'] == 'New Task'
        assert 'completed' in task
        assert 'created_at' in task

    def test_create_task_with_description(self, client):
        """Test creating task with description"""
        response = client.post('/api/tasks',
                              data=json.dumps({
                                  'title': 'Task',
                                  'description': 'Description'
                              }),
                              content_type='application/json')
        data = json.loads(response.data)
        assert data['task']['description'] == 'Description'

    def test_create_task_with_completed_status(self, client):
        """Test creating task with completed status"""
        response = client.post('/api/tasks',
                              data=json.dumps({
                                  'title': 'Task',
                                  'completed': True
                              }),
                              content_type='application/json')
        data = json.loads(response.data)
        assert data['task']['completed'] is True

    def test_create_task_without_title_returns_400(self, client):
        """Test creating task without title returns 400"""
        response = client.post('/api/tasks',
                              data=json.dumps({}),
                              content_type='application/json')
        assert response.status_code == 400

    def test_create_task_with_empty_title_returns_400(self, client):
        """Test creating task with empty title returns 400"""
        response = client.post('/api/tasks',
                              data=json.dumps({'title': ''}),
                              content_type='application/json')
        assert response.status_code == 400

    def test_create_task_without_body_returns_400(self, client):
        """Test creating task without request body returns 400"""
        response = client.post('/api/tasks',
                              content_type='application/json')
        assert response.status_code == 400

    def test_create_task_without_content_type_returns_415(self, client):
        """Test creating task without content type returns 415"""
        response = client.post('/api/tasks',
                              data='{"title": "Task"}')
        assert response.status_code == 415  # Unsupported Media Type

    def test_create_multiple_tasks(self, client):
        """Test creating multiple tasks"""
        for i in range(3):
            response = client.post('/api/tasks',
                                  data=json.dumps({'title': f'Task {i}'}),
                                  content_type='application/json')
            assert response.status_code == 201

    def test_created_tasks_have_unique_ids(self, client):
        """Test created tasks have unique IDs"""
        ids = []
        for i in range(3):
            response = client.post('/api/tasks',
                                  data=json.dumps({'title': f'Task {i}'}),
                                  content_type='application/json')
            data = json.loads(response.data)
            ids.append(data['task']['id'])
        assert len(ids) == len(set(ids))


class TestUpdateTask:
    """Tests for updating tasks"""

    def test_update_task_title_returns_200(self, client):
        """Test updating task title returns 200"""
        response = client.put('/api/tasks/1',
                             data=json.dumps({'title': 'Updated Title'}),
                             content_type='application/json')
        assert response.status_code == 200

    def test_update_task_title_changes_value(self, client):
        """Test updating task title actually changes it"""
        client.put('/api/tasks/1',
                  data=json.dumps({'title': 'Updated Title'}),
                  content_type='application/json')
        response = client.get('/api/tasks/1')
        data = json.loads(response.data)
        assert data['task']['title'] == 'Updated Title'

    def test_update_task_completed_status(self, client):
        """Test updating task completed status"""
        response = client.put('/api/tasks/1',
                             data=json.dumps({'completed': True}),
                             content_type='application/json')
        data = json.loads(response.data)
        assert data['task']['completed'] is True

    def test_update_task_description(self, client):
        """Test updating task description"""
        response = client.put('/api/tasks/1',
                             data=json.dumps({'description': 'New description'}),
                             content_type='application/json')
        data = json.loads(response.data)
        assert data['task']['description'] == 'New description'

    def test_update_nonexistent_task_returns_404(self, client):
        """Test updating nonexistent task returns 404"""
        response = client.put('/api/tasks/9999',
                             data=json.dumps({'title': 'New Title'}),
                             content_type='application/json')
        assert response.status_code == 404

    def test_update_task_with_empty_title_returns_400(self, client):
        """Test updating task with empty title returns 400"""
        response = client.put('/api/tasks/1',
                             data=json.dumps({'title': ''}),
                             content_type='application/json')
        assert response.status_code == 400

    def test_update_task_with_invalid_completed_returns_400(self, client):
        """Test updating with invalid completed value returns 400"""
        response = client.put('/api/tasks/1',
                             data=json.dumps({'completed': 'yes'}),
                             content_type='application/json')
        assert response.status_code == 400

    def test_update_task_without_body_returns_400(self, client):
        """Test updating task without body returns 400"""
        response = client.put('/api/tasks/1',
                             content_type='application/json')
        assert response.status_code == 400

    def test_update_multiple_fields(self, client):
        """Test updating multiple fields at once"""
        response = client.put('/api/tasks/1',
                             data=json.dumps({
                                 'title': 'New Title',
                                 'description': 'New Description',
                                 'completed': True
                             }),
                             content_type='application/json')
        data = json.loads(response.data)
        assert data['task']['title'] == 'New Title'
        assert data['task']['description'] == 'New Description'
        assert data['task']['completed'] is True


class TestDeleteTask:
    """Tests for deleting tasks"""

    def test_delete_task_returns_200(self, client):
        """Test deleting task returns 200"""
        response = client.delete('/api/tasks/1')
        assert response.status_code == 200

    def test_delete_task_returns_correct_response(self, client):
        """Test delete response structure"""
        response = client.delete('/api/tasks/1')
        data = json.loads(response.data)
        assert 'status' in data
        assert data['status'] == 'deleted'

    def test_delete_nonexistent_task_returns_404(self, client):
        """Test deleting nonexistent task returns 404"""
        response = client.delete('/api/tasks/9999')
        assert response.status_code == 404

    def test_delete_task_removes_it(self, client):
        """Test deleted task is removed"""
        client.delete('/api/tasks/1')
        response = client.get('/api/tasks/1')
        assert response.status_code == 404

    def test_delete_task_once(self, client):
        """Test deleting a single task works"""
        # First create a task
        create_response = client.post('/api/tasks',
                                     data=json.dumps({'title': 'Task to delete'}),
                                     content_type='application/json')
        task_id = json.loads(create_response.data)['task']['id']
        
        # Now delete it
        response = client.delete(f'/api/tasks/{task_id}')
        assert response.status_code == 200
        
        # Verify it's deleted
        get_response = client.get(f'/api/tasks/{task_id}')
        assert get_response.status_code == 404


class TestErrorHandling:
    """Tests for error handling"""

    def test_nonexistent_endpoint_returns_404(self, client):
        """Test accessing nonexistent endpoint returns 404"""
        response = client.get('/api/nonexistent')
        assert response.status_code == 404

    def test_404_error_has_message(self, client):
        """Test 404 error has message"""
        response = client.get('/api/nonexistent')
        data = json.loads(response.data)
        assert 'error' in data
