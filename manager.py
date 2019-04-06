#!/usr/bin/env python3
import argparse
import os
import sys

from pid import PidFile

from data.tools.json import JsonDBTool
from constants import *


parser = argparse.ArgumentParser()
parser.add_argument('-a', '--add', dest='add_device', default=NO_DEVICE,
					help='Device ID to register')
parser.add_argument('-r', '--remove', dest='remove_device', default=NO_DEVICE,
					help='Device ID to remove')

def app_is_running():
	return os.path.isfile(PIDFILE)

# Running from command line
if __name__ == '__main__':
	args = parser.parse_args()
	sys.argv = [sys.argv[0]]

	# Declare Kivy after clearing command line arguments
	from kivy_files.USBApp import USBManagerApp
	app = USBManagerApp()

	if args.add_device != NO_DEVICE:
		app.set_add_device(args.add_device)

	app.run()
	if app_is_running():
		app.stop()
