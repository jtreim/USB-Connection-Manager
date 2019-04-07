import kivy
kivy.require('1.10.1')

from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView

from widgets.device_input.device_input import DeviceInput

Builder.load_file('views/device_rv/display.kv')

class DeviceRV(RecycleView):
    def __init__(self, **kwargs):
        super(DeviceRV, self).__init__(**kwargs)
        self.data = [{'device_id': 'Test_id', 'device_active': True, 'device_action': 'none'},
                     {'device_id': 'Test_id2', 'device_active': False, 'device_action': 'none'},
                     {'device_id': 'Test_id3', 'device_active': True, 'device_action': 'none'},
                     {'device_id': 'Test_id4', 'device_active': True, 'device_action': 'none'},
                     {'device_id': 'Test_id5', 'device_active': False, 'device_action': 'none'},
                     {'device_id': 'Test_id6', 'device_active': False, 'device_action': 'none'},
                     {'device_id': 'Test_id7', 'device_active': False, 'device_action': 'none'},
                     {'device_id': 'Test_id8', 'device_active': False, 'device_action': 'none'},
                     {'device_id': 'Test_id9', 'device_active': True, 'device_action': 'none'},
                     {'device_id': 'Test_id10', 'device_active': True, 'device_action': 'none'},
                     {'device_id': 'Test_id11', 'device_active': False, 'device_action': 'none'},
                     {'device_id': 'Test_id12', 'device_active': True, 'device_action': 'none'},]

