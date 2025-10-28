from flask import Blueprint, jsonify, request
from app import db
from app.comments.models import Task

tasks_bp = Blueprint("tasks_bp", __name__)

# GET all tasks
@tasks_bp.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([t.to_dict() for t in tasks])

# POST create a task
@tasks_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    if not title:
        return jsonify({"error": "Title is required"}), 400

    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

# PUT update a task
@tasks_bp.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    db.session.commit()
    return jsonify(task.to_dict())

# DELETE a task
@tasks_bp.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"})
