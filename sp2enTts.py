from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from translate import Translator
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import tempfile
import os

class TranslatorApp(App):
    def build(self):
        # Create the main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Section for English to Spanish translation
        en_to_es_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        en_to_es_label = Label(text='English to Spanish', size_hint=(1, None), height=30)
        en_to_es_layout.add_widget(en_to_es_label)

        self.en_input_text = TextInput(hint_text='Enter English text here', multiline=True, size_hint_y=None, height=100)
        en_to_es_layout.add_widget(self.en_input_text)

        self.es_output_text = TextInput(hint_text='Spanish translation will appear here', multiline=True, size_hint_y=None, height=100)
        en_to_es_layout.add_widget(self.es_output_text)

        en_to_es_button = Button(text='Translate to Spanish', size_hint=(1, None), height=40)
        en_to_es_button.bind(on_press=self.translate_en_to_es)
        en_to_es_layout.add_widget(en_to_es_button)

        en_to_es_tts_button = Button(text='Speak Translation', size_hint=(1, None), height=40)
        en_to_es_tts_button.bind(on_press=self.speak_es_translation)
        en_to_es_layout.add_widget(en_to_es_tts_button)

        # Section for Spanish to English translation
        es_to_en_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        es_to_en_label = Label(text='Spanish to English', size_hint=(1, None), height=30)
        es_to_en_layout.add_widget(es_to_en_label)

        self.es_input_text = TextInput(hint_text='Enter Spanish text here', multiline=True, size_hint_y=None, height=100)
        es_to_en_layout.add_widget(self.es_input_text)

        self.en_output_text = TextInput(hint_text='English translation will appear here', multiline=True, size_hint_y=None, height=100)
        es_to_en_layout.add_widget(self.en_output_text)

        es_to_en_button = Button(text='Translate to English', size_hint=(1, None), height=40)
        es_to_en_button.bind(on_press=self.translate_es_to_en)
        es_to_en_layout.add_widget(es_to_en_button)

        es_to_en_tts_button = Button(text='Speak Translation', size_hint=(1, None), height=40)
        es_to_en_tts_button.bind(on_press=self.speak_en_translation)
        es_to_en_layout.add_widget(es_to_en_tts_button)

        # Add both sections to the main layout
        main_layout.add_widget(en_to_es_layout)
        main_layout.add_widget(es_to_en_layout)

        return main_layout

    def translate_en_to_es(self, instance):
        input_text = self.en_input_text.text.strip()
        if input_text:
            try:
                translator = Translator(from_lang='en', to_lang='es')
                translation = translator.translate(input_text)
                self.es_output_text.text = translation
            except Exception as e:
                print(f"Error occurred: {e}")
                self.es_output_text.text = "Translation error, please try again."

    def translate_es_to_en(self, instance):
        input_text = self.es_input_text.text.strip()
        if input_text:
            try:
                translator = Translator(from_lang='es', to_lang='en')
                translation = translator.translate(input_text)
                self.en_output_text.text = translation
            except Exception as e:
                print(f"Error occurred: {e}")
                self.en_output_text.text = "Translation error, please try again."

    def speak_es_translation(self, instance):
        translation_text = self.es_output_text.text.strip()
        if translation_text:
            try:
                tts = gTTS(translation_text, lang='es')
                temp_path = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
                tts.save(temp_path)
                audio = AudioSegment.from_mp3(temp_path)
                play(audio)
                os.remove(temp_path)
            except Exception as e:
                print(f"Error occurred: {e}")

    def speak_en_translation(self, instance):
        translation_text = self.en_output_text.text.strip()
        if translation_text:
            try:
                tts = gTTS(translation_text, lang='en')
                temp_path = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
                tts.save(temp_path)
                audio = AudioSegment.from_mp3(temp_path)
                play(audio)
                os.remove(temp_path)
            except Exception as e:
                print(f"Error occurred: {e}")

# Create the Kivy app instance
if __name__ == '__main__':
    TranslatorApp().run()
