#!/usr/bin/env python3

"""
Module that defines the BasicAuth class for basic authentication.
"""

from api.v1.auth.auth import Auth
from models.user import User
import base64
from typing import TypeVar


class BasicAuth(Auth):
    """
    Basic authentication class
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header
        for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header.

        Returns:
            str: The Base64 part of the Authorization header,
            or None if the header is invalid.
        """
        if (
            authorization_header is None
            or not isinstance(authorization_header, str)
        ):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split(" ", 1)[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes the Base64 authorization header.

        Args:
            base64_authorization_header (str): The Base64 authorization header.

        Returns:
            str: The decoded value of the Base64 header,
            or None if it's not valid.
        """
        if (
            base64_authorization_header is None
            or not isinstance(base64_authorization_header, str)
        ):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user email and password from a decoded Base64
        authorization header.

        Args:
            decoded_base64_authorization_header (str): The decoded
            Base64 authorization header.

        Returns:
            tuple: A tuple containing the user email and password.
        """
        if (
            decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str)
        ):
            return None, None

        if ":" not in decoded_base64_authorization_header:
            return None, None

        user_email, user_password = decoded_base64_authorization_header.split(
            ":", 1)
        return user_email, user_password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on the email and password.

        Args:
            user_email (str): The email of the user.
            user_pwd (str): The password of the user.

        Returns:
            User: The User instance, or None if user credentials are invalid.
        """
        if (
            user_email is None
            or not isinstance(user_email, str)
            or user_pwd is None
            or not isinstance(user_pwd, str)
        ):
            return None

        users = User.search({"email": user_email})
        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request.

        Args:
            request (Request): The request object.

        Returns:
            User: The User instance, or None if not found.
        """
        if request is None:
            return None

        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None

        base64_header = self.extract_base64_authorization_header(
            authorization_header)
        if base64_header is None:
            return None

        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None

        user_email, user_password = self.extract_user_credentials(
            decoded_header)
        if user_email is None or user_password is None:
            return None

        return self.user_object_from_credentials(user_email, user_password)
