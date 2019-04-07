import daemon
import os
import pyudev
import time
import signal
import subprocess

from common import *
from kivy_files.USBApp import USBManagerApp

from data.tools.json import JsonDBTool
from data.USBDevice import USBDevice

finished = False

EVENT_NONE = 0
EVENT_ADD_DEVICE = 1
EVENT_REMOVE_DEVICE = 2

event = EVENT_NONE
added = []
removed = []


def stop(sig, frame):
    global finished
    print('I\'m stopping everything now...')
    finished = True

signal.signal(signal.SIGINT, stop)

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

if __name__ == "__main__":
    # with daemon.DaemonContext():

    # Set up pyudev monitoring
    udev_context = pyudev.Context()
    udev_monitor = pyudev.Monitor.from_netlink(udev_context)
    udev_monitor.filter_by(subsystem='usb')
    
    # Listen for udev events
    udev_observer = pyudev.MonitorObserver(udev_monitor, handle_udev_event)
    udev_observer.start()

    # Run process until told stahp
    while not finished:

        # A device was connected
        if event & EVENT_ADD_DEVICE:
            for dev_id in added:
                global devices
                if dev_id in devices:
                    device = devices.get(dev_id)
                    devices.get(dev_id).active = True

                else:
                    devices[dev_id] = USBDevice(dev_id, active=True)


            event ^= EVENT_ADD_DEVICE

        # A device was disconnected
        elif event & EVENT_REMOVE_DEVICE:
            event ^= EVENT_REMOVE_DEVICE
            
                
        # Sleep until next event
        time.sleep(1)
    
    
    # Wrap up any remaining work and shut down
