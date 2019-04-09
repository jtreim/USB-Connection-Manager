import kivy
kivy.require('1.10.1')

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

from app.views.device_rv.device_rv import DeviceRV

Builder.load_file('app/screens/test/display.kv')

class TestScreen(Screen):
    pass