# backend/app/comments/routes.py
from flask import Blueprint, request, jsonify
from app import db
from app.comments.models import Comment, Task

comments_bp = Blueprint("comments", __name__)

# 🟩 CREATE Comment
@comments_bp.route("/comments", methods=["POST"])
def add_comment():
    data = request.get_json()
    task_id = data.get("task_id")
    content = data.get("content")

    if not task_id or not content:
        return jsonify({"error": "task_id and content are required"}), 400

    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    comment = Comment(content=content, task_id=task_id)
    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.to_dict()), 201


# 🟨 READ Comments for a Task
@comments_bp.route("/comments/<int:task_id>", methods=["GET"])
def get_comments(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    comments = Comment.query.filter_by(task_id=task_id).all()
    return jsonify([c.to_dict() for c in comments]), 200


# 🟦 UPDATE Comment
@comments_bp.route("/comments/<int:comment_id>", methods=["PUT"])
def update_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    data = request.get_json()
    content = data.get("content")
    if not content:
        return jsonify({"error": "content is required"}), 400

    comment.content = content
    db.session.commit()
    return jsonify(comment.to_dict()), 200


# 🟥 DELETE Comment
@comments_bp.route("/comments/<int:comment_id>", methods=["DELETE"])
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    db.session.delete(comment)
    db.session.commit()
    return jsonify({"message": "Comment deleted successfully"}), 200
