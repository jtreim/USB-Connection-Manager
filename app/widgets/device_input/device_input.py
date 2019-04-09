import kivy
kivy.require('1.10.1')

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty

Builder.load_file('app/widgets/device_input/display.kv')

class DeviceInput(BoxLayout):
    device_id = StringProperty()
    device_active = BooleanProperty()
    device_action = StringProperty()
