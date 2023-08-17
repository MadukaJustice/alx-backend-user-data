#!/usr/bin/env python3
"""
Integration testing module
"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://localhost:5001"


def register_user(email: str, password: str) -> None:
    """Tests whether or not a user can be registered"""
    response = requests.post(f"{BASE_URL}/users",
                             data={
                                 "email": email,
                                 "password": password
                             })
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "user created"}

    response = requests.post(f"{BASE_URL}/users",
                             data={
                                 "email": email,
                                 "password": password
                             })

    assert response.status_code == 400
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests whether the wrong password is rejected"""
    response = requests.post(f"{BASE_URL}/sessions",
                             data={
                                 "email": email,
                                 "password": password
                             })
    assert response.status_code == 401


def profile_unlogged() -> None:
    """Tests whether or not an unlogged user can access the profile"""
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403


def log_in(email: str, password: str) -> str:
    """Logs in a user"""
    response = requests.post(f"{BASE_URL}/sessions",
                             data={
                                 "email": email,
                                 "password": password
                             })
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL, "message": "logged in"}
    session_id = response.cookies.get("session_id")
    assert session_id is not None
    return session_id


def profile_logged(session_id: str) -> None:
    """Tests whether or not a logged user can access the profile"""
    response = requests.get(f"{BASE_URL}/profile",
                            cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """Logs out a user"""
    response = requests.delete(f"{BASE_URL}/sessions",
                               cookies={"session_id": session_id})
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue"}
    profile_unlogged()


def reset_password_token(email: str) -> str:
    """Gets a password reset token"""
    response = requests.post(f"{BASE_URL}/reset_password",
                             data={"email": email})
    assert response.status_code == 200
    token = response.json().get("reset_token")
    assert token is not None
    return token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests whether or not a user can update their password with a reset token
    """
    response = requests.put(f"{BASE_URL}/reset_password",
                            data={
                                "email": email,
                                "reset_token": reset_token,
                                "new_password": new_password
                            })
    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
