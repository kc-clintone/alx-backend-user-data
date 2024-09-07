#!/usr/bin/env python3
"""Authentication module for the API.
"""
import os
import re
from typing import List, TypeVar
from flask import request


class Auth:
    """Class for authentication.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """This function checks if a path requires authentication.
        """
        if path is not None and excluded_paths is not None:
            for ex_path in map(lambda cb: cb.strip(), excluded_paths):
                pattern = ''
                if ex_path[-1] == '*':
                    pattern = '{}.*'.format(ex_path[0:-1])
                elif ex_path[-1] == '/':
                    pattern = '{}/*'.format(ex_path[0:-1])
                else:
                    pattern = '{}/*'.format(ex_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Retrieve authorization header from request.
        """
        if request is not None:
            return request.headers.get('Authorization', None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve current user from request.
        """
        return None

    def session_cookie(self, request=None) -> str:
        """Get cookies => named SESSION_NAME.
        """
        if request is not None:
            cookie_name = os.getenv('SESSION_NAME')
            return request.cookies.get(cookie_name)
