#!/usr/bin/env python3
"""
Module for SessionAuth class
"""
from api.v1.auth.auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """
    SessionAuth class
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session for the given user_id
        """
        if not user_id or not isinstance(user_id, str):
            return None

        # Generate a Session ID using uuid module
        session_id = str(uuid.uuid4())

        # Store the session ID along with the user ID
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the user ID based on the session ID
        """
        if not session_id or not isinstance(session_id, str):
            return None

        # Retrieve the user ID based on the session ID
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> User:
        """
        Returns a User instance based on a cookie value
        """
        session_id = self.session_cookie(request)
        if not session_id:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return None
        return User.get(user_id)
