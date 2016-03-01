from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm
from .models import User

@app.route('/')
@app.route('/index')
# ensure page is only seen by logged in users
@login_required
def index():
   user = g.user
   # user = {'nickname': 'Geoff'} # mock user object
   posts = [ # mock array of posts
         {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
            },
         {
            'author': {'nickname': 'Susan'},
               'body': 'The Avengers movie was so cool!'
               }
            ]
   return render_template('index.html',
         title = 'Home',
         user = user,
         posts = posts) # invokes Jinja2 templating engine

@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
   if g.user is not None and g.user.is_authenticated:
      return redirect(url_for('index'))
   form = LoginForm()
   # does all form processing work
   # if called as part of form submission request:
   # gathers all data, runs all validators attached to fields, returns True
   if form.validate_on_submit():
      session['remember_me'] = form.remember_me.data
      return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
   return render_template('login.html',
         title='Sign In',
         form = form,
         providers=app.config['OPENID_PROVIDERS'])

@lm.user_loader
def load_user(id):
   return User.query.get(int(id))

@oid.after_login
def after_login(resp):
      if resp.email is None or resp.email == "":
         flash('Invalid login. Please try again.')
         return redirect(url_for('login'))
      user = User.query.filter_by(email = resp.email).first()
      if user is None:
         nickname = resp.nickname
         if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
         user = User(nickname=nickname, email=resp.email)
         db.session.add(user)
         db.session.commit()
      remember_me = False
      if 'remember_me' in session:
         reember_me = session['remember_me']
         session.pop('remember_me', None)
      login_user(user, remember = remember_me)
      return redirect(request.args.get('next') or url_for('index'))

# in login view we check if a user already logged in
# implement this here using before_request event from Flask
@app.before_request
def before_request():
   g.user = current_user

@app.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('index'))
