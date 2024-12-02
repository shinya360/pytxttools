from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from translate import Translator
from gtts import gTTS
import pygame
import tempfile
import os
import speech_recognition as sr
import threading
from kivy.clock import Clock

# Load the .kv file
#Builder.load_file('test.kv')

class TestTranslatorApp(App):
    def build(self):
        pygame.mixer.init()  # Initialize pygame mixer
        container = Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    padding: 10
    spacing: 10

    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10

        BoxLayout:
            size_hint_y: None
            height: 300  # Increased height for better centering
            Label:
                text: 'English to Spanish'
                font_size: 100
                halign: 'center'
                valign: 'middle'
                text_size: self.size

        TextInput:
            id: en_input_text
            hint_text: 'Enter English text here'
            multiline: True
            size_hint_y: None
            height: 100

        TextInput:
            id: es_output_text
            hint_text: 'Spanish translation will appear here'
            multiline: True
            size_hint_y: None
            height: 100

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 100  # Increased height for buttons
            spacing: 10

            Button:
                id: en_to_es_speak_button
                text: 'Speak Translation'
                background_normal: ''
                background_color: (0.2, 0.6, 1, 1)
                border: (20, 20, 20, 20)
                on_press: app.speak_es_translation(self)

            Button:
                id: en_to_es_translate_button
                text: 'Translate to Spanish'
                background_normal: ''
                background_color: (0.2, 0.6, 1, 1)
                border: (20, 20, 20, 20)
                on_press: app.translate_en_to_es(self)

            Button:
                id: en_to_es_mic_button
                text: 'Mic Input(EN)'
                background_normal: ''
                background_color: (0.2, 0.6, 1, 1)
                border: (20, 20, 20, 20)
                on_press: app.listen_english(self)

            Button:
                id: copy_spanish_button
                text: 'Copy to Clipboard'
                background_normal: ''
                background_color: (0.2, 0.6, 1, 1)
                border: (20, 20, 20, 20)
                on_press: app.copy_spanish(self)

            Button:
                id: paste_english_button
                text: 'Paste'
                background_normal: ''
                background_color: (0.2, 0.6, 1, 1)
                border: (20, 20, 20, 20)
                on_press: app.paste_english(self)
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10

        BoxLayout:
            size_hint_y: None
            height: 300  # Increased height for better centering
            Label:
                text: 'Spanish to English'
                font_size: 100
                halign: 'center'
                valign: 'middle'
                text_size: self.size

        TextInput:
            id: es_input_text
            hint_text: 'Enter Spanish text here'
            multiline: True
            size_hint_y: None
            height: 100

        TextInput:
            id: en_output_text
            hint_text: 'English translation will appear here'
            multiline: True
            size_hint_y: None
            height: 100

        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 100  # Increased height for buttons
            spacing: 10

            Button:
                id: es_to_en_speak_button
                text: 'Speak Translation'
                background_normal: ''
                background_color: (0.2, 0.6, 1, 1)
                border: (20, 20, 20, 20)
                on_press: app.speak_en_translation(self)

            Button:
                id: es_to_en_translate_button
                text: 'Translate to English'
                background_normal: ''
                background_color: (0.2, 0.6, 1, 1)
                border: (20, 20, 20, 20)
                on_press: app.translate_es_to_en(self)

            Button:
                id: es_to_en_mic_button
                text: 'Mic Input(ES)'
                background_normal: ''
                background_color: (0.2, 0.6, 1, 1)
                border: (20, 20, 20, 20)
                on_press: app.listen_spanish(self)
                
            Button:
                id: copy_english_button
                text: 'Copy to Clipboard'
                background_normal: ''
                background_color: (0.2, 0.6, 1, 1)
                border: (20, 20, 20, 20)
                on_press: app.copy_english(self)
                
            Button:
                id: paste_spanish_button
                text: 'Paste'
                background_normal: ''
                background_color: (0.2, 0.6, 1, 1)
                border: (20, 20, 20, 20)
                on_press: app.paste_spanish(self)''')
        return container
        #return Builder.load_file('test.kv')

    def translate_en_to_es(self, button):
        button.background_color = (1, 0, 0, 1)  # Change button color to red while translating
        threading.Thread(target=self.perform_translation_en_to_es, args=(button,)).start()

    def translate_es_to_en(self, button):
        button.background_color = (1, 0, 0, 1)  # Change button color to red while translating
        threading.Thread(target=self.perform_translation_es_to_en, args=(button,)).start()

    def perform_translation_en_to_es(self, button):
        input_text = self.root.ids.en_input_text.text.strip()
        if input_text:
            try:
                translator = Translator(from_lang='en', to_lang='es')
                translation = translator.translate(input_text)
                Clock.schedule_once(lambda dt: self.update_text(self.root.ids.es_output_text, translation), 0)
            except Exception as e:
                print(f"Error occurred: {e}")
                Clock.schedule_once(lambda dt: self.update_text(self.root.ids.es_output_text, "Translation error, please try again."), 0)
        Clock.schedule_once(lambda dt: self.reset_button_color(button), 0)

    def perform_translation_es_to_en(self, button):
        input_text = self.root.ids.es_input_text.text.strip()
        if input_text:
            try:
                translator = Translator(from_lang='es', to_lang='en')
                translation = translator.translate(input_text)
                Clock.schedule_once(lambda dt: self.update_text(self.root.ids.en_output_text, translation), 0)
            except Exception as e:
                print(f"Error occurred: {e}")
                Clock.schedule_once(lambda dt: self.update_text(self.root.ids.en_output_text, "Translation error, please try again."), 0)
        Clock.schedule_once(lambda dt: self.reset_button_color(button), 0)

    def update_text(self, text_input, text):
        text_input.text = text

    def reset_button_color(self, button):
        button.background_color = (0.2, 0.6, 1, 1)  # Revert button color to original after translating

    def speak_es_translation(self, button):
        translation_text = self.root.ids.es_output_text.text.strip()
        if translation_text:
            try:
                tts = gTTS(translation_text, lang='es')
                temp_path = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
                tts.save(temp_path)
                button.background_color = (1, 0, 0, 1)  # Change button color to red while speaking
                threading.Thread(target=self.play_audio, args=(temp_path, button)).start()
            except Exception as e:
                print(f"Error occurred: {e}")

    def speak_en_translation(self, button):
        translation_text = self.root.ids.en_output_text.text.strip()
        if translation_text:
            try:
                tts = gTTS(translation_text, lang='en')
                temp_path = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
                tts.save(temp_path)
                button.background_color = (1, 0, 0, 1)  # Change button color to red while speaking
                threading.Thread(target=self.play_audio, args=(temp_path, button)).start()
            except Exception as e:
                print(f"Error occurred: {e}")

    def listen_english(self, button):
        button.background_color = (1, 0, 0, 1)  # Change button color to red while listening
        threading.Thread(target=self.perform_listen, args=('en-US', self.root.ids.en_input_text, button)).start()

    def listen_spanish(self, button):
        button.background_color = (1, 0, 0, 1)  # Change button color to red while listening
        threading.Thread(target=self.perform_listen, args=('es-ES', self.root.ids.es_input_text, button)).start()

    def copy_spanish(self, button):
        return
    def copy_english(self, button):
        return

    def perform_listen(self, language, target_textbox, button):
        recognizer = sr.Recognizer()
        mic = sr.Microphone()
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language=language)
            Clock.schedule_once(lambda dt: self.update_text(target_textbox, text), 0)
        except sr.UnknownValueError:
            Clock.schedule_once(lambda dt: self.update_text(target_textbox, "Sorry, I did not understand that."), 0)
        except sr.RequestError as e:
            Clock.schedule_once(lambda dt: self.update_text(target_textbox, f"Could not request results; {e}"), 0)
        Clock.schedule_once(lambda dt: self.reset_button_color(button), 0)

    def play_audio(self, file_path, button):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        button.background_color = (0.2, 0.6, 1, 1)  # Revert button color to original after speaking
        os.remove(file_path)

# Create the Kivy app instance
if __name__ == '__main__':
    TestTranslatorApp().run()
