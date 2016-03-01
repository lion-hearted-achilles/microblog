import os
basedir = os.path.abspath(os.path.dirname(__file__))

# path of the database file
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# folder where the SQLAlchemy-midgrate data files are stored
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-w1ll-never-guess'

OPENID_PROVIDERS = [
         {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
         {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
         {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
         {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
         {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]
