#!/usr/bin/env python3

"""
Module for Session DB Authentication class
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """
    Session DB Authentication class
    """

    def create_session(self, user_id=None):
        """
        Create a new session and store it in the database
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        kwargs = {
            'user_id': user_id,
            'session_id': session_id,
        }
        user_session = UserSession(**kwargs)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the user ID based on the session ID from the database
        """
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """
        Destroys the session based on the session ID from the request cookie
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
