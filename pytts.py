import fitz  # PyMuPDF
from gtts import gTTS

def pdf_to_speech(pdf_path, output_audio_path):
    # Open the PDF file
    document = fitz.open(pdf_path)
    text = ""

    # Extract text from each page
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()

    # Convert text to speech
    tts = gTTS(text)
    tts.save(output_audio_path)
    print(f"Audio saved to {output_audio_path}")

# Example usage
pdf_to_speech('../TheDancingWuLiMasters.pdf', 'output.mp3')
