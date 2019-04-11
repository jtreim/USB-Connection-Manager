# USB Connection Manager
A daemon that monitors udev connections, and registers bash commands for unique USB connections.

## What's going on
There are three main pieces; the daemon (monitor.py), the windowed app (app/run.py), and the database for registered USB connections (data/tools/dbtool.py).

- The monitor handles receiving udev events, and determining what to do with the event.
- The DBTool is used to initialize data, and save when shutting down. The current dbtool being used is a JSON implementation (data/tools/json.py). Currently, the entire db is loaded by the monitor on startup.
- A window is spawned using Kivy to handle displaying and registering USB connections.

### Setup
Right now, this only is supporting a Linux platform with Python 3.6. Installing all required libraries can be done with pip by running
```
pip install -r requirements.txt
```

#### Notes
When pyudev detects a USB udev event (either connecting or disconnecting), pyudev receives a dict of properties about the event. Every udev calls on pyudev roughly 4 or 5 times, each time having some fields being included or excluded. This seems to vary between each of the multiple signals, by the type of device being detected, and can vary by port detecting the event. The pyudev_common_info.json is a json object of consistent information that pyudev receives.