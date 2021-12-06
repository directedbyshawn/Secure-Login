'''

    Class to help with communicating with the database.

'''

import sqlite3, os, base64, hashlib, csv
from .config import DB_FILE

def create_db():

    ''' Database created '''

    conn = None
    c = None

    try:

        if not os.path.exists(DB_FILE):

            # create db connection
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()

            # create table
            c.execute('''CREATE TABLE accounts
                        (
                        username text,
                        password text,
                        authlevel int
                        )''')
            conn.commit()
            
            c.close()
            conn.close()
            c = None
            conn = None

            with open('app/test_credentials.csv') as csv_file:
                file = csv.reader(csv_file)
                for row in file:
                    try:
                        add_user(row[0], row[1], int(row[2]))
                    except:
                        print('ERROR: Could not add one of the test credentials to the db.')
           
            return True
        
        else:
            print('ERROR: Database already exists')
            return False
    except Exception:
        print("ERROR: Error creating database")
        if c is not None:
            c.close()
        if conn is not None:
            conn.close()
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
        conn = sqlite3.connect(DB_FILE)
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
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        for row in c.execute('SELECT * FROM accounts'):
            users.append(row)
    except sqlite3.DatabaseError:
        print('Error. Could not retrieve data.')
    finally:
        try:
            if c is not None:
                c.close()
            if conn is not None:
                conn.close()
        except Exception:
            print("ERROR: It appears you did not run setup.py")

    return users

def get_auth_level(username):

    # finds correct account and returns auth level
    users = retrieve_accounts()

    auth_level = ''
    for user in users:
        if user[0] == username:
            auth_level = user[2]

    return auth_level

def salted_pass(password):
    
    ''' Returns hashed and salted password '''

    # generates salt
    token = os.urandom(30)
    salt = base64.b64encode(token).decode('utf-8')

    hashable = salt + password  # concatenate salt and plain_text
    hashable = hashable.encode('utf-8')  # convert to bytes
    this_hash = hashlib.sha1(hashable).hexdigest()  # hash w/ SHA-1 and hexdigest
    return salt + this_hash

if __name__ == '__main__':
    print("ERROR: Only run from start.py and setup.py")
