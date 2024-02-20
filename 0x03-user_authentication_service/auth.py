#!/usr/bin/env python3

"""
Authentication Module
"""
import bcrypt
import uuid
from typing import Union
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt."""
    # Generate a salt and hash the password with it
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """Generate a new UUID."""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initializes Auth Instance"""
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
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user credentials.

        Args:
            email: A string representing the user's email address.
            password: A string representing the user's password.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                    password.encode("utf-8"),
                    user.hashed_password,
                )
        except NoResultFound:
            return False
        return False

    def create_session(self, email: str) -> str:
        """Create a session for the user with the given email."""
        # Find the user by email
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        if user is None:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Retrieve the user corresponding to the given session ID.

        Args:
            session_id: A string representing the session ID.

        Returns:
            User: The corresponding User object if found, otherwise None.
        """
        user = None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Destroy the session for the user with the given user ID.

        Args:
            user_id: An integer representing the user ID.

        Returns:
            None
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset password token for the
        user with the provided email.

        Args:
            email: A string representing the user's email address.

        Returns:
            str: The generated reset password token.

        Raises:
            ValueError: If no user exists with the provided email.
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, new_password: str) -> None:
        """Update user's password using reset token."""
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        new_password_hash = _hash_password(new_password)
        self._db.update_user(
            user.id,
            hashed_password=new_password_hash,
            reset_token=None,
        )
