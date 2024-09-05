#!/usr/bin/env python3
"""
Auth class
"""

from typing import List, TypeVar
from flask import Flask, request


class Auth:
    """Authentication class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Required authentication
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        if path[-1] == '/':
            path = path[:-1]

        has_slash = False
        for ex_path in excluded_paths:
            if ex_path[-1] == '/':
                ex_path = ex_path[:-1]
                has_slash = True

            if ex_path.endswith('*'):
                last_index = ex_path.rfind('/') + 1
                ex_paths = ex_path[last_index:-1]

                last_index = path.rfind('/') + 1
                temp = path[last_index:]

                if ex_paths in temp:
                    return False

            if has_slash:
                hass_slash = False

        path += '/'

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """Header for the authentication
        """
        if request is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user method
        """
        request = Flask(__name__)
        return None
