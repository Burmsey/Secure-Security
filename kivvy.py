from kivy.app import App
from kivy.lang import Builder
import camDetect
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup

KV = '''
FloatLayout:
    id: main_layout

    Image:
        source: 'Assets/secure security background.png'
        allow_stretch: True
        keep_ratio: False
        size: self.size
        pos: self.pos

    BoxLayout:
        orientation: 'vertical'
        spacing: 0
        padding: (50, 50, 50, 0)
        size_hint: 1, 1  # fill the screen

        Label:
            text: "Secure Security"
            font_size: 100

        BoxLayout:  
            orientation: 'horizontal'
            spacing: 50
            padding: (100, 0, 100, 200)

            Button:
                text: "Start Camera"
                font_size: 24
                on_release:
                    app.init()
                background_normal: ''
                background_color: 0.2, 0.6, 1, 1

            Button:
                text: "View Captures"
                font_size: 24
                on_release:
                    app.open_file_explorer()
                background_normal: ''
                background_color: 0.2, 0.6, 1, 1
'''

class FileExplorer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.file_chooser = FileChooserListView(
            path=r"C:\Users\joehu\Code Projects\School Projects\Secure-Security",  # Change this to your folder
            filters=["*.mp4"],  #files types user can see
        )

        self.add_widget(self.file_chooser)


class SimpleHomeApp(App):
    def build(self):
        return Builder.load_string(KV)

    def init(self):
        camDetect.init()

    def open_file_explorer(self):
        content = FileExplorer()
        popup = Popup(title="Choose a file", content=content,
                      size_hint=(0.9, 0.9))
        popup.open()

if __name__ == "__main__":
    SimpleHomeApp().run()

