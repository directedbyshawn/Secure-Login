'''

    Launch flask app from here.

'''

import traceback

from flask_app import app

if __name__ == '__main__':
    try:
        app.run(debug=app.debug, host='localhost', port=8097)
    except Exception as err:
        traceback.print_exc()