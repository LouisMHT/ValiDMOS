import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter.font import Font
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
import easyocr
import io
import numpy as np

# Fonction pour basculer entre les frames
def show_frame(frame):
    frame.tkraise()

# Crée la fenêtre principale avec le thème Adapta
root = ThemedTk(theme="adapta")  # Appliquer le thème Adapta
root.title("GRDF - DMOSControl")
root.geometry("854x480")
root.resizable(False, False)
icon = tk.PhotoImage(file="logo3.png")
root.iconphoto(False, icon)
root.configure(bg="white")

# Crée deux frames
frame1 = tk.Frame(root, bg="white")
frame2 = tk.Frame(root, bg="white")
frame3 = tk.Frame(root, bg="white")
frame4 = tk.Frame(root, bg="white")
frame5 = tk.Frame(root, bg="white")

# Utilisation de place pour les frames
frame1.place(x=0, y=0, relwidth=1, relheight=1)
frame2.place(x=0, y=0, relwidth=1, relheight=1)
frame3.place(x=0, y=0, relwidth=1, relheight=1)
frame4.place(x=0, y=0, relwidth=1, relheight=1)
frame5.place(x=0, y=0, relwidth=1, relheight=1)

custom_font = Font(family="Calibri", size=16, weight="bold")
custom_font2 = Font(family="Calibri", size=10, weight="bold", slant="italic")




# Charger une image avec PIL
image_path = "logo.png"
image = Image.open(image_path)
image = image.resize((298, 148))
photo = ImageTk.PhotoImage(image)

# Ajouter l'image à la première frame
image_label = tk.Label(frame1, image=photo, bg="white")
image_label.place(x=278, y=75)

# Ajouter un label et un bouton
label = ttk.Label(frame1, text="Bienvenue dans l'application de prévalidation de DMOS !", font=custom_font, background="white")
label.place(relx=0.5, anchor='center', y=250)

button = ttk.Button(frame1, text="Commencer", command=lambda: show_frame(frame2), style="TButton")
button.place(relx=0.5, anchor='center', y=315)

label2 = ttk.Label(frame1, text="Application en Bêta - LT", font=custom_font2, foreground="grey", background="white")
label2.place(relx=0.5, anchor='center', y=460)





# Charger une image avec PIL
image_path2 = "logopdf.png"
image2 = Image.open(image_path2)
image2 = image2.resize((128, 128))
photo2 = ImageTk.PhotoImage(image2)

# Ajouter l'image à la première frame
image_label2 = tk.Label(frame2, image=photo2, bg="white")
image_label2.place(x=363, y=50)

# Ajouter un label et un bouton
label3 = ttk.Label(frame2, text="Sélectionner le fichier pdf", font=custom_font, background="white")
label3.place(relx=0.5, anchor='center', y=220)


def ouvrir_fichier():
    global chemin_fichier
    # Ouvre la boîte de dialogue pour sélectionner un fichier
    chemin_fichier = filedialog.askopenfilename(
        title="Sélectionner un fichier",
        filetypes=[("Tous les fichiers", "*.*"), ("Fichiers texte", "*.txt")]
    )
    # Affiche le chemin du fichier sélectionné
    label_fichier.config(text=chemin_fichier if chemin_fichier else "Aucun fichier sélectionné")

chemin_fichier = None

def valider():
    # Vérifie si un fichier a été sélectionné
    if not chemin_fichier:
        # Affiche un message d'erreur si aucun fichier n'a été sélectionné
        messagebox.showerror("Erreur", "Veuillez sélectionner un fichier avant de valider.")
    else:
        show_frame(frame3)
        utiliser_fichier()


def utiliser_fichier():
    global chemin_fichier
    if frame3.winfo_ismapped():
        print("Frame 3 affichée")
        root.after(3000, lambda: scan(chemin_fichier))

def scan(chemin_fichier):
    try:
        # Initialiser le lecteur easyocr pour la langue française
        reader = easyocr.Reader(['fr'])

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
    except Exception as e:
        pass




# Crée un bouton pour ouvrir la boîte de dialogue de sélection de fichier
bouton_ouvrir = ttk.Button(frame2, text="Ouvrir un fichier", command=ouvrir_fichier)
bouton_ouvrir.place(relx=0.5, anchor='center', y=315)

# Crée un label pour afficher le chemin du fichier sélectionné
label_fichier = ttk.Label(frame2, text="Aucun fichier sélectionné")
label_fichier.place(relx=0.5, anchor='center', y=260)

# Crée un bouton pour valider la sélection
button3 = ttk.Button(frame2, text="Valider", command=valider, style="TButton")
button3.place(x=745, y=420)

button2 = ttk.Button(frame2, text="Retour", command=lambda: show_frame(frame1), style="TButton")
button2.place(x=25, y=420)

label5 = ttk.Label(frame2, text="L'application ne prend en charge que les DMOS d'une seule page.", font=custom_font2, foreground="grey", background="white")
label5.place(relx=0.5, anchor='center', y=360)


label4 = ttk.Label(frame2, text="Application en Bêta - LT", font=custom_font2, foreground="grey", background="white")
label4.place(relx=0.5, anchor='center', y=460)



# Fonction pour animer le GIF
def update_frame(ind):
    frame = frames[ind]
    ind += 1
    if ind == frame_count:
        ind = 0
    label5.configure(image=frame)
    root.after(100, update_frame, ind)

# Charger le GIF
gif_path = "chargement3.gif"  # Remplacez par le chemin de votre GIF
im = Image.open(gif_path)

# Charger toutes les frames du GIF
frames = []
try:
    while True:
        frames.append(ImageTk.PhotoImage(im.copy()))
        im.seek(len(frames))  # Aller à la frame suivante
except EOFError:
    pass

frame_count = len(frames)

# Créer un widget Label pour afficher le GIF
label5 = tk.Label(frame3)
label5.place(relx=0.5, anchor='center', y=220)

# Démarrer l'animation
frame3.after(0, update_frame, 0)


button4 = ttk.Button(frame3, text="Retour", command=lambda: show_frame(frame2), style="TButton")
button4.place(x=25, y=420)

label6 = ttk.Label(frame3, text="Application en Bêta - LT", font=custom_font2, foreground="grey", background="white")
label6.place(relx=0.5, anchor='center', y=460)

label8 = ttk.Label(frame3, text="Le scan est en cours. L'application peut se figer pendant une minute. Merci de patienter.", font=custom_font2, foreground="grey", background="white")
label8.place(relx=0.5, anchor='center', y=350)

label7 = ttk.Label(frame3, text="Scan en cours...", font=custom_font, background="white")
label7.place(relx=0.5, anchor='center', y=170)


show_frame(frame1)

# Démarrer la boucle principale
root.mainloop()
