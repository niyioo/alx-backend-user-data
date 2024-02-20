#!/usr/bin/env python3

"""
Authentication Module
"""
import bcrypt
import uuid
from db import DB
from user import User
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

    def valid_login(self, email: str, password: str) -> bool:
        """Validate user credentials.

        Args:
            email: A string representing the user's email address.
            password: A string representing the user's password.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_password = user.hashed_password
            # Check if the provided password matches the hashed password
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """Generate a new UUID."""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """Create a session for the user with the given email."""
        # Find the user by email
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        # Generate a new UUID for the session ID
        session_id = str(uuid.uuid4())

        # Update the user's session ID in the database
        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Retrieve the user corresponding to the given session ID.

        Args:
            session_id: A string representing the session ID.

        Returns:
            User: The corresponding User object if found, otherwise None.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by_session_id(session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy the session for the user with the given user ID.

        Args:
            user_id: An integer representing the user ID.

        Returns:
            None
        """
        try:
            user = self._db.find_user_by_id(user_id)
            user.session_id = None
            self._db.commit()
        except NoResultFound:
            pass

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
        # Find the user corresponding to the email
        user = self._db.find_user_by(email=email)

        # If the user does not exist, raise a ValueError
        if not user:
            raise ValueError(f"No user found with email {email}")

        # Generate a UUID for the reset token
        reset_token = str(uuid.uuid4())

        # Update the user's reset_token database field
        user.reset_token = reset_token

        # Commit the changes to the database
        self._db.commit()

        # Return the generated reset token
        return reset_token

    def update_password(self, reset_token: str, new_password: str) -> None:
        """Update user's password using reset token."""
        # Retrieve the user associated with the reset_token
        user = self._db.find_user_by_reset_token(reset_token)

        if user is None:
            # If no user is found with the reset_token, raise ValueError
            raise ValueError("Invalid reset token")

        # Hash the new password
        hashed_password = self._hash_password(new_password)

        # Update the user's hashed_password and reset_token fields
        user.hashed_password = hashed_password
        user.reset_token = None


if __name__ == "__main__":
    auth = Auth()
    email = 'bob@bob.com'
    password = 'MyPwdOfBob'
    auth.register_user(email, password)
    print(auth.create_session(email))
    print(auth.create_session("unknown@email.com"))
