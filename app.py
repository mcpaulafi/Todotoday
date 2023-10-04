# Application ToDo Today is made by Paula Meuronen 2023 for Helsinki University course TKT20019
# app.py: start application and Flask 
 
from flask import Flask
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")

import routes