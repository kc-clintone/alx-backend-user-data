#!/usr/bin/env python3
"""
Let's now dive into encrypting passwords.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    This function hashes passwords using random salt value
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Read hashees from given passwords
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
