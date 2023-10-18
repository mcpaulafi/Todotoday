"""db.py: database connection"""
# Application ToDo Today is made by Paula Meuronen 2023
# for Helsinki University course TKT20019

from os import getenv
from flask_sqlalchemy import SQLAlchemy
from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)
