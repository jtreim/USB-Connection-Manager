import kivy
kivy.require('1.10.1')

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_file('screens/add_device/display.kv')

class AddDeviceScreen(Screen):
	pass