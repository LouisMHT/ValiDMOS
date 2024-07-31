import fitz  # PyMuPDF
from PIL import Image, ImageTk
import tkinter as tk
import io

def display_pdf_in_tkinter(pdf_path):
    # Ouvrir le PDF
    document = fitz.open(pdf_path)
    page = document[0]  # Pour afficher la première page

    # Extraire l'image de la page
    pix = page.get_pixmap()
    img_bytes = pix.tobytes()
    img = Image.open(io.BytesIO(img_bytes))

    # Créer la fenêtre Tkinter
    root = tk.Tk()
    root.title("PDF Viewer")

    # Convertir l'image PIL en ImageTk
    img_tk = ImageTk.PhotoImage(img)

    # Ajouter l'image à un widget Label
    label = tk.Label(root, image=img_tk)
    label.pack()

    # Lancer l'interface graphique
    root.mainloop()

# Exemple d'utilisation
pdf_path = "DMOS TEST.pdf"
display_pdf_in_tkinter(pdf_path)
