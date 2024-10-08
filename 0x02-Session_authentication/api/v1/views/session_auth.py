#!/usr/bin/env python3
"""Session authenticating views.
"""
import os
from typing import Tuple
from flask import abort, jsonify, request
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """
    Logging in users
    POST /api/v1/auth_session/login
    Return:
      - Returns a JSON representation of a User object.
    """
    res_nf = {"error": "no user found for this email"}
    email = request.form.get('email')
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify(res_nf), 404
    if len(users) <= 0:
        return jsonify(res_nf), 404
    if users[0].is_valid_password(password):
        from api.v1.app import auth
        sessiond_id = auth.create_session(getattr(users[0], 'id'))
        response = jsonify(users[0].to_json())
        response.set_cookie(os.getenv("SESSION_NAME"), sessiond_id)
        return response
    return jsonify({"error": "wrong password"}), 401

@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """
    Logging out users
    DELETE /api/v1/auth_session/logout
    Return:
      - Returns an empty JSON object.
    """
    from api.v1.app import auth
    session_destroyed = auth.destroy_session(request)
    if not session_destroyed:
        abort(404)
    return jsonify({})
