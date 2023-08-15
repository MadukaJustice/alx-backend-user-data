#!/usr/bin/env python3
""" Session Expiration Auth module """

import os
from datetime import datetime, timedelta
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class """
    def __init__(self):
        """ Initialization params (set session duration """
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION'))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Create a session id from user_id """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {
                "user_id": user_id,
                "created_at": datetime.now(),
                }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns the user_id from te session dictionary """
        if session_id is None or not self.user_id_by_session_id[session_id]:
            return None

        session_dictionary = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dictionary["user_id"]

        if not session_dictionary["created_at"]:
            return None

        created_at = session_dictionary["created_at"]
        time_limit = created_at + timedelta(seconds=self.session_duration)
        if time_limit < datetime.now():
            return None

        return session_dictionary["user_id"]