"""users.py: user login and registration"""
# Application ToDo Today is made by Paula Meuronen 2023
# for Helsinki University course TKT20019

from os import getenv
from flask import Flask

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes
