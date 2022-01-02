from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import BooleanProperty, StringProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from database import DataBase
from kivy.uix.recycleview import RecycleView


class SavePopup(Popup):
    """
    Class displaying popup window and saving time with title in db
    after clicking save button
    """
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
        self.hrs = str(obj.hrs_l)
        self.T.append(self.hrs)
        self.T.append(self.min)
        self.T.append(self.sec)
        self.T.append(self.micro_sec)
        self.time = ' : '.join(self.T)
        self.background_color = (1, 1, 1, .5)

    def save_button(self):
        """
        Run after click save button
        :return: new row in database
        """
        name = self.ids.time_name.text
        if name == '':
            pass
        else:
            db = DataBase()
            db.insert(name, self.hrs, self.min, self.sec, self.micro_sec)
            self.dismiss()


class Timer(Screen):
    """
    First window, time measuring
    """
    Window.clearcolor = (97/255, 97/255, 101/255, 1)
    stop_disabled = BooleanProperty(True)
    start_disabled = BooleanProperty(False)
    save_disabled = BooleanProperty(True)
    stop_reset = StringProperty('Stop')

    def __init__(self):
        super(Timer, self).__init__(name='timer')
        self.micro_l = 0
        self.sec_l = 0
        self.min_l = 0
        self.hrs_l = 0
        self.reset = False

    def on_pre_enter(self, *args):
        self.stop_disabled = True
        self.start_disabled = False
        self.micro_l = 0
        self.sec_l = 0
        self.min_l = 0
        self.hrs_l = 0
        self.ids.hrs_l.text = '0'
        self.ids.min_l.text = '0'
        self.ids.sec_l.text = '0'
        self.ids.micro_sec_l.text = '0'
        self.reset = False

    def reset_button(self):
        self.save_disabled = True
        self.ids.hrs_l.text = '0'
        self.ids.min_l.text = '0'
        self.ids.sec_l.text = '0'
        self.ids.micro_sec_l.text = '0'
        self.micro_l = 0
        self.sec_l = 0
        self.min_l = 0
        self.hrs_l = 0

    def start_button(self):
        self.stop_disabled = False
        self.start_disabled = True
        self.save_disabled = True
        self.stop_reset = 'Stop'
        self.reset = False
        self.micro_sec_event = Clock.schedule_interval(self.micro_sec, 0.01)

    def stop_button(self):
        self.start_disabled = False
        self.stop_disabled = False
        self.save_disabled = False
        self.stop_reset = 'Reset'
        if (self.micro_l > 0 or self.sec_l > 0 or self.min_l > 0 or self.hrs_l > 0) and self.reset:
            self.reset_button()
        self.reset = True
        Clock.unschedule(self.micro_sec_event)

    def save_button(self):
        popup = SavePopup(self)
        popup.open()

    def micro_sec(self, *args):
        """
        Function calls for 0.01 sec from 'start_button', running 'sec'
        :param args:
        :return:
        """
        self.micro_l += 1
        self.ids.micro_sec_l.text = str(self.micro_l)
        if self.micro_l == 99:
            self.sec()
            self.micro_l = 0

    def sec(self):
        self.sec_l += 1
        self.ids.sec_l.text = str(self.sec_l)
        if self.sec_l == 59:
            self.minute()
            self.sec_l = 0

    def minute(self):
        self.min_l += 1
        self.ids.min_l.text = str(self.min_l)
        if self.min_l == 60:
            self.hours()
            self.min_l = 0

    def hours(self):
        self.hrs_l += 1
        self.ids.hrs_l.text = str(self.hrs_l)


class EndPopup(Popup):
    """
    Popup displaying when time's up, class count time since time is over
    this time is displaying in this popup, user can stop counting clicking button
    """
    def __init__(self):
        super().__init__()
        self.background_color = (1, 1, 1, .5)
        self.micro_l = 0
        self.sec_l = 0
        self.min_l = 0
        self.hrs_l = 0
        self.event = Clock.schedule_interval(self.micro_sec, 0.01)

    def ok_button(self):
        Clock.unschedule(self.event)

    def micro_sec(self, *args):
        self.micro_l += 1
        self.ids.micro_sec_l.text = str(self.micro_l)
        if self.micro_l == 99:
            self.sec()
            self.micro_l = 0

    def sec(self):
        self.sec_l += 1
        self.ids.sec_l.text = str(self.sec_l)
        if self.sec_l == 59:
            self.minute()
            self.sec_l = 0

    def minute(self):
        self.min_l += 1
        self.ids.min_l.text = str(self.min_l)
        if self.min_l == 60:
            self.hours()
            self.min_l = 0

    def hours(self):
        self.hrs_l += 1
        self.ids.hrs_l.text = str(self.hrs_l)


