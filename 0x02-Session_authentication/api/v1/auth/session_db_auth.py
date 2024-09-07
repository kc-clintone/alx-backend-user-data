#!/usr/bin/env python3
"""Session auth with expiration module.
"""
from flask import request
from datetime import datetime, timedelta
from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Session authentication class.
    """

    def create_session(self, user_id=None) -> str:
        """Creating and storing session_ids.
        """
        session_id = super().create_session(user_id)
        if type(session_id) == str:
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
            usr_session = UserSession(**kwargs)
            usr_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieving a user based on session id
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        curent_time = datetime.now()
        ses_duration = timedelta(seconds=self.session_duration)
        expiration_time = sessions[0].created_at + ses_duration
        if expiration_time < current_time:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """Destroying an authenticated session.
        """
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
