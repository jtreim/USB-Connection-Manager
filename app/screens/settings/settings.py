import kivy
kivy.require('1.10.1')

from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen

from app.views.device_rv.device_rv import DeviceRV

Builder.load_file('app/screens/settings/display.kv')

class SettingsScreen(Screen):
	data = ListProperty()
	
	def __init__(self, **kwargs):
		super(SettingsScreen, self).__init__(**kwargs)
		self.data = []
	
	def save(self):
		print('\nSave stuffes!\n')

	def update_data(self, data):
		self.data = data