class TimeCounter(Screen):
    """
    Window, setting time and countdown after click start button
    """
    reset_akt = BooleanProperty(True)
    stop_disabled = BooleanProperty(True)
    start_disabled = BooleanProperty(False)
    save_disabled = BooleanProperty(True)

    def __init__(self):
        super(TimeCounter, self).__init__(name='time_counter')
        self.hrs = 0
        self.min = 0
        self.sec = 0

    def on_pre_enter(self, *args):
        self.stop_disabled = True
        self.reset_akt = True

    def start_button(self):
        self.start_disabled = True
        self.stop_disabled = False
        self.reset_akt = True
        self.hrs = int(self.ids.hrs_set.text)
        self.min = int(self.ids.min_set.text)
        self.sec = int(self.ids.sec_set.text)
        self.event = Clock.schedule_interval(self.count_down, 1)

    def count_down(self, *args):
        if self.sec > 0:
            self.sec -= 1
        elif self.min > 0:
            self.min -= 1
            self.sec = 59
        elif self.hrs > 0:
            self.min = 60
            self.hrs -= 1

        self.ids.hrs_set.text = str(self.hrs)
        self.ids.min_set.text = str(self.min)
        self.ids.sec_set.text = str(self.sec)

        if self.sec == 0 and self.min == 0 and self.hrs == 0:
            self.stop_button()
            self.time_end()

    @staticmethod
    def time_end():
        popup = EndPopup()
        popup.open()

    def stop_button(self):
        Clock.unschedule(self.event)
        self.stop_disabled = True
        self.start_disabled = False
        self.save_disabled = False
        self.reset_akt = False

    def reset_button(self):
        self.stop_button()
        self.reset_akt = True
        self.ids.hrs_set.text = '0'
        self.ids.min_set.text = '0'
        self.ids.sec_set.text = '0'

    def hour_up(self):
        """
        Functions used to setting time by user on app's screen
        """
        h = self.ids.hrs_set.text
        h = int(h) + 1
        self.ids.hrs_set.text = str(h)

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
        h = self.ids.hrs_set.text
        if h != '0':
            h = int(h) - 1
        self.ids.hrs_set.text = str(h)

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


class EditPopup(Popup):
    """
    Popup displaying after clicking on row, user can edit only the title
    """
    obj = ObjectProperty(None)
    name = StringProperty('')
    time_name = StringProperty('')
    idt = StringProperty('')

    def __init__(self, obj, **kwargs):
        super(EditPopup, self).__init__(**kwargs)
        self.obj = obj
        self.name = obj.text
        self.background_color = (1, 1, 1, .5)
        T = self.name.split()
        for t in T:
            if t == ':':
                T.remove(t)
        self.time_name = T[1]
        self.idt = T[0]


"""
Classes below are taking part in Recycle View
"""


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    """ Adds selection and focus behaviour to the view. """


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
        self.idt = popup.idt
        popup.open()

    def update_changes(self, name):
        db = DataBase()
        db.edit_by_id(self.idt, name)
        self.text = db.reading_one(self.idt)
        # print(self.idt, name)

    def delete(self):
        db = DataBase()
        db.delete_by_id(self.idt)
        self.text = ''


class RV(RecycleView, Screen):

    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.words = []

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


class BoxLayout_1(BoxLayout):
    pass


class WatchApp(App):
    ui_color = StringProperty([0, 183 / 255, 135 / 255, 1])

    def build(self):
        sm = ScreenManager()
        sm.add_widget(Timer())
        sm.add_widget(TimeCounter())
        sm.add_widget(RV(name='time_table'))
        return sm


if __name__ == '__main__':
    WatchApp().run()
