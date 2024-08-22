import tkinter as tk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import fitz
import io

# Fonction pour basculer entre les frames
def show_frame(frame):
    frame.tkraise()


# Crée la fenêtre principale avec le thème Adapta
root = ThemedTk(theme="adapta")  # Appliquer le thème Adapta
root.title("GRDF - ValiDMOS")
root.geometry("854x480")
root.resizable(False, False)
icon = tk.PhotoImage(file="images/logo3.png")
root.iconphoto(False, icon)
root.configure(bg="white")

# Crée deux frames
frame1 = tk.Frame(root, bg="white")

# Utilisation de place pour les frames
frame1.place(x=0, y=0, relwidth=1, relheight=1)

def display_pdf_in_frame(chemin_fichier):
    try:
        pdf_path = chemin_fichier
        # Ouvrir le PDF
        document = fitz.open(pdf_path)

        # Sélectionner la page spécifiée
        page = document[0]

        # Extraire l'image de la page
        pix = page.get_pixmap()
        img_bytes = pix.tobytes()
        img = Image.open(io.BytesIO(img_bytes))

        # Fermer le document PDF
        document.close()
        img = img.resize((300, 427))
        # Convertir l'image PIL en ImageTk
        img_tk = ImageTk.PhotoImage(img)

        # Ajouter l'image à un widget Label dans le frame
        label = tk.Label(frame1, image=img_tk)
        label.image = img_tk  # Garder une référence à l'image pour éviter le garbage collection
        label.place(x=25, y=25)

    except Exception as e:
        print(f"Erreur lors de l'extraction et de l'affichage de l'image: {e}")

show_frame(frame1)

display_pdf_in_frame("DMOS3.pdf")

# Démarrer la boucle principale
root.mainloop()
