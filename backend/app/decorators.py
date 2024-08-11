from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from app.models.user import User

def is_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        id = get_jwt_identity()
        current_user = User.query.filter_by(id=id).first()
        if current_user.status != 'admin':
            return jsonify({"status": "error", "message": "Page introuvable"}), 404
        return func(*args, **kwargs) 
    return decorated_function

def is_moderator(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        id = get_jwt_identity()
        current_user = User.query.filter_by(id=id).first()
        if current_user.status != 'moderator' and current_user.status != 'admin':
            return jsonify({"status": "error", "message": "Page introuvable"}), 404
        return func(*args, **kwargs) 
    return decorated_function