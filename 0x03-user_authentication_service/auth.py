#!/usr/bin/env python3
"""
Authentication Module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt"""
    # Generate a salt and hash the password with it
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
