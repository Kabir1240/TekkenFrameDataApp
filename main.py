from tekken_docs import TekkenDocs
from functools import partial
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import AsyncImage
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

TEKKEN_DOCS = TekkenDocs()
# LABEL_PADDING = [0, "150dp", 0, 0]
LABEL_SIZE = 100
TEXT_SIZE = 80


class SyncedScrollView(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sync_view = None
    
    def on_scroll_move(self, touch):
        if self.sync_view:
            self.sync_view.scroll_x = self.scroll_x
        super().on_scroll_move(touch)

            
class ImageButton(ButtonBehavior, AsyncImage):
    pass


class CharacterIconLayout(GridLayout):
    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        
        characters = TEKKEN_DOCS.get_character_data()
        for character in characters:
            # get character details
            name = character["name"].title()
            image_link = character["image_link"]
            link = character["link"]
            
            # create box layout
            new_box_layout = BoxLayout(orientation="vertical", size_hint=(.1,.1))
            
            # create and add character image and name
            new_button = ImageButton(source=image_link, size_hint_y=.9)
            new_button.bind(on_press=partial(self.go_to_second_screen, link))
            new_label = Label(text=name, size_hint_y=.1)
            new_box_layout.add_widget(new_button)
            new_box_layout.add_widget(new_label)
            
            # add boxlayout to the TekkenGridLayout
            self.add_widget(new_box_layout)
    
    def go_to_second_screen(self, link, instance):
        self.screenmanager.get_screen('second').data = link
        self.screenmanager.transition.direction = 'left'
        self.screenmanager.current = 'second'


# Define the screens
class FirstScreen(Screen):
    pass


class SecondScreen(Screen):
    data = StringProperty('')
    
    def on_enter(self, *args):
        super().on_enter(*args)
        self.link_scroll_views()
        self.display_moveset()
        
    def link_scroll_views(self):
        header_scrollview = self.ids.header_scrollview
        content_scrollview = self.ids.content_scrollview
        
        header_scrollview.sync_view = content_scrollview
        content_scrollview.sync_view = header_scrollview

    def display_moveset(self):
        moveset = TEKKEN_DOCS.get_character_moveset(self.data)
        content_grid = self.ids.content_grid
        for move in moveset:
            command_label = Label(
                                    text=move["command"], 
                                    size_hint_x=None,
                                    width=LABEL_SIZE,
                                    text_size=(TEXT_SIZE, None),
                                    halign='center',
                                    valign='center')
            hit_level_label = Label(
                                    text=move["hit level"],
                                    size_hint_x=None,
                                    width=LABEL_SIZE,
                                    text_size=(TEXT_SIZE, None),
                                    halign='center',
                                    valign='center')
            damage_label = Label(
                                    text=move["damage"],
                                    size_hint_x=None,
                                    width=LABEL_SIZE,
                                    text_size=(TEXT_SIZE, None),
                                    halign='center',
                                    valign='center')
            startup_label = Label(
                                    text=move["startup"], 
                                    size_hint_x=None,
                                    width=LABEL_SIZE,
                                    text_size=(TEXT_SIZE, None),
                                    halign='center',
                                    valign='center')
            block_label = Label(text=
                                    move["block"], 
                                    size_hint_x=None,
                                    width=LABEL_SIZE,
                                    text_size=(TEXT_SIZE, None),
                                    halign='center',
                                    valign='center')
            
            hit_label = Label(
                                    text=move["hit"],
                                    size_hint_x=None,
                                    width=LABEL_SIZE,
                                    text_size=(TEXT_SIZE, None),
                                    halign='center',
                                    valign='center')
            counter_label = Label(text=                  
                                    move["counter hit"], 
                                    size_hint_x=None,
                                    width=LABEL_SIZE,
                                    text_size=(TEXT_SIZE, None),
                                    halign='center',
                                    valign='center')
            
            notes = ""
            for note in move["notes"]:
                notes += note + "\n"
            notes_label = Label(
                                    text=notes,
                                    size_hint_x=None,
                                    size_hint_y=None,
                                    height="45dp",
                                    width=400,
                                    text_size=(400, None),
                                    halign='center',
                                    valign='center')
            
            content_grid.add_widget(command_label)
            content_grid.add_widget(hit_level_label)
            content_grid.add_widget(damage_label)
            content_grid.add_widget(startup_label)
            content_grid.add_widget(block_label)
            content_grid.add_widget(hit_label)
            content_grid.add_widget(counter_label)
            content_grid.add_widget(notes_label)


# Define the screen manager
class MyScreenManager(ScreenManager):
    pass


class TekkenFrameData(App):
        def build(self):
            sm = MyScreenManager()
            first_screen = FirstScreen()
            second_screen = SecondScreen()

            # Bind the data property from first screen to second screen
            second_screen.bind(data=first_screen.setter('data'))
            
            # add screens
            sm.add_widget(first_screen)
            sm.add_widget(second_screen)

            # Bind the back button press
            Window.bind(on_key_down=self.on_back_button)
            return sm

        
        def on_back_button(self, window, key, *args):
            if key == 27:
                sm = self.root
                if sm.current == 'second':
                    self.switch_to_first_screen(sm)
                    return True
            return False
        
        
        def switch_to_first_screen(self, sm):
            sm.transition.direction = 'right'
            sm.current = 'first'
            sm.remove_widget(sm.get_screen('second'))


TekkenFrameData().run()
