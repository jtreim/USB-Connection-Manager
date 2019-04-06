import subprocess

class USBDevice:
    def __init__(self, id, action, active=False):
        self.id = id
        self.action = action
        self.active = active

    def do_action(self):
        process = subprocess.Popen(self.action.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

    def __str__(self):
	    return 'ID:{} active:{}\naction:{}'.format(self.id, self.active, self.action)

