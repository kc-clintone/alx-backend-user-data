#!/usr/bin/env python3
"""Session auth module.
"""
import os
from flask import request
from datetime import datetime, timedelta
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session auth class (with expiration).
    """

    def __init__(self) -> None:
        """Initializing a new SessionExpAuth instance.
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Creating a session id for user.
        """
        session_id = super().create_session(user_id)
        if type(session_id) != str:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """Retrieving users based on sessi9n id.
        """
        if session_id in self.user_id_by_session_id:
            ses_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return ses_dict['user_id']
            if 'created_at' not in ses_dict:
                return None
            current_time = datetime.now()
            ses_duration = timedelta(seconds=self.session_duration)
            expiration_time = ses_dict['created_at'] + ses_duration
            if expiration_time < current_time:
                return None
            return ses_dict['user_id']
