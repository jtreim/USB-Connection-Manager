from multiprocessing import Process, Event
import os
import signal
import sys
import time

from PyQt5.QtCore import QObject, pyqtSlot

import kivy
kivy.require('1.10.1')
from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from app.screens.main.main import MainScreen
from app.screens.settings.settings import SettingsScreen

from common import *

Config.set('graphics', 'width', 600)
Config.set('graphics', 'height', 300)

class USBManagerApp(App):
	def __init__(self, **kwargs):
		super(USBManagerApp, self).__init__(**kwargs)
		self.devices = []
		self.process = Process(target=self.run)
		self.settings_screen = None
		self.main_screen = None

	def build(self):
		self.title = 'USB Connect App'
		self.settings_screen = SettingsScreen(name='settings')
		self.settings_screen.data = self.devices
		self.main_screen = MainScreen(name='main')
		self.main_screen.subtitle = 'This is new...'
		self.main_screen.msg = ('I don\'t recognize this device. Would you '
								'like to register an action for it?')

		# Add screens to screen manager
		sm = ScreenManager()
		sm.add_widget(self.main_screen)
		sm.add_widget(self.settings_screen)
		return sm

	def is_running(self):
		return self.process.is_alive()

	def update_devices(self, data):
		print('got data: {}'.format(data))
		self.devices = data
		if self.is_running() and self.settings_screen:
			self.settings_screen.update_data(data)

	def stop(self):
		super(USBManagerApp, self).stop()
		if self.is_running():
			os.kill(self.process.pid, signal.SIGTERM)
			# self.process = Process(target=self.run)
		# self.process.terminate()
		# sys.exit()
