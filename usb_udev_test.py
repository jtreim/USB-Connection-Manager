import contextvars
import daemon
import pyudev
import time

from app import startup, teardown

udev_context = pyudev.Context()
udev_monitor = pyudev.Monitor.from_netlink(udev_context)
udev_monitor.filter_by(subsystem='usb')

device_connected = False

def handle_event(action, device):
    if action == 'add':
        print('{} connected'.format(device))
        global device_connected
        device_connected = True
        print('Device connected: %s' % (device_connected))

# with daemon.DaemonContext():
udev_observer = pyudev.MonitorObserver(udev_monitor, handle_event)
udev_observer.start()
    
while not device_connected:
    print('Sleeping...')
    time.sleep(1)

startup()
