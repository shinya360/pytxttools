import fitz  # PyMuPDF
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from plyer import filechooser


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

        return self.layout

    def open_file_chooser(self, instance):
        filechooser.open_file(on_selection=self.load_pdf, filters=['*.pdf'])

    def load_pdf(self, selection):
        if selection:
            pdf_path = selection[0]
            self.pdf_document = fitz.open(pdf_path)
            self.current_page = 0
            self.extract_paragraphs()
            self.display_pdf_page(self.current_page)

    def extract_paragraphs(self):
        self.page_paragraphs = {}
        for page_num in range(self.pdf_document.page_count):
            page = self.pdf_document.load_page(page_num)
            text = page.get_text("text").strip()
            if text:  # Only add non-empty text
                self.page_paragraphs[page_num] = text.split("\n\n")
        for page_num in self.page_paragraphs:
            self.page_paragraphs[page_num] = [para for para in self.page_paragraphs[page_num] if
                                              para.strip()]  # Remove empty paragraphs

    def display_pdf_page(self, page_num):
        if not self.pdf_document:
            return

        self.layout.clear_widgets()

        page = self.pdf_document.load_page(page_num)
        pix = page.get_pixmap()

        # Create a Kivy Texture from the pixmap
        texture = Texture.create(size=(pix.width, pix.height))
        texture.blit_buffer(pix.samples, colorfmt='rgb', bufferfmt='ubyte')
        texture.flip_vertical()  # Flip the texture vertically

        image = Image(texture=texture, allow_stretch=True, keep_ratio=True, size_hint=(1, 1))

        scrollview = ScrollView(size_hint=(1, 0.9))  # Use most of the available space
        scrollview.add_widget(image)
        self.layout.add_widget(scrollview)

        # Combine all navigation buttons in a single row
        button_layout = BoxLayout(size_hint=(1, 0.1))

        # Page navigation buttons
        prev_page_button = Button(text="Previous Page", size_hint=(0.25, 1), on_release=self.show_previous_page)
        next_page_button = Button(text="Next Page", size_hint=(0.25, 1), on_release=self.show_next_page)

        # Paragraph navigation buttons
        prev_paragraph_button = Button(text="Previous Paragraph", size_hint=(0.25, 1),
                                       on_release=self.show_previous_paragraph)
        next_paragraph_button = Button(text="Next Paragraph", size_hint=(0.25, 1), on_release=self.show_next_paragraph)

        button_layout.add_widget(prev_page_button)
        button_layout.add_widget(next_page_button)
        button_layout.add_widget(prev_paragraph_button)
        button_layout.add_widget(next_paragraph_button)
        self.layout.add_widget(button_layout)

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


if __name__ == "__main__":
    PDFViewerApp().run()
