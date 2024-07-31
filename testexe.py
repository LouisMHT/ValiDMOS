import fitz  # PyMuPDF
from paddleocr import PaddleOCR
from PIL import Image
import io
import numpy as np

# Initialiser PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='fr')  # Langue française

# Ouvrir le PDF
pdf_path = "DMOS TEST.pdf"
document = fitz.open(pdf_path)

# Variable pour regrouper toutes les informations extraites
all_texts = []

# Sélectionner la page (ici la première page, index 0)
page = document[0]

# Extraire l'image de la page
image_list = page.get_images(full=True)
for img_index, img in enumerate(image_list, start=1):
    xref = img[0]
    base_image = document.extract_image(xref)
    image_bytes = base_image["image"]

    # Convertir l'image en format PIL
    pil_image = Image.open(io.BytesIO(image_bytes))

    # Convertir l'image PIL en tableau NumPy
    image_np = np.array(pil_image)

    # Utiliser PaddleOCR pour effectuer l'OCR
    result = ocr.ocr(image_np, cls=True)

    # Afficher le résultat pour déboguer
    print("OCR Result:", result)

    # Assurez-vous que le résultat n'est pas None et contient des données
    if result and isinstance(result, list) and len(result) > 0 and isinstance(result[0], list):
        # Extraire le texte des résultats
        extracted_text = " ".join([line[1][0] for line in result[0] if line[1] and isinstance(line[1], list) and len(line[1]) > 0])
    else:
        extracted_text = ""

    # Regrouper le texte extrait dans une seule variable
    all_texts.append(extracted_text)

# Fermer le document PDF
document.close()

# Afficher toutes les informations extraites
all_extracted_text = " ".join(all_texts)
print("Texte extrait de toutes les images:\n", all_extracted_text)
