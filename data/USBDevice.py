import subprocess
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from common import *

NO_ACTION = 'none'

class USBDevice(QObject):
    created = pyqtSignal(str)
    action_changed = pyqtSignal(str, str)
    active_toggled = pyqtSignal(str, bool)

    def __init__(self, id, action=NO_ACTION, active=False):
        super(USBDevice, self).__init__()
        self.id = id
        self._action = action
        self._active = active

        self.created.emit(self.id)

    @property
    def action(self):
        return self._action
    
    @action.setter
    def action(self, new_action):
        self._action = new_action
        self.action_changed.emit(self.id, new_action)
    
    def do_action(self):
        process = subprocess.Popen(self._action.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
    
    @property
    def active(self):
        return self._active
    
    @active.setter
    def active(self, is_active):
        self._active = is_active
        print('All set to emit a toggle active event')
        self.active_toggled.emit(self.id, is_active)

    def __str__(self):
	    return 'ID:{} active:{}\naction:{}'.format(self.id, self._active, self._action)

