#!/usr/bin/env python3
import argparse
import logging
import os
import sys

from pid import PidFile

from data.tools.json import JsonDBTool
from constants import *


parser = argparse.ArgumentParser()
parser.add_argument('action', dest='action', description='What should the app do?')
parser.add_argument('-a', '--add', dest='new_device', default=NO_DEVICE,
					help='Device ID to register')
parser.add_argument('-r', '--remove', dest='remove_device', default=NO_DEVICE,
					help='Device ID to remove')

# Running from command line
if __name__ == '__main__':
	args = parser.parse_args()
	sys.argv = [sys.argv[0]]

	# Declare Kivy after clearing command line arguments
	from kivy_files.USBApp import USBManagerApp
	app = USBManagerApp()

	def register_device(device_id):
		app.set_add_device(device_id)
		app.run()

	if args.action == REGISTER_DEVICE and args.new_device != NO_DEVICE:
		register_device(args.new_device)
	elif args.action == REGISTER_DEVICE:
		logging.error('No device id given for registration!')

	app.run()
	if os.path.isfile(PIDFILE):
		app.stop()
