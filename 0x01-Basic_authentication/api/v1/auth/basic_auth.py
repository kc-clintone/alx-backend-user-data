#!/usr/bin/env python3
"""Basic Auth module
"""
import base64
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """ Attributes and methods for basic auth
        inherits from Auth
    Args:
        Auth (class): Parent auth class
    """

    def extract_base64_authorization_header(self, authorization_header: str
            ) -> str:
        """Returns:
                  Base64 Auth header
        Args:
            authorization_header (str): auth_header
        Returns:
            str: base64 string
        """
        if not (authorization_header and isinstance(authorization_header, str)
                and authorization_header.startswith('Basic ')):
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                          ) -> str:
        """Returns:
                 Decoded Base64 string
        Args:
            base64_authorization_header (str): base64 auth header
        Returns:
            str: Decoded Base64 string
        """
        if not (base64_authorization_header and
                isinstance(base64_authorization_header, str)):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except BaseException:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                ) -> Tuple[str, str]:
        """Extracts:
                User's email and password from the B64 value.
        Args:
            self (obj): Basic Auth instance
            decoded_base64_authorization_header (str): auth header
        """
        if not (decoded_base64_authorization_header and
                isinstance(decoded_base64_authorization_header, str) and
                ':' in decoded_base64_authorization_header):
            return None, None

        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email: str,
             user_pwd: str) -> TypeVar('User'):
        """Returns:
               User instance based on extracted email and password.
        Args:
            self (_type_): Basic auth instance
            user_email(str): user email
            user_pwd(str): user pwd
        """
        if not (user_email and isinstance(user_email, str) and
                user_pwd and isinstance(user_pwd, str)):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for usr in users:
            if usr.is_valid_password(user_pwd):
                return usr

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve current user"""
        try:
            auth_header = self.authorization_header(request)
            B64 = self.extract_base64_authorization_header(auth_header)
            D64 = self.decode_base64_authorization_header(B64)
            email, password = self.extract_user_credentials(D64)
            return self.user_object_from_credentials(email, password)
        except Exception:
            return None
