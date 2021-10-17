from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import BooleanProperty, StringProperty, ObjectProperty
from kivy.uix.popup import Popup


class SavePopup(Popup):
    obj = ObjectProperty(None)
    micro_sec = StringProperty('')
    sec = StringProperty('')
    min = StringProperty('')
    hrs = StringProperty('')
    time = StringProperty('')

    def __init__(self, obj, **kwargs):
        super(SavePopup, self).__init__(**kwargs)
        self.T = []
        self.obj = obj
        self.micro_sec = str(obj.micro_l)
        self.sec = str(obj.sec_l)
        self.min = str(obj.min_l)
        self.hrs = str(obj.hours_l)
        self.T.append(self.hrs)
        self.T.append(self.min)
        self.T.append(self.sec)
        self.T.append(self.micro_sec)
        self.time = ' : '.join(self.T)
        self.background_color = (255, 255, 255, 1)


class Timer(Screen):
    Window.clearcolor = (1, 1, 1, 1)
    stop_disabled = BooleanProperty(True)
    start_disabled = BooleanProperty(False)
    save_disabled = BooleanProperty(True)

    def on_pre_enter(self, *args):
        self.stop_disabled = True
        self.start_disabled = False
        self.micro_l = 0
        self.sec_l = 0
        self.min_l = 0
        self.hours_l = 0

    def reset_button(self):
        self.stop_button()
        self.ids.hours_l.text = '0'
        self.ids.min_l.text = '0'
        self.ids.sec_l.text = '0'
        self.ids.micro_sec_l.text = '0'

    def start_button(self):
        self.stop_disabled = False
        self.start_disabled = True
        self.save_disabled = True
        self.micro_sec_event = Clock.schedule_interval(self.micro_sec, 0.01)


    def stop_button(self):
        self.start_disabled = False
        self.stop_disabled = True
        self.save_disabled = False
        Clock.unschedule(self.micro_sec_event)

    def save_button(self):
        popup = SavePopup(self)
        popup.open()

    def micro_sec(self, *args):
        self.micro_l += 1
        self.ids.micro_sec_l.text = str(self.micro_l)
        if self.micro_l == 99:
            self.sec()
            self.micro_l = 0

    def sec(self, *args):
        self.sec_l += 1
        self.ids.sec_l.text = str(self.sec_l)
        if self.sec_l == 59:
            self.minute()
            self.sec_l = 0

    def minute(self, *args):
        self.min_l += 1
        self.ids.min_l.text = str(self.min_l)
        if self.min_l == 60:
            self.hours()
            self.min_l = 0

    def hours(self, *args):
        self.hours_l += 1
        self.ids.hours_l.text = str(self.hours_l)


class EndPopup(Popup):
    def __init__(self):
        super().__init__()
        self.background_color = (255, 255, 255, 1)
        self.micro_l = 0
        self.sec_l = 0
        self.min_l = 0
        self.hours_l = 0
        self.event = Clock.schedule_interval(self.micro_sec, 0.01)

    def ok_button(self):
        Clock.unschedule(self.event)

    def micro_sec(self, *args):
        self.micro_l += 1
        self.ids.micro_sec_l.text = str(self.micro_l)
        if self.micro_l == 99:
            self.sec()
            self.micro_l = 0

    def sec(self, *args):
        self.sec_l += 1
        self.ids.sec_l.text = str(self.sec_l)
        if self.sec_l == 59:
            self.minute()
            self.sec_l = 0

    def minute(self, *args):
        self.min_l += 1
        self.ids.min_l.text = str(self.min_l)
        if self.min_l == 60:
            self.hours()
            self.min_l = 0

    def hours(self, *args):
        self.hours_l += 1
        self.ids.hours_l.text = str(self.hours_l)


class TimeCounter(Screen):
    stop_disabled = BooleanProperty(True)
    start_disabled = BooleanProperty(False)
    save_disabled = BooleanProperty(True)

    def on_pre_enter(self, *args):
        self.stop_disabled = True

    def start_button(self):
        self.start_disabled = True
        self.stop_disabled = False
        self.h = int(self.ids.hours_set.text)
        self.m = int(self.ids.min_set.text)
        self.s = int(self.ids.sec_set.text)
        self.event = Clock.schedule_interval(self.count_down, 1)

    def count_down(self, *args):

        if self.s > 0:
            self.s -= 1
        elif self.m > 0:
            self.m -= 1
            self.s = 59
        elif self.h > 0:
            self.m = 60
            self.h -= 1

        self.ids.hours_set.text = str(self.h)
        self.ids.min_set.text = str(self.m)
        self.ids.sec_set.text = str(self.s)

        if self.s == 0 and self.m == 0 and self.h == 0:
            self.stop_button()
            self.time_end()

    def time_end(self):
        popup = EndPopup()
        popup.open()

    def stop_button(self):
        Clock.unschedule(self.event)
        self.stop_disabled = True
        self.start_disabled = False
        self.save_disabled = False

    def reset_button(self):
        self.stop_button()
        self.ids.hours_set.text = '0'
        self.ids.min_set.text = '0'
        self.ids.sec_set.text = '0'

    def hour_up(self):
        h = self.ids.hours_set.text
        h = int(h) + 1
        self.ids.hours_set.text = str(h)

    def min_up(self):
        m = self.ids.min_set.text
        if m == '59':
            self.hour_up()
            self.ids.min_set.text = '0'
        else:
            m = int(m) + 1
            self.ids.min_set.text = str(m)

    def sec_up(self):
        s = self.ids.sec_set.text
        if s == '59':
            self.min_up()
            self.ids.sec_set.text = '0'
        else:
            s = int(s) + 1
            self.ids.sec_set.text = str(s)

    def hours_down(self):
        h = self.ids.hours_set.text
        if h != '0':
            h = int(h) - 1
        self.ids.hours_set.text = str(h)

    def min_down(self):
        m = self.ids.min_set.text
        if m != '0':
            m = int(m) - 1
        self.ids.min_set.text = str(m)

    def sec_down(self):
        s = self.ids.sec_set.text
        if s != '0':
            s = int(s) - 1
        self.ids.sec_set.text = str(s)


class TimeTable(Screen):
    pass


class BoxLayout_1(BoxLayout):
    pass


class WatchApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Timer(name='timer'))
        sm.add_widget(TimeCounter(name='time_counter'))
        sm.add_widget(TimeTable(name='time_table'))
        return sm


if __name__ == '__main__':
    WatchApp().run()





