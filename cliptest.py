from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.clipboard import Clipboard


class ClipboardApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.input_text = TextInput(hint_text='Enter text to copy', multiline=True)
        layout.add_widget(self.input_text)

        copy_button = Button(text='Copy to Clipboard', size_hint_y=None, height=50)
        copy_button.bind(on_press=self.copy_to_clipboard)
        layout.add_widget(copy_button)

        return layout

    def copy_to_clipboard(self, instance):
        Clipboard.copy(self.input_text.text)
        print("Text copied to clipboard:", self.input_text.text)


if __name__ == '__main__':
    ClipboardApp().run()
