from functools import wraps
from flask import request, jsonify
import jwt
import os
from datetime import datetime, timedelta
import yaml

# Load configuration
with open("config/config.yaml", "r") as f:
    config = yaml.safe_load(f)

def generate_token(user_id: str) -> str:
    """Generate a JWT token for the user"""
    expiry = datetime.utcnow() + timedelta(seconds=config["security"]["token_expiry"])
    payload = {
        "user_id": user_id,
        "exp": expiry
    }
    return jwt.encode(
        payload,
        os.getenv("JWT_SECRET_KEY", config["security"]["jwt_secret_key"]),
        algorithm="HS256"
    )

def require_auth(f):
    """Decorator to require authentication for routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check if token is in headers
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({"error": "Invalid token format"}), 401

        if not token:
            return jsonify({"error": "Missing authentication token"}), 401

        try:
            # Verify token
            jwt.decode(
                token,
                os.getenv("JWT_SECRET_KEY", config["security"]["jwt_secret_key"]),
                algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated 