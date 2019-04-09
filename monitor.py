# import daemon
import os
import sys
import pyudev
import time
import signal
# import subprocess

from PyQt5.QtCore import QObject, pyqtSlot

from common import *
from app.run import USBManagerApp

from data.tools.json import JsonDBTool
from data.USBDevice import USBDevice

# finished = False

EVENT_NONE = 0
EVENT_ADD_DEVICE = 1
EVENT_REMOVE_DEVICE = 2

event = EVENT_NONE
added = []
removed = []

# When PyQt5 fails to tell you anything, cause it does its own thing for
# exceptions.

sys._excepthook = sys.excepthook

def application_exception_hook(exctype, value, traceback):
    # Let's try to write the problem
    print("Exctype : %s, value : %s traceback : %s"%(exctype, value, traceback))
    # Call the normal Exception hook after (this will probably abort application)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

sys.excepthook = application_exception_hook

def handle_udev_event(action, device):
    global event
    global added
    global removed

    if action == 'add':
        # Create a unique id for the device
        custom_id = '{}-{}'.format(device.get('ID_VENDOR_FROM_DATABASE'),
                                   device.get('PRODUCT'))
        event |= EVENT_ADD_DEVICE
        if custom_id not in added:
            added.append(custom_id)
        

    elif action == 'remove':
        # Create a unique id for the device
        custom_id = '{}-{}'.format(device.get('ID_VENDOR_FROM_DATABASE'),
                                   device.get('PRODUCT'))
        event |= EVENT_REMOVE_DEVICE
        if custom_id not in removed:
            removed.append(custom_id)

class Monitor(QObject):
    def __init__(self):
        super(Monitor, self).__init__()
        
        # Put data from db into memory
        self.db = JsonDBTool()
        devices = self.db.get_all()
        self.devices = {}

        for device in devices:
            id = device.get('device_id', '')
            if id != '':
                action = device.get('device_action')
                d = USBDevice(id, action=action)
                d.action_changed.connect(self.device_registered)
                d.active_toggled.connect(self.device_toggled)
                self.devices[id] = d

        self.udev_context = pyudev.Context()
        self.udev_monitor = pyudev.Monitor.from_netlink(self.udev_context)
        self.udev_monitor.filter_by(subsystem='usb')
        self.udev_observer = pyudev.MonitorObserver(self.udev_monitor, handle_udev_event)
        
        self.app = USBManagerApp()

        # For multiprocessing app and monitor
        # self.queue = Queue()
        # self.app.process = Process(target=self.app.run)

        self.finished = False

    def update_app(self):
        updated = self.get_device_list()
        self.app.update_devices(updated)
    
    def get_device_list(self):
        result = []
        for key in self.devices:
            dev = self.devices[key]
            result.append({
                'device_id': dev.id,
                'device_action': dev.action,
                'device_active': dev.active
            })
        return result

    @pyqtSlot()
    def device_registered(self, device_id, new_action):
        self.db.register(device_id, cmd=new_action, save=False)
        self.update_app()

    @pyqtSlot()
    def device_toggled(self, device_id=None, is_active=None):
        self.update_app()

    def run(self):
        # Listen for udev events
        self.udev_observer.start()
        
        print(self.devices)

        while not self.finished:
            global event
            global added
            global removed

            # A device was connected
            if event & EVENT_ADD_DEVICE:
                print('Got a device connection event!')
                print('added: {}'.format(added))
                for dev_id in added:
                    if dev_id in self.devices:
                        print('Found the device!')
                        device = self.devices.get(dev_id)
                        self.devices.get(dev_id).active = True
                        if device.action != self.db.NO_ACTION:
                            device.do_action()
                        else:
                            self.update_app()
                    
                    else:
                        new_device = USBDevice(dev_id)
                        new_device.action_changed.connect(self.device_registered)
                        new_device.active_toggled.connect(self.device_toggled)
                        self.devices[dev_id] = new_device

                        if not self.app.is_running():
                            print('MONITOR::I want to start the app.')
                            self.app.process.start()
                        self.update_app()

                event ^= EVENT_ADD_DEVICE
            
            # A device was disconnected
            if event & EVENT_REMOVE_DEVICE:
                print('Got a device disconnection event!')
                print('removed: {}'.format(removed))
                if self.app.is_running():
                    self.update_app()
                event ^= EVENT_REMOVE_DEVICE
            
            # Sleep until next event
            time.sleep(1)
    
    def stop(self, sig, frame):
        self.finished = True
        if self.app.is_running():
            self.app.stop()

    def cleanup(self):
        self.db.save()

usb_monitor = Monitor()

signal.signal(signal.SIGINT, usb_monitor.stop)

if __name__ == "__main__":
    # with daemon.DaemonContext():    
    usb_monitor.run()

    # Wrap up any remaining work and shut down
    usb_monitor.cleanup()
