from flask import Blueprint, request, jsonify, make_response
from models import User, db

user_bp = Blueprint('user', __name__)


def authenticate(email, password):
    """Check if the provided credentials are valid."""
    user = User.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None

@user_bp.route('/users', methods=['POST'])
def register():
    data = request.get_json()
    
    # Add validation for required fields
    if not data or 'email' not in data or 'password' not in data or 'name' not in data:
        return jsonify({"message": "Missing required fields"}), 400
    
    # Check for existing user
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "User already exists."}), 409  # More appropriate status code
    
    try:
        new_user = User(name=data['name'], email=data['email'])
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    user = authenticate(data['email'], data['password'])
    
    if user:
        return jsonify({"message": f"Welcome {user.name}!"}), 200
    
    return jsonify({"message": "Invalid credentials"}), 401


@user_bp.route('/profile', methods=['GET'])
def profile():
    #! For simplicity, we will not implement session management here.
    return jsonify({"message": "Please log in to view your profile."}), 401


@user_bp.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    
    return jsonify([{
        "id": user.user_id,
        "name": user.name,
        "email": user.email,
        "projects_count": len(user.projects),
        "tasks_count": len(user.tasks),
     } for user in users]), 200


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({"message": "User deleted successfully"}), 200
