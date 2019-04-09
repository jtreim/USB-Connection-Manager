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

from screens.test.test import TestScreen

Config.set('graphics', 'width', 600)
Config.set('graphics', 'height', 300)

class TestApp(App):
    def build(self):
        self.title = 'Test App'

        # Add screens to screen manager
        sm = ScreenManager()
        sm.add_widget(TestScreen(name='test'))
        return sm

if __name__=='__main__':
    TestApp().run()