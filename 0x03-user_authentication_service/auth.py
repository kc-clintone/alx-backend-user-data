#!/usr/bin/env python3
"""Authentication-related routines.
"""
import bcrypt
from uuid import uuid4
from typing import Union
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashing the given password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generating a new UUID.
    """
    return str(uuid4())


class Auth:
    """This class will communicate with the auth database.
    """

    def __init__(self):
        """Creating a new Auth instance.
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """creating and adding new user to the database.
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Login validation and verification
        """
        usr = None
        try:
            usr = self._db.find_user_by(email=email)
            if usr is not None:
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    user.hashed_password,
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """New user new session - creating sessions.
        """
        usr = None
        try:
            usr = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if usr is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(usr.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Getting a user based on session ID.
        """
        usr = None
        if session_id is None:
            return None
        try:
            usr = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return usr

    def destroy_session(self, user_id: int) -> None:
        """Destroying user sessions.
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Password reset token.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        token = _generate_uuid()
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updating user password.
        """
        usr = None
        try:
            usr = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            usr = None
        if usr is None:
            raise ValueError()
        new_pwd_hash = _hash_password(password)
        self._db.update_user(
            usr.id,
            hashed_password=new_pwd_hash,
            reset_token=None,
        )
