#!/usr/bin/env python3
"""
Module for SessionAuth class
"""
from api.v1.auth.auth import Auth
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
