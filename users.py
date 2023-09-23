from db import db
from flask import session
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash

#LOGIN
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

            return True
        else:
            return False

#LOGOUT clears all session parametres
def logout():
    session.clear()

#ADD NEW USER
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

