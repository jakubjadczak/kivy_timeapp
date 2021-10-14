from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import BooleanProperty


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

    def start_button(self):
        self.stop_disabled = False
        self.start_disabled = True
        self.save_disabled = True
        self.micro_sec_event = Clock.schedule_interval(self.micro_sec, 0.01,)
        #self.sec_event = Clock.schedule_interval(self.sec, 1)
        #self.min_event = Clock.schedule_interval(self.minute, 60)
        #self.hours_event = Clock.schedule_interval(self.hours, 3600)

    def stop_button(self):
        self.start_disabled = False
        self.stop_disabled = True
        self.save_disabled = False
        Clock.unschedule(self.micro_sec_event)
        #Clock.unschedule(self.sec_event)
        #Clock.unschedule(self.min_event)
        #Clock.unschedule(self.hours_event)

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
    def click(self):
        print('ok')

    def validate(self):
        in_put = self.ids.input_1.text
        return in_put


class BoxLayout_1(BoxLayout):
    pass


class WatchApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Timer(name='timer'))
        sm.add_widget(TimeCounter(name='time_counter'))
        return sm


if __name__ == '__main__':
    WatchApp().run()





