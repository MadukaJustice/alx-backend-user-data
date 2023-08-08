#!/usr/bin/env python3
""" Basic Auth module """
from .auth import Auth
from models.user import User
from typing import TypeVar
from base64 import b64decode


class BasicAuth(Auth):
    """ Basic Auth class which inherits from Auth class """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ Returns the base64 part of the Auth header """
        h = authorization_header
        if h is None or not isinstance(h, str) or not h.startswith("Basic "):
            return None
        return h.split(" ")[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ Returns the decoded value of a base64 string """
        h = base64_authorization_header
        if h is None or not isinstance(h, str):
            return None
        try:
            return b64decode(h).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ Returns the email and pwd from b64 decoded value """
        h = decoded_base64_authorization_header
        if h is None or not isinstance(h, str) or ":" not in h:
            return None, None
        credentials = h.split(":", 1)
        return credentials[0], credentials[1]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Returns the User instance based off email and pwd  """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
            if len(users) == 0:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ overloads Auth and retrieves User instance """
        auth = self.authorization_header(request)

        if auth is None:
            return None

        extracted = self.extract_base64_authorization_header(auth)
        decoded = self.decode_base64_authorization_header(extracted)
        credentials = self.extract_user_credentials(decoded)
        email = credentials[0]
        pwd = credentials[1]
        return self.user_object_from_credentials(email, pwd)