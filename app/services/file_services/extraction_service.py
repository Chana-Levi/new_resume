import os
import time
import io
import fitz
import pytesseract
from PIL import Image
from docx import Document as DocxDocument

# Set the path to the Tesseract executable from environment variable
tesseract_cmd = os.getenv('TESSERACT_CMD', r'C:\Program Files\Tesseract-OCR\tesseract.exe')
pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
print("Tesseract cmd path:", pytesseract.pytesseract.tesseract_cmd)


def extract_info(file_path: str):
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.lower()
    if file_extension == '.pdf':
        return read_pdf_with_tesseract(file_path)
    elif file_extension == '.doc' or file_extension == '.docx':
        return read_word(file_path)
    elif file_extension == '.txt':
        return read_text_file(file_path)
    elif file_extension in ['.jpg', '.jpeg', '.png']:
        return read_image_with_tesseract(file_path)
    else:
        raise ValueError("Unsupported file extension: " + file_extension)


def read_text_file(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def read_pdf_with_tesseract(file_path: str) -> str:
    pdf_document = fitz.open(file_path)
    extracted_text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes()))
        text = pytesseract.image_to_string(img, lang='eng+heb')
        extracted_text += text + "\n"
    return extracted_text


def read_word(file_path: str):
    doc = DocxDocument(file_path)
    time.sleep(1)
    all_text = ""
    for paragraph in doc.paragraphs:
        all_text += paragraph.text + "\n"
    return all_text


def read_image_with_tesseract(file_path: str) -> str:
    img = Image.open(file_path)
    text = pytesseract.image_to_string(img, lang='eng+heb')
    return text