from flask import Blueprint, jsonify

# Create a blueprint
main = Blueprint('main', __name__)

# Define a route for the home page
@main.route('/')
def home():
    return jsonify({"message": "Flask backend is running successfully!"})
