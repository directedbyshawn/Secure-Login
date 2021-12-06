'''

    Class to help with communicating with the database.

'''

import sqlite3
from authenticate import salted_pass

def create_db():

    ''' Database created '''

    try:
        conn = sqlite3.connect('instance/var/db/users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE accounts
                    (
                    username text,
                    password text,
                    authlevel int
                    )''')
        conn.commit()
        return True
    except BaseException:
        return False
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

def add_user(username, password, auth_level):

    ''' Add user to database '''

    safe_password = salted_pass(password)

    data_to_insert = [(username, safe_password, auth_level)]

    try:
        conn = sqlite3.connect('instance/var/db/users.db')
        c = conn.cursor()
        c.executemany('INSERT INTO accounts VALUES (?, ?, ?)', data_to_insert)
        conn.commit()
    except sqlite3.IntegrityError:
        print('ERROR: Attempt to add duplicate record.')
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

def retrieve_accounts():

    ''' Retrieves all user accounts from database '''

    users = []

    try:
        conn = sqlite3.connect('instance/var/db/users.db')
        c = conn.cursor()
        for row in c.execute('SELECT * FROM accounts'):
            users.append(row)
    except sqlite3.DatabaseError:
        print('Error. Could not retrieve data.')
    finally:
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()

    return users

def get_auth_level(username):

    # finds correct account and returns auth level
    users = retrieve_accounts()

    auth_level = ''
    for user in users:
        if user[0] == username:
            auth_level = user[2]

    return auth_level
