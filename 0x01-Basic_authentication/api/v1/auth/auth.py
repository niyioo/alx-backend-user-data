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
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Remove trailing slashes from paths for consistency
        path = path.rstrip("/")

        for excluded_path in excluded_paths:
            # Remove trailing slashes from excluded paths for consistency
            excluded_path = excluded_path.rstrip("/")
            if excluded_path.endswith("*") and \
                    path.startswith(excluded_path[:-1]):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Return authorization header"""
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> User:
        """Return current user"""
        return None
