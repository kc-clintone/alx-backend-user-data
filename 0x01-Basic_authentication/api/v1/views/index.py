#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route("/unauthorized/", strict_slashes=False)
def unauthorized() -> str:
    """Route for unauthorized requests

    Returns:
        str: A 401 status code (unauthorized)
    """
    abort(401)


@app_views.route("/forbidden/",
                 strict_slashes=False)
def forbidden() -> str:
    """Route for forbidden requests (403)

    Returns:
        str: A 403 status code (Forbidden)
    """
    abort(403)


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)
