#!/usr/bin/env python3

"""
Module for User Session Model
"""

from models.base import Base


class UserSession(Base):
    """
    User Session Model
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        Initialize User Session instance
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
