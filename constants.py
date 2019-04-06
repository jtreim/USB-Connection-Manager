import os

# Global Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUN_DIR = os.path.join(BASE_DIR, 'run')
PIDFILE = '%s/app.py.pid' % (RUN_DIR)
NO_DEVICE = 'none'
NO_ACTION = 'none'