from kivy.app import App
from kivy.lang import Builder
import camDetect
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
import camDetect
import os
import threading

KV = '''
FloatLayout:

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
        size_hint: 1, 1

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

        BoxLayout:
            orientation: 'horizontal'
            spacing: 50
            padding: (100, 0, 100, 50)

            Button:
                text: "Next Cam"
                font_size: 24
                on_release:
                    app.set_variable(True)

            Button:
                text: "Previous Cam"
                font_size: 24
                on_release:
                    app.set_variable(False)
'''

class FileExplorer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
         
        dir_path = os.path.dirname(os.path.realpath(__file__))
        if(os.path.exists(dir_path)):
            self.file_chooser = FileChooserListView(
                path=os.getcwd(),
                filters=["*.mp4"],
            )
            print("assets found!")
        else:
            print("assets not found!\ncheck your directory")
        self.add_widget(self.file_chooser)


class SimpleHomeApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cam_index = 0
        self.close_cam = False

    def build(self):
        return Builder.load_string(KV)

    def init(self):
        self.close_cam = False
        threading.Thread(
            target=camDetect.init,
            args=(self.cam_index,),
            kwargs={'should_close': lambda: self.close_cam},
            daemon=True
        ).start()

    def open_file_explorer(self):
        content = FileExplorer()
        popup = Popup(title="Choose a file", content=content,
                      size_hint=(0.9, 0.9))
        popup.open()

    def set_variable(self, next_cam):
        if next_cam:
            self.cam_index += 1
            self.close_cam = True  # Signal to close camera loop
        else:
            self.cam_index = max(0, self.cam_index - 1)
            self.close_cam = True  # Signal to close camera loop
        print(f"Switching to camera index: {self.cam_index}")
        # Start new camera after closing old one
        self.init()
 
if __name__ == "__main__":
    SimpleHomeApp().run()
