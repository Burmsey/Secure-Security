from kivy.app import App
from kivy.lang import Builder

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
                    print("Start Camera button pressed!")
                background_normal: ''
                background_color: 0.2, 0.6, 1, 1
            Button:
                text: "View Captures"
                font_size: 24
                on_release:
                    print("View Captures button pressed!")
                background_normal: ''
                background_color: 0.2, 0.6, 1, 1

'''

class SimpleHomeApp(App):
    def build(self):
        return Builder.load_string(KV)

if __name__ == "__main__":
    SimpleHomeApp().run()
