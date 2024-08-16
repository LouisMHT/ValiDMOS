from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
import easyocr
import io
import numpy as np


def scan(chemin_fichier):
    global all_extracted_text
    try:

        # Initialiser le lecteur easyocr pour la langue française
        reader = easyocr.Reader(['fr'], model_storage_directory='model', download_enabled=False)
        #reader = easyocr.Reader(['fr'])

        # Ouvrir le PDF
        pdf_path = chemin_fichier
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
            image = Image.open(io.BytesIO(image_bytes))

            # Convertir l'image PIL en tableau de pixels
            image_np = np.array(image)

            # Utiliser easyocr pour effectuer l'OCR
            result = reader.readtext(image_np, detail=0)  # detail=0 pour obtenir seulement le texte

            # Regrouper le texte extrait dans une seule variable
            extracted_text = " ".join(result)
            all_texts.append(extracted_text)

        # Fermer le document PDF
        document.close()

        # Afficher toutes les informations extraites
        all_extracted_text = " ".join(all_texts)

        print("Texte extrait de toutes les images:\n", all_extracted_text)
        # utiliser_text()
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")
        pass

scan("DMOS TEST.pdf")