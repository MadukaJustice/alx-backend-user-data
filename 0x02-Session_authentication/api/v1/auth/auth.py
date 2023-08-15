#!/usr/bin/env python3
""" Auth module """
from flask import request
from typing import List, TypeVar
import os


class Auth():
    """ Auth class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns requre auth status """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        path = path.rstrip("/")
        for ex_path in excluded_paths:
            if ex_path.endswith("*"):
                ex_path = ex_path[:-1]
                if path.startswith(ex_path):
                    return False
            elif ex_path.rstrip("/") == path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Returns auth header """
        if request is None or request.headers.get("Authorization") is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns current user """
        return None

    def session_cookie(self, request=None):
        """ returns a cookie valur from a request """
        if request is None:
            return None

        _my_session_id = os.getenv('SESSION_NAME')
        return request.cookies.get(_my_session_id)