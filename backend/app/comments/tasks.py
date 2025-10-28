# backend/app/comments/tasks.py
from flask import Blueprint, request, jsonify
from app import db
from app.comments.models import Task

tasks_bp = Blueprint("tasks_bp", __name__)

# Get all tasks
@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

# Create a task
@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description", "")
    if not title:
        return jsonify({"error": "Title is required"}), 400

    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

# Update a task
@tasks_bp.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.get_json()
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    db.session.commit()
    return jsonify(task.to_dict())

# Delete a task
@tasks_bp.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})
