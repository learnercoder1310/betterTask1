# backend/app/__init__.py
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # ✅ enable cross-origin requests

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_DATABASE_URI="sqlite:///app.db"
    )

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    # Enable CORS for all routes
    CORS(app)  # ✅

    with app.app_context():
        # Import models
        from app.comments.models import Task, Comment

        # Import blueprints
        from app.comments.routes import comments_bp  # ✅ existing
        from app.comments.tasks_routes import tasks_bp  # ✅ fixed import

        # Create tables
        db.create_all()

        # Register blueprints
        app.register_blueprint(comments_bp, url_prefix="/api")
        app.register_blueprint(tasks_bp, url_prefix="/api")

    @app.route("/")
    def home():
        return jsonify({"message": "Flask backend is running successfully!"})

    return app






