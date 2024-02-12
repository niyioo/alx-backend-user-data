#!/usr/bin/env python3
"""
Authentication class module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if authentication is required"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Remove trailing slashes from paths for consistency
        path = path.rstrip("/")
        excluded_paths = [p.rstrip("/") for p in excluded_paths]

        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """Return authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Return current user"""
        return None
