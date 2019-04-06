import daemon
import pyudev
import time
import subprocess

from constants import *
from data.tools.json import JsonDBTool
from data.USBDevice import USBDevice
from manager import app_is_running

START_APP = 'python manager.py'

EVENT_NONE = 0
EVENT_ADD_DEVICE = 1
EVENT_REMOVE_DEVICE = 2

event = EVENT_NONE
added = []
removed = []

def handle_event(action, device):
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
 
def run_command(cmd, args={}):
    arg_list = [cmd]
    for key in args:
        arg_list.append(key)
        arg_list.append(args.get(key))
    
    subprocess.Popen(arg_list, shell=True, executable='/bin/bash')

if __name__ == "__main__":
    # with daemon.DaemonContext():

    # Set up pyudev monitoring
    udev_context = pyudev.Context()
    udev_monitor = pyudev.Monitor.from_netlink(udev_context)
    udev_monitor.filter_by(subsystem='usb')
    
    # Listen for udev events
    udev_observer = pyudev.MonitorObserver(udev_monitor, handle_event)
    udev_observer.start()


    # Load all data from the dbTool
    db = JsonDBTool()
    registered_devices = db.get_all()
    devices = {}
    for dev in registered_devices:
        device = USBDevice(dev.get('id'), dev.get('action'))
        devices[device.id] = device

    # Run process until told stahp
    finished = False
    while not finished:

        if event & EVENT_ADD_DEVICE:
            for dev_id in added:
                if dev_id in devices:
                    device = devices.get(dev_id)
                    devices.get(dev_id).active = True
                    if device.action != NO_ACTION:
                        run_command(device.action)
                    elif not app_is_running():
                        run_command(START_APP, args={"-a":dev_id})

            event ^= EVENT_ADD_DEVICE

        elif event & EVENT_REMOVE_DEVICE:
            event ^= EVENT_REMOVE_DEVICE
            if app.is_running():
                app.update_devices(devices)

        time.sleep(1)
    
        # Wrap up any remaining work and shut down
