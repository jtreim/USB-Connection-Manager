import contextvars
import daemon
import pyudev
import time

from USBConnect import app

udev_context = pyudev.Context()
udev_monitor = pyudev.Monitor.from_netlink(udev_context)
udev_monitor.filter_by(subsystem='usb')

EVENT_NONE = 0
EVENT_ADD_DEVICE = 1
EVENT_REMOVE_DEVICE = 2

event = EVENT_NONE
devices = []

finished = False

def handle_event(action, device):
    if action == 'add':
        print('{} connected'.format(device))
        global event
        event = EVENT_ADD_DEVICE
        global devices
        devices.append(device)

    elif action == 'remove':
        global event
        event = EVENT_REMOVE_DEVICE
        global devices
        devices.remove(device)
 
if __name__ == "__main__":
    with daemon.DaemonContext():
        udev_observer = pyudev.MonitorObserver(udev_monitor, handle_event)
        udev_observer.start()
        while not finished:
            if event == EVENT_ADD_DEVICE:
                event = EVENT_NONE
                if not app.is_running():
                    app.run()

                app.update_devices(devices)

            elif event == EVENT_REMOVE_DEVICE:
                event = EVENT_NONE
                if app.is_running():
                    app.update_devices(devices)

            time.sleep(1)
    
        # Wrap up any remaining work and shut down
