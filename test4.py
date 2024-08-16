import calamari_ocr
from calamari_ocr.ocr import CalamariOCR
from PIL import Image
import io
import fitz  # PyMuPDF
import numpy as np
from pdf2image import convert_from_path

def preprocess_image(image_np):
    # Convertir en niveaux de gris
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    # Binariser l'image
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary

def scan_with_calamari(pdf_path):
    # Charger le modèle Calamari
    model = CalamariOCR.load_model('path/to/your/calamari_model')

    # Convertir le PDF en images
    images = convert_from_path(pdf_path)

    all_texts = []

    for i, image in enumerate(images):
        # Convertir l'image PIL en tableau numpy
        image_np = np.array(image)

        # Prétraiter l'image
        preprocessed_image_np = preprocess_image(image_np)

        # Convertir numpy array en image PIL pour Calamari
        image_pil = Image.fromarray(preprocessed_image_np)

        # OCR avec Calamari
        result = model.predict(image_pil)
        extracted_text = " ".join(result)
        all_texts.append(extracted_text)

    # Combiner les résultats
    all_extracted_text = " ".join(all_texts)
    print("Texte extrait avec Calamari OCR:\n", all_extracted_text)

# Exemple d'utilisation
scan_with_calamari("DMOS TEST.pdf")
