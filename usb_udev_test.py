import contextvars
import daemon
import pyudev
import time

from app import startup as app_startup
from app import teardown as app_cleanup

udev_context = pyudev.Context()
udev_monitor = pyudev.Monitor.from_netlink(udev_context)
udev_monitor.filter_by(subsystem='usb')

EVENT_NONE = 0
EVENT_NEW_DEVICE = 1

event = EVENT_NONE

finished = False

def handle_event(action, device):
    if action == 'add':
        print('{} connected'.format(device))
        global event
        event = EVENT_NEW_DEVICE

# with daemon.DaemonContext():
udev_observer = pyudev.MonitorObserver(udev_monitor, handle_event)
udev_observer.start()



while not finished:
    if event == EVENT_NEW_DEVICE:
        event = EVENT_NONE
        app_startup()

        # When app finishes, make sure it stops gracefully
        app_cleanup()

    time.sleep(.1)

# Wrap up any remaining work and shut down
