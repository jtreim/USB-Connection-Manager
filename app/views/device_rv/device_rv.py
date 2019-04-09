import kivy
kivy.require('1.10.1')

from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView

from app.widgets.device_input.device_input import DeviceInput

Builder.load_file('app/views/device_rv/display.kv')

class DeviceRV(RecycleView):
    pass

