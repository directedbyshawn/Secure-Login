'''

    Flask app for final project.

'''

from .config import display
from .db import *
from flask import Flask, render_template, request, redirect, url_for
from .authenticate import authenticate, verify_new_account, random_password

app = Flask(__name__, static_folder='instance/static')

logged_in = False
login_attempts = 1
locked_out = False
current_user = ''
current_password = ''
current_auth_level = ''

@app.route('/', methods=['GET', 'POST'])
def home1():
    global locked_out
    # user is sent to login page if they arent locked out
    if (locked_out == True):
        return redirect(url_for('locked_out'))
    else:
        return render_template('index.html', title='Secure Login', heading='Secure Login', show=display)

@app.route('/index.html', methods=['GET', 'POST'])
def home():
    global logged_in, login_attempts, locked_out, current_user, current_password, current_auth_level
    # user is sent to login page if they arent locked out
    if request.method == 'GET':
        if (locked_out == True):
            return redirect(url_for('locked_out'))
        else:
            return render_template('index.html', title='Secure Login', heading='Secure Login', show=display)

    if request.method == 'POST':
        # gets form data
        username = request.form.get('usernameInput')
        password = request.form.get('passwordInput')

        # user is locked out if more than 3 bad attempts, redirected if bad but less than 3,
        # or logged in

        if (authenticate(username, password) == True):
            logged_in = True
            current_user = username
            current_password = password
            current_auth_level = get_auth_level(username)
            return redirect(url_for('login_success'))
        elif (login_attempts >= 3):
            locked_out = True
            return redirect(url_for('locked_out'))  
        else:
            login_attempts += 1
            return redirect(url_for('login_failure'))

@app.route('/login_success', methods=['GET'])
def login_success():
    global logged_in, locked_out, current_user, current_password, current_auth_level
    if logged_in:
        return render_template('login_success.html', 
                                title='Login Success', 
                                heading='Login Success',
                                username=current_user,
                                auth=current_auth_level)
    else:
        if (locked_out == True):
            return redirect(url_for('locked_out'))
        else:
            return redirect(url_for('login_failure'))

@app.route('/login_failure', methods=['GET'])
def login_failure():
    global locked_out
    if (locked_out == True):
        return redirect(url_for('locked_out'))
    else:
        return render_template('login_failure.html', title='Login Failure', heading='Login Failure')

@app.route('/locked_out', methods=['GET'])
def locked_out():
    return render_template('locked_out.html', title='Locked Out', heading='Locked Out')

@app.route('/create_account.html', methods=['GET', 'POST'])
def create_account():
    global locked_out
    if (locked_out == True):
        return redirect(url_for('locked_out'))
    else:
        if request.method == 'GET':
            random_pword = random_password()
            return render_template('create_account.html', title='Create Account', heading='Create Account', random_pass=random_pword)
        if request.method == 'POST':
            # gets form data
            username = request.form.get('usernameInput')
            password = request.form.get('passwordInput')

            if (verify_new_account(username, password) == True):
                # store new credentials in database
                add_user(username, password, 3)
                return render_template('index_account_created.html')
            else:
                return redirect(url_for('create_account_bad_pass'))

@app.route('/create_account_bad_pass', methods=['GET'])
def create_account_bad_pass():
    global locked_out
    if (locked_out == True):
        return redirect(url_for('locked_out'))
    else:
        if request.method == 'GET':
            random_pword = random_password()
            return render_template('create_account_bad_password.html', title='Create Account', heading='Create Account', random_pass=random_pword)

@app.route('/index_account_created', methods=['GET'])
def home_after_pass():
    global locked_out
    if (locked_out == True):
        return redirect(url_for('locked_out'))
    else:
        return render_template('index_account_created.html')

@app.route('/user_management', methods=['GET'])
def user_management():
    global locked_out, current_auth_level, logged_in
    if (locked_out == True):
        return redirect(url_for('locked_out'))
    elif (logged_in == False):
        return redirect(url_for('/index.html'))
    else:
        if (current_auth_level == 1):
            return render_template('access_granted.html')
        else:
            return render_template('access_denied.html')

@app.route('/systems_management', methods=['GET'])
def systems_management():
    global locked_out, current_auth_level, logged_in
    if (locked_out == True):
        return redirect(url_for('locked_out'))
    elif (logged_in == False):
        return redirect(url_for('/index.html'))
    else:
        if (current_auth_level == 1):
            return render_template('access_granted.html')
        else:
            return render_template('access_denied.html')

@app.route('/systems_overview', methods=['GET'])
def systems_overview():
    global locked_out, current_auth_level, logged_in
    if (locked_out == True):
        return redirect(url_for('locked_out'))
    elif (logged_in == False):
        return redirect(url_for('/index.html'))
    else:
        if (current_auth_level <= 2):
            return render_template('access_granted.html')
        else:
            return render_template('access_denied.html')

@app.route('/source_code', methods=['GET'])
def source_code():
    global locked_out, current_auth_level, logged_in
    if (locked_out == True):
        return redirect(url_for('locked_out'))
    elif (logged_in == False):
        return redirect(url_for('/index.html'))
    else:
        if (current_auth_level <= 2):
            return render_template('access_granted.html')
        else:
            return render_template('access_denied.html')

@app.route('/time_reporting', methods=['GET'])
def time_reporting():
    global locked_out, current_auth_level, logged_in
    if (locked_out == True):
        return redirect(url_for('locked_out'))
    elif (logged_in == False):
        return redirect(url_for('/index.html'))
    else:
        return render_template('access_granted.html')

@app.route('/it_help', methods=['GET'])
def it_help():
    global locked_out, current_auth_level, logged_in
    if (locked_out == True):
        return redirect(url_for('locked_out'))
    elif (logged_in == False):
        return redirect(url_for('/index.html'))
    else:
        return render_template('access_granted.html')