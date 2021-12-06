'''

    Directory setup.

'''

import os 

import app.db as db

DIRS = ['app/instance/var/db',
        'app/instance/var/log',
        'app/instance/var/tmp',
        'app/instance/var/run']

if __name__ == '__main__':

    os.system('cls')

    print('Creating directories...')
    for d in DIRS:
        try:
            os.makedirs(d)
        except FileExistsError:
            pass

    print('Initializing database...')
    if (db.create_db()):
        print('Database created!')
    else:
        print("ERROR: Could not create database")