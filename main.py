from tekken_docs import TekkenDocs
from functools import partial
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import AsyncImage
from kivy.uix.button import ButtonBehavior
from kivy.properties import StringProperty
from kivy.uix.gridlayout import GridLayout

TEKKEN_DOCS = TekkenDocs()
CHARACTERS = TEKKEN_DOCS.get_character_data()


class ImageButton(ButtonBehavior, AsyncImage):
    pass

class TekkenGridLayout(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols=3
        self.padding=[0,0,0,0]
    
    def on_kv_post(self, base_widget):
        super().on_kv_post(base_widget)
        for character in CHARACTERS:
            image = character["image_link"]
            new_button = ImageButton(source=image)
            new_button.bind(on_press=partial(self.go_to_second_screen, character["link"]))
            self.add_widget(new_button)
    
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
