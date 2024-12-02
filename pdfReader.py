import fitz  # PyMuPDF
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from plyer import filechooser
from kivy.clock import Clock
import threading
import time


class PDFViewerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.file_chooser_button = Button(text="Choose PDF File", size_hint=(1, 0.1))
        self.file_chooser_button.bind(on_release=self.open_file_chooser)
        self.layout.add_widget(self.file_chooser_button)

        self.pdf_document = None
        self.current_page = 0
        self.page_paragraphs = {}
        self.current_paragraph = 0
        self.tts_thread = None
        self.tts_pause_event = threading.Event()
        self.tts_pause_event.set()  # Start with TTS paused

        # Combine all navigation buttons in a single row
        self.button_layout = BoxLayout(size_hint=(1, 0.1))

        # Page navigation buttons
        prev_page_button = Button(text="Previous Page", size_hint=(0.14, 1), on_release=self.show_previous_page)
        next_page_button = Button(text="Next Page", size_hint=(0.14, 1), on_release=self.show_next_page)

        # Paragraph navigation buttons
        prev_paragraph_button = Button(text="Previous Paragraph", size_hint=(0.14, 1),
                                       on_release=self.show_previous_paragraph)
        next_paragraph_button = Button(text="Next Paragraph", size_hint=(0.14, 1), on_release=self.show_next_paragraph)

        # Pause/Resume TTS button
        self.pause_resume_button = Button(text="Resume", size_hint=(0.14, 1), on_release=self.pause_resume_tts)

        self.button_layout.add_widget(prev_page_button)
        self.button_layout.add_widget(next_page_button)
        self.button_layout.add_widget(prev_paragraph_button)
        self.button_layout.add_widget(next_paragraph_button)
        self.button_layout.add_widget(self.pause_resume_button)

        return self.layout

    def open_file_chooser(self, instance):
        filechooser.open_file(on_selection=self.load_pdf, filters=['*.pdf'])

    def load_pdf(self, selection):
        if selection:
            pdf_path = selection[0]
            self.pdf_document = fitz.open(pdf_path)
            self.layout.remove_widget(self.file_chooser_button)  # Remove the file chooser button after selection
            self.layout.add_widget(self.button_layout)  # Add navigation buttons
            self.current_page = 0
            self.extract_paragraphs()
            self.display_pdf_page(self.current_page)
            self.start_tts()  # Start the TTS functionality after loading the PDF

    def extract_paragraphs(self):
        self.page_paragraphs = {}
        for page_num in range(self.pdf_document.page_count):
            page = self.pdf_document.load_page(page_num)
            blocks = page.get_text("blocks")
            paragraphs = []
            for b in blocks:
                text = b[4].strip()
                if text:  # Only add non-empty text
                    paragraphs.append((b, text))
            self.page_paragraphs[page_num] = paragraphs

    def display_pdf_page(self, page_num):
        if not self.pdf_document:
            return

        if hasattr(self, 'scrollview'):
            self.layout.remove_widget(self.scrollview)

        page = self.pdf_document.load_page(page_num)
        pix = page.get_pixmap()

        # Create a Kivy Texture from the pixmap
        texture = Texture.create(size=(pix.width, pix.height))
        texture.blit_buffer(pix.samples, colorfmt='rgb', bufferfmt='ubyte')
        texture.flip_vertical()  # Flip the texture vertically

        image = Image(texture=texture, allow_stretch=True, keep_ratio=True, size_hint=(1, 1))

        # Highlight the current paragraph
        if self.current_page in self.page_paragraphs and self.page_paragraphs[self.current_page]:
            current_block = self.page_paragraphs[self.current_page][self.current_paragraph][0]
            rect = fitz.Rect(current_block[:4])
            highlight = page.add_highlight_annot(rect)

        self.scrollview = ScrollView(size_hint=(1, 0.9))  # Use most of the available space
        self.scrollview.add_widget(image)
        self.layout.add_widget(self.scrollview, index=1)

    def show_previous_page(self, instance):
        if self.current_page > 0:
            self.current_page -= 1
            self.current_paragraph = 0  # Reset to the first paragraph of the new page
            self.display_pdf_page(self.current_page)

    def show_next_page(self, instance):
        if self.current_page < self.pdf_document.page_count - 1:
            self.current_page += 1
            self.current_paragraph = 0  # Reset to the first paragraph of the new page
            self.display_pdf_page(self.current_page)

    def show_previous_paragraph(self, instance):
        if self.current_page in self.page_paragraphs:
            if self.current_paragraph > 0:
                self.current_paragraph -= 1
            elif self.current_page > 0:
                self.current_page -= 1
                if self.current_page in self.page_paragraphs:
                    self.current_paragraph = len(self.page_paragraphs[self.current_page]) - 1
                else:
                    self.current_paragraph = 0
                self.display_pdf_page(self.current_page)
            self.display_pdf_page(self.current_page)

    def show_next_paragraph(self, instance):
        if self.current_page in self.page_paragraphs:
            if self.current_paragraph < len(self.page_paragraphs[self.current_page]) - 1:
                self.current_paragraph += 1
            elif self.current_page < self.pdf_document.page_count - 1:
                self.current_page += 1
                self.current_paragraph = 0
                self.display_pdf_page(self.current_page)
            self.display_pdf_page(self.current_page)

    def pause_resume_tts(self, instance):
        if self.tts_thread and self.tts_thread.is_alive():
            if self.tts_pause_event.is_set():
                self.tts_pause_event.clear()
                Clock.schedule_once(lambda dt: self.update_button_text("Pause"), 0)
            else:
                self.tts_pause_event.set()
                Clock.schedule_once(lambda dt: self.update_button_text("Resume"), 0)

    def update_button_text(self, text):
        self.pause_resume_button.text = text

    def text_to_speech(self):
        while True:
            if not self.tts_pause_event.is_set():
                # Placeholder for TTS functionality
                print("Performing text-to-speech...")
            time.sleep(1)
        print("TTS paused")

    def start_tts(self):
        if not self.tts_thread or not self.tts_thread.is_alive():
            self.tts_thread = threading.Thread(target=self.text_to_speech)
            self.tts_thread.start()


if __name__ == "__main__":
    PDFViewerApp().run()
