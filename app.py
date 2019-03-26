#!/usr/bin/env python3

import os
import sys
import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from pid import PidFile

from screens.add_device.add_device import AddDeviceScreen
from screens.settings.settings import SettingsScreen  

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUN_DIR = os.path.join(BASE_DIR, 'run')
PIDFILE = '%s/app.py.pid' % (RUN_DIR)

Config.set('graphics', 'width', 600)
Config.set('graphics', 'height', 300)


class USBConnectApp(App):
	def build(self):
		self.title = 'USB Connect App' 
		# Registering a new device screen
		device_screen = AddDeviceScreen(name='add_device')

		# Settings screen
		settings_screen = SettingsScreen(name='settings')

		# Add screens to screen manager
		sm = ScreenManager()
		sm.add_widget(device_screen)
		sm.add_widget(settings_screen)
		return sm

def startup():
	print('STARTUP::Trying to run the program!')
	
	# Create pidfile
	if os.path.isfile(PIDFILE):
		print('STARTUP::Says I can\'t.')
		sys.exit()
	else:
		print('STARTUP::I am about to start!')
		with PidFile(piddir=RUN_DIR):
			USBConnectApp().run()

def teardown():
	print('TEARDOWN::Shutting down gracefully...')

if __name__ == '__main__':
	startup()
