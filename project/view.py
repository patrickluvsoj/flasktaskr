# imports - sqlite, flask
import sqlite3
from functools import wraps

from flask import Flask, render_template, redirect, session, 
flash, request, url_for

# instantiate flask app
app = Flask(__name__)

# get configurations
app.config.from_object('_config')

# method to connect to db
def connect_db():
    return sqlite3.connect(app.config['DATABASE_PATH'])

# login required decorator
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash("Login is required")
            return redirect(url_for('login'))
        return wrap

# logout method
@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash("Log out successful")
    return redirect(url_for('login'))

# login page
@app.route('/', methods='GET', 'POST')
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] \
            or request.form['password'] != app.config['PASSWORd']:
            error =("Login credentials are incorrect. Try again.")
            return render_template('login.html', error = error)
        else:
            session['logged_in'] = True
            flash('Welcome!')
            return redirect(url_for('tasks'))
    return render_template('login.html')



