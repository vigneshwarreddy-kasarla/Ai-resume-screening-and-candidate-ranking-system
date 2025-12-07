import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from PyPDF2 import PdfReader

from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import os

# Download NLTK Data
nltk.download("punkt")
nltk.download("stopwords")

STOPWORDS = set(stopwords.words("english"))

# ---- IMPORTANT: SET TESSERACT PATH ----
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# Extract text using PyPDF2 → If fails → use OCR
def extract_text_from_pdf(path):
    text = ""

    # First try PyPDF2
    try:
        reader = PdfReader(path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    except:
        pass

    # If text empty -> fallback to OCR
    if text.strip() == "":
        print(f"⚠ OCR Enabled For: {path}")
        images = convert_from_path(path)

        for i, img in enumerate(images):
            temp_path = f"page_{i}.png"
            img.save(temp_path, "PNG")
            text += pytesseract.image_to_string(Image.open(temp_path)) + " "
            os.remove(temp_path)

    return text


def clean_text(text):
    text = text.lower()
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"\+?\d[\d -]{8,15}", " ", text)
    text = re.sub(r"[^a-z ]+", " ", text)
    return text


def tokenize(text):
    tokens = word_tokenize(text)
    return [t for t in tokens if t.isalpha() and t not in STOPWORDS]


def parse_resume(path):
    raw = extract_text_from_pdf(path)
    cleaned = clean_text(raw)
    tokens = tokenize(cleaned)
    return cleaned, tokens
