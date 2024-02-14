#!/usr/bin/env python3
"""
Authentication class module
"""
from flask import request
from typing import List, TypeVar
User = TypeVar('User')


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required"""
        if path is None:
            return True
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for excluded_path in excluded_paths:
                if excluded_path.startswith(path):
                    return False
                if path.startswith(excluded_path):
                    return False
                if excluded_path.endswith("*"):
                    if path.startswith(excluded_path[:-1]):
                        return False
        return True

    def authorization_header(self, request=None) -> str:
        """Return authorization header"""
        if request is None:
            return None

        if "Authorization" not in request.headers:
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> User:
        """Return current user"""
        return None

    def session_cookie(self, request=None) -> str:
        """
        Returns a cookie value from a request
        """
        if request is None:
            return None

        session_name = getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name)
