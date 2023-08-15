#!/usr/bin/env python3
""" Session Auth module """
from .auth import Auth
from models.user import User
from typing import TypeVar
import uuid


class SessionAuth(Auth):
    """ Session Auth class which inherits from Auth class """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Creates a new session ID for a user_id """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ returns the associated User ID based on a Session ID """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ returns the current User ID based on a cookie value """
        session = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session)

        return User.get(user_id)

    def destroy_session(self, request=None):
        """ Destroy user session cookie """
        if request is None:
            return False

        session_cookie = self.session_cookie(request)
        if not session_cookie:
            return False

        user_id = self.user_id_for_session_id(session_cookie)
        if not user_id:
            return False

        del self.user_id_by_session_id[session_cookie]
        return True