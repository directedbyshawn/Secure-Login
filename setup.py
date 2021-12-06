'''

    Directory setup.

'''

import os 

from db import *

DIRS = ['instance/var/db',
        'instance/var/log',
        'instance/var/tmp',
        'instance/var/run']

if __name__ == '__main__':

    print('Creating directories...')
    for d in DIRS:
        try:
            os.makedirs(d)
        except FileExistsError:
            pass

    print('Initializing database...')
    create_db()

    print('Done!')