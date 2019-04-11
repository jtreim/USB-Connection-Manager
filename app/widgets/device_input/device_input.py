import kivy
kivy.require('1.10.1')

from kivy.lang import Builder
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty

Builder.load_file('app/widgets/device_input/display.kv')

class DeviceInput(RecycleDataViewBehavior, BoxLayout):
    index = None
    device_id = StringProperty()
    device_name = StringProperty()
    device_active = BooleanProperty()
    device_action = StringProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(DeviceInput, self).refresh_view_attrs(rv, index, data)
