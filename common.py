import os
from PyQt5.QtCore import pyqtSlot
from data.tools.json import JsonDBTool
from data.USBDevice import USBDevice


# Shared constants
# Common files/folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PID_DIR = os.path.join(BASE_DIR, 'pid')
PIDFILE = '%s/app.py.pid' % (PID_DIR)


# Shared variables between scripts
# List of registered devices app knows about
devices = {}

# DB
# Load all data from the db
db = JsonDBTool()

