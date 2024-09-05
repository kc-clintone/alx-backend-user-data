#!/usr/bin/env python3
"""Authenticating sessions
"""
import os
from typing import Tuple
from flask import abort, jsonify, request
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    """POST:
             /api/v1/auth_session/login
    Return:
      - JSON repr of a User object.
    """
    res_404 = {"error": "no user found for this email"}
    email = request.form.get('email')
    if email is None or len(email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        usrs = User.search({'email': email})
    except Exception:
        return jsonify(res_404), 404
    if len(usrs) <= 0:
        return jsonify(res_404), 404
    if usrs[0].is_valid_password(password):
        from api.v1.app import auth
        sessiond_ID = auth.create_session(getattr(usrs[0], 'id'))
        response = jsonify(usrs[0].to_json())
        response.set_cookie(os.getenv("SESSION_NAME"), sessiond_ID)
        return response
    return jsonify({"error": "wrong password"}), 401

@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    """DELETE:
              /api/v1/auth_session/logout
    Return:
      - An empty JSON object.
    """
    from api.v1.app import auth
    is_deleted = auth.destroy_session(request)
    if not is_deleted:
        abort(404)
    return jsonify({})
