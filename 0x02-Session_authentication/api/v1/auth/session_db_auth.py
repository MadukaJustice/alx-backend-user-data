#!/usr/bin/env python3
""" SessionDBAuth module definition """

from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class that inherits from SessionExpAuth """
    def create_session(self, user_id=None):
        """ Creates a new user sesson instance and returns the session id """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns the user id based on the session id """
        if session_id is None:
            return None

        sessions = UserSession.search({"session_id": session_id})
        if len(sessions) == 0:
            return None

        for session in sessions:
            if self.session_duration <= 0:
                return session.user_id

            created_at = session.created_at
            limit = created_at + timedelta(seconds=self.session_duration)
            if limit < datetime.now():
                return None

            return session.user_id

    def destroy_session(self, request=None):
        """
            Destroys the UserSession based on the session_id
            from the request cookie
        """
        if request is None or not self.session_cookie(request):
            return False

        session_id = self.session_cookie(request)
        sessions = UserSession.search({"session_id": session_id})
        if len(sessions) == 0:
            return False

        for session in sessions:
            session.remove()
            return True