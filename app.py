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

from screens.add_device.add_device import AddDeviceScreen
from screens.settings.settings import SettingsScreen  

Config.set('graphics', 'width', 400)
Config.set('graphics', 'height', 200)

class StreamerApp(App):
	def build(self):
		# Registering a new device screen
		device_screen = AddDeviceScreen(name='add_device')

		# Settings screen
		settings_screen = SettingsScreen(name='settings')

		# Add screens to screen manager
		sm = ScreenManager()
		sm.add_widget(device_screen)
		sm.add_widget(settings_screen)
		return sm

if __name__ == '__main__':
	StreamerApp().run()
