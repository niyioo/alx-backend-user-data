#!/usr/bin/env python3

"""
Authentication Module
"""

from db import DB
from user import User
import bcrypt
from sqlalchemy.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user.

        Args:
            email: A string representing the user's email address.
            password: A string representing the user's password.

        Returns:
            User: A User object representing the newly registered user.

        Raises:
            ValueError: If a user already exists with the provided email.
        """
        # Check if user with the provided email already exists
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        # Hash the password
        hashed_password = self._hash_password(password)

        # Save the user to the database
        user = self._db.add_user(email, hashed_password)

        return user

    def _hash_password(self, password: str) -> bytes:
        """Hash a password using bcrypt."""
        # Generate a salt and hash the password with it
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password
