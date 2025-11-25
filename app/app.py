"""
Flask Task Management API
A simple REST API for managing tasks
"""

from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# In-memory task storage (for demo; use database in production)
tasks = [
    {
        "id": 1,
        "title": "Setup CI/CD Pipeline",
        "description": "Configure GitHub Actions",
        "completed": False,
        "created_at": "2024-01-15T10:00:00Z"
    },
    {
        "id": 2,
        "title": "Write Unit Tests",
        "description": "Create comprehensive test suite",
        "completed": False,
        "created_at": "2024-01-15T11:00:00Z"
    }
]

task_counter = 3


@app.route('/')
def home():
    """Home endpoint - API information"""
    return jsonify({
        "name": "Task Management API",
        "version": "1.0.0",
        "description": "REST API for managing tasks",
        "endpoints": {
            "GET /": "API information",
            "GET /health": "Health check",
            "GET /api/tasks": "List all tasks",
            "GET /api/tasks/<id>": "Get specific task",
            "POST /api/tasks": "Create new task",
            "PUT /api/tasks/<id>": "Update task",
            "DELETE /api/tasks/<id>": "Delete task"
        }
    }), 200


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }), 200


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks"""
    return jsonify({
        "tasks": tasks,
        "count": len(tasks),
        "status": "success"
    }), 200


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by ID"""
    task = next((t for t in tasks if t['id'] == task_id), None)

    if not task:
        return jsonify({
            "error": "Task not found",
            "task_id": task_id
        }), 404

    return jsonify({
        "task": task,
        "status": "success"
    }), 200


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task"""
    global task_counter

    data = request.get_json()

    # Validation
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    if 'title' not in data or not data['title']:
        return jsonify({"error": "Title is required"}), 400

    if len(data['title']) < 1:
        return jsonify({"error": "Title cannot be empty"}), 400

    new_task = {
        "id": task_counter,
        "title": data['title'],
        "description": data.get('description', ''),
        "completed": data.get('completed', False),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    tasks.append(new_task)
    task_counter += 1

    return jsonify({
        "task": new_task,
        "status": "created"
    }), 201


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task"""
    task = next((t for t in tasks if t['id'] == task_id), None)

    if not task:
        return jsonify({
            "error": "Task not found",
            "task_id": task_id
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    # Update fields if provided
    if 'title' in data:
        if not data['title']:
            return jsonify({"error": "Title cannot be empty"}), 400
        task['title'] = data['title']

    if 'description' in data:
        task['description'] = data['description']

    if 'completed' in data:
        if not isinstance(data['completed'], bool):
            return jsonify({"error": "Completed must be a boolean"}), 400
        task['completed'] = data['completed']

    return jsonify({
        "task": task,
        "status": "updated"
    }), 200


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    global tasks

    task = next((t for t in tasks if t['id'] == task_id), None)

    if not task:
        return jsonify({
            "error": "Task not found",
            "task_id": task_id
        }), 404

    tasks = [t for t in tasks if t['id'] != task_id]

    return jsonify({
        "message": "Task deleted successfully",
        "task_id": task_id,
        "status": "deleted"
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "message": "The requested endpoint does not exist"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
