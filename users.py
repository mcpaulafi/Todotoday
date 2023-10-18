"""users.py: user login and registration"""
# Application ToDo Today is made by Paula Meuronen 2023
# for Helsinki University course TKT20019

import secrets
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from flask import session
from db import db


def login(username, password):
    """Login"""
    sql = "SELECT user_id, username, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if not user:
        return False

    if check_password_hash(user.password, password):
        session["user_id"] = user.user_id
        session["username"] = user.username
        session["csrf_token"] = secrets.token_hex(16)

        # Adding login time to database
        try:
            sql = "UPDATE users SET lastlogin_date=NOW() WHERE user_id=:user_id"
#            print(f"Login, user_id:{user.user_id}, date")
            db.session.execute(text(sql), {"user_id":user.user_id})
            db.session.commit()
        except Exception:
#           print("error sql", e)
            return False

        return True
    return False

def logout():
    """Logout: clears all session parametres"""
    session.clear()

def register(username_new, password_new):
    """Register new user"""
    hash_value = generate_password_hash(password_new)
    role = 2 #basic-level default

    try:
        sql = "INSERT INTO users (username, password, role, create_date) \
            VALUES (:username, :password,:role, NOW())"
        db.session.execute(text(sql), {"username":username_new, "password":hash_value, "role":role})
        db.session.commit()
    except Exception:
        return False
    return login(username_new, password_new)

def user_id():
    """Get userid from session"""
    return session.get("user_id", 0)

def check_name(username):
    """Is the new name already registered?"""
    sql = "SELECT username FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if not user:
        return True
    return False
    