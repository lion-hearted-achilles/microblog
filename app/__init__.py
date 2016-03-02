from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
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
if not app.debug:
   import logging
   from logging.andlers import SMPTHandler
   credentials = None
   if MAIL_USERNAME or MAIL_PASSWORD:
      credentials = (MAIL_USERNAME, MAIL_PASSWORD)

# avoid circular references here
from app import views, models

