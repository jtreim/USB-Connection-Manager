import kivy
kivy.require('1.10.1')

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file('screens/settings/display.kv')

class SettingsScreen(Screen):
	pass