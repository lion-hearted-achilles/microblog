from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir
import os
# must define lm here to avoid circular references
# https://flask.readthedocs.org/en/latest/patterns/packages/
app = Flask(__name__)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

app.config.from_object('config')
# initialize database when we intialize the app
db = SQLAlchemy(app)
# avoid circular references here
from app import views, models

