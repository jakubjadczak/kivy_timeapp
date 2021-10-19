from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import BooleanProperty, StringProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget

from kivy.uix.button import Button
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from database import DataBase
from kivy.uix.recycleview import RecycleView


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

    def save_button(self):
        name = self.ids.time_name.text
        db = DataBase()
        db.insert(name, self.hrs, self.min, self.sec, self.micro_sec)
        self.dismiss()


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


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """


class EditPopup(Popup):
    obj = ObjectProperty(None)
    name = StringProperty('')
    time_name = StringProperty('')
    idt = StringProperty('')

    def __init__(self, obj, **kwargs):
        super(EditPopup, self).__init__(**kwargs)
        self.obj = obj
        self.name = obj.text
        self.background_color = (255, 255, 255, 1)
        print(type(self.name), self.name)
        T = self.name.split()
        for t in T:
            if t == ':':
                T.remove(t)
        self.time_name = T[1]
        self.idt = T[0]



class SelectableButton(RecycleDataViewBehavior, Button):
    """ Add selection support to the Label """

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """ Catch and handle the view changes """
        self.index = index
        return super(SelectableButton, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        """ Add selection on touch down """
        if super(SelectableButton, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """ Respond to the selection of items in the view. """
        self.selected = is_selected

    def on_press(self):
        popup = EditPopup(self)
        print(popup.name)
        print(popup.time_name, popup.idt)
        popup.open()

    def update_changes(self, idt, name):
        pass


class RV(RecycleView, Screen):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

    def set_data(self):
        db = DataBase()
        self.words = db.reading_all()
        d = [{'text': str(self.words[i][0]) + '       ' + str(self.words[i][1]) + '      '
                      + str(self.words[i][2]) + '  :  ' + str(self.words[i][3]) + '  :  ' + str(
            self.words[i][4]) + '  :  ' + str(self.words[i][5])
              } for i in range(len(self.words))]
        return d

    def refresh_view(self):
        self.ids.rv_view.data = self.set_data()
        self.ids.rv_view.refresh_from_data()


class RVTimeTable(Screen):
    pass



class BoxLayout_1(BoxLayout):
    pass


class WatchApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Timer(name='timer'))
        sm.add_widget(TimeCounter(name='time_counter'))
        sm.add_widget(RV(name='time_table'))
        return sm


if __name__ == '__main__':
    WatchApp().run()





