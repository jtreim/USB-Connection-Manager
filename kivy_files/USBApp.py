import os
import sys
from pid import PidFile

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

from kivy_files.screens.add_device.add_device import AddDeviceScreen
from kivy_files.screens.settings.settings import SettingsScreen

from constants import *

Config.set('graphics', 'width', 600)
Config.set('graphics', 'height', 300)

class USBManagerApp(App):
	def __init__(self, **kwargs):
		super(USBManagerApp, self).__init__(**kwargs)
		self.db = None
		self.devices = {}
		self.add_device_id = ''

	def build(self):
		self.title = 'USB Connect App'

		# Add screens to screen manager
		sm = ScreenManager()
		add_device_screen = AddDeviceScreen(name='add_device')
		add_device_screen.add_device_id = self.add_device_id
		sm.add_widget(add_device_screen)
		sm.add_widget(SettingsScreen(name='settings'))
		return sm

	def run(self):
		print('STARTUP::Trying to run the program!')
	
		# Create pidfile
		if self.is_running():
			print('STARTUP::Says I can\'t.')
			sys.exit()
		else:
			print('STARTUP::I am about to start!')
			with PidFile(piddir=RUN_DIR):
				super(USBManagerApp, self).run()

	def set_db(self, db):
		self.db = db

	def set_add_device(self, device_id):
		self.add_device_id = device_id

	def is_running(self):
		return os.path.isfile(PIDFILE)

	def stop(self):
		print('TEARDOWN::Shutting down gracefully...')
		super(USBManagerApp, self).stop()
		sys.exit()
