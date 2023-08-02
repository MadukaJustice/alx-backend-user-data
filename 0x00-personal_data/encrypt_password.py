#!/usr/bin/env python3
"""
Password Hashing module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes the given password and returns a salted hash"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if the given password matches the hashed password"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
