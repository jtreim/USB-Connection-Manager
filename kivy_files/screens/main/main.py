import kivy
kivy.require('1.10.1')

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

Builder.load_file('screens/main/display.kv')

class MainScreen(Screen):
	subtitle = StringProperty()
	msg = StringProperty()
