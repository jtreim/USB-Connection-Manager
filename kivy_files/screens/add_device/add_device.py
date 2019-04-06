import kivy
kivy.require('1.10.1')

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

Builder.load_file('kivy_files/screens/add_device/display.kv')

class AddDeviceScreen(Screen):
	add_device_id = StringProperty()
