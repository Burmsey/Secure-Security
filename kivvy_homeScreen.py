from kivy.app import App
from kivy.lang import Builder
import camDetect
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
import camDetect
import os
import threading
from kivy.properties import NumericProperty
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

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
        padding: (50, 0, 50, 10)
        size_hint: 1, 1

        Label:
            text: "Secure Security"
            font_size: 100

        BoxLayout:  
            orientation: 'horizontal'
            spacing: 5
            padding: (100, 100, 100, 5)

            Button:
                text: "Start Camera: {}".format(app.cam_index + 1)
                font_size: 24
                on_release:
                    app.init()
                background_normal: ''
                background_color: 0.2, 0.6, 1, 1
        
        BoxLayout:
            orientation: 'horizontal'
            spacing: 70
            padding: (100, 0, 100, 150)
            # up left right down

            Button:
                text: "Next Cam"
                font_size: 24
                on_release:
                    app.set_variable(True)
                background_normal: ''
                background_color: 0, 0, 0, 1

            Button:
                text: "Previous Cam"
                font_size: 24
                on_release:
                    app.set_variable(False)
                background_normal: ''
                background_color: 0, 0, 0, 1
            Button:
                text: "Revert to Cam: 1"
                font_size: 24
                on_release:
                    app.revert_to_first_cam()
                background_normal: ''
                background_color: 0, 0, 0, 1

        BoxLayout:
            orientation: 'horizontal'
            spacing: 100
            padding: (100, 0, 100, 100)

            Button:
                text: "View Captures"
                font_size: 24
                on_release:
                    app.open_file_explorer()
                background_normal: ''
                background_color: 0.2, 0.6, 1, 1

            Button:
                text: "How To View Captures"
                font_size: 24
                on_release:
                    app.capture_info()
                background_normal: ''
                background_color: 0.2, 0.6, 1, 1
'''


class FileExplorer(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.file_chooser = FileChooserListView(
            path=os.getcwd(),
            filters=["*.mp4"],
        )
        self.file_chooser.bind(on_submit=self.open_file)  # auto open on double-click
        self.add_widget(self.file_chooser)

    def open_file(self, filechooser, selection, touch):
        if selection:
            selected_file = selection[0]
            print(f"Opening file: {selected_file}")
            os.startfile(selected_file)

class SimpleHomeApp(App):

    cam_index = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
    
    def revert_to_first_cam(self):
        self.cam_index = 0
        self.close_cam = True  # Signal to close current camera loop if running
    
    def capture_info(self):
        messagebox.showinfo("Info", "Open Capture Menu By Clicking 'View Captures'. Then Double Click A .mp4 File To View")

if __name__ == "__main__":
    SimpleHomeApp().run()
