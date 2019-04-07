import os
from PyQt5.QtCore import pyqtSlot as Slot
from data.tools.json import JsonDBTool
from data.USBDevice import USBDevice


# Shared constants

# Common files/folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUN_DIR = os.path.join(BASE_DIR, 'run')
PIDFILE = '%s/app.py.pid' % (RUN_DIR)

# DB defaults
NO_DEVICE = 'none'
NO_ACTION = 'none'



# Shared variables between scripts
# List of registered devices app knows about
devices = {}

# DB
# Load all data from the db
db = JsonDBTool()

@Slot
def db_initialized():
    registered_devices = db.get_all()
    global devices
    for dev in registered_devices:
        device = USBDevice(dev.get('id'), dev.get('action'))
        devices[device.id] = device

# Connect to db initialize
db.initialized.connect(db_initialized)
