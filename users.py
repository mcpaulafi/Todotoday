# Application ToDo Today is made by Paula Meuronen 2023 for Helsinki University course TKT20019
# users.py: user login and registration

from db import db
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
import secrets

# Login
# ##############################################################################

def login(username, password):
    sql = "SELECT user_id, username, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.user_id
            session["username"] = user.username
            session["csrf_token"] = secrets.token_hex(16)

            # Adding login time to database
            try:
                sql = "UPDATE users SET lastlogin_date=NOW() WHERE user_id=:user_id"
#                print(f"Login, user_id:{user.user_id}, date")
                db.session.execute(text(sql), {"user_id":user.user_id})
                db.session.commit()
            except Exception as e:
#                print("error sql", e)
                return False

            return True
        else:
            return False

# Logout: clears all session parametres
# ##############################################################################

def logout():
    session.clear()

# Register new user
# ##############################################################################

def register(username_new, password_new):
    hash_value = generate_password_hash(password_new)
    role = 2 #basic-level default

    try:
        sql = "INSERT INTO users (username, password, role, create_date) VALUES (:username, :password,:role, NOW())"
        db.session.execute(text(sql), {"username":username_new, "password":hash_value, "role":role})
        db.session.commit()
    except:
        return False
    return login(username_new, password_new)

def user_id():
    return session.get("user_id", 0)

# Is the new name already registered?
# ##############################################################################
def check_name(username):
    sql = "SELECT username FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    user = result.fetchone()
    if not user:
        return True
    else:
        return False