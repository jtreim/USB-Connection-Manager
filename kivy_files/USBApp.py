import os
import sys
from pid import PidFile

import kivy
kivy.require('1.10.1')
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from screens.main.main import MainScreen
from screens.settings.settings import SettingsScreen

# from common import *
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RUN_DIR = os.path.join(BASE_DIR, 'run')
PIDFILE = '%s/app.py.pid' % (RUN_DIR)

Config.set('graphics', 'width', 600)
Config.set('graphics', 'height', 300)

class USBManagerApp(App):
	def __init__(self, **kwargs):
		super(USBManagerApp, self).__init__(**kwargs)
		self.db = None
		self.devices = []

	def build(self):
		self.title = 'USB Connect App'

		# Add screens to screen manager
		sm = ScreenManager()
		sm.add_widget(MainScreen(name='main'))
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

	def is_running(self):
		return os.path.isfile(PIDFILE)

	def stop(self):
		print('TEARDOWN::Shutting down gracefully...')
		super(USBManagerApp, self).stop()
		sys.exit()

USBManagerApp().run()