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

TEKKEN_DOCS = TekkenDocs()


class ImageButton(ButtonBehavior, AsyncImage):
    pass

class TekkenGridLayout(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols=3
        self.padding=[0,0,0,0]
        self.spacing=10
    
    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        
        characters = TEKKEN_DOCS.get_character_data()
        for character in characters:
            # get character details
            name = character["name"].title()
            image_link = character["image_link"]
            link = character["link"]
            
            # create box layout
            new_box_layout = BoxLayout(orientation="vertical")
            
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
        self.screenmanager.current = 'second'

# Define the screens
class FirstScreen(Screen):
    pass

class SecondScreen(Screen):
    data = StringProperty('')
    
    def on_enter(self, *args):
        pass

# Define the screen manager
class MyScreenManager(ScreenManager):
    pass

class TekkenFrameData(App):
        def build(self):
            sm = MyScreenManager()
            first_screen = FirstScreen(name='first')
            second_screen = SecondScreen(name='second')

            # Bind the data property from first screen to second screen
            second_screen.bind(data=first_screen.setter('data'))
            
            # add screens
            sm.add_widget(first_screen)
            sm.add_widget(second_screen)

            sm.current='first'
            return sm


TekkenFrameData().run()
