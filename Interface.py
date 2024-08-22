import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter.font import Font
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
# import easyocr
import io
# import numpy as np
# import re
# import pandas as pd
# import os
# from tkinter import Tk
# import sys


# Fonction pour basculer entre les frames
def show_frame(frame):
    frame.tkraise()


# Crée la fenêtre principale avec le thème Adapta
root = ThemedTk(theme="adapta")  # Appliquer le thème Adapta
root.title("GRDF - ValiDMOS")
root.geometry("1000x560")
root.minsize(1000, 560)  # Définir la taille minimale
icon = tk.PhotoImage(file="images/logo3.png")
root.iconphoto(False, icon)
root.configure(bg="white")

# Crée deux frames
frame1 = tk.Frame(root, bg="white")
frame2 = tk.Frame(root, bg="white")
frame3 = tk.Frame(root, bg="white")
frame4 = tk.Frame(root, bg="white")
frame5 = tk.Frame(root, bg="white")

# Utilisation de grid pour les frames
frame1.grid(row=0, column=0, sticky='nsew')
frame2.grid(row=0, column=0, sticky='nsew')
frame3.grid(row=0, column=0, sticky='nsew')
frame4.grid(row=0, column=0, sticky='nsew')
frame5.grid(row=0, column=0, sticky='nsew')

# Configurer la grille de la fenêtre principale pour redimensionner les frames
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Configurer la grille des frames pour redimensionner les widgets à l'intérieur
frame1.grid_rowconfigure(0, weight=1)
frame1.grid_rowconfigure(1, weight=1)
frame1.grid_rowconfigure(2, weight=1)
frame1.grid_rowconfigure(3, weight=1)
frame1.grid_rowconfigure(4, weight=1)
frame1.grid_rowconfigure(5, weight=1)
frame1.grid_rowconfigure(6, weight=1)
frame1.grid_rowconfigure(7, weight=1)
frame1.grid_rowconfigure(8, weight=1)
frame1.grid_rowconfigure(9, weight=1)
frame1.grid_rowconfigure(10, weight=1)
frame1.grid_rowconfigure(11, weight=1)
frame1.grid_rowconfigure(12, weight=1)
frame1.grid_rowconfigure(13, weight=1)
frame1.grid_rowconfigure(14, weight=1)
frame1.grid_rowconfigure(15, weight=1)
frame1.grid_rowconfigure(16, weight=1)
frame1.grid_rowconfigure(17, weight=1)
frame1.grid_rowconfigure(18, weight=1)
frame1.grid_rowconfigure(19, weight=1)
frame1.grid_columnconfigure(0, weight=1)

custom_font = Font(family="Calibri", size=16, weight="bold")
custom_font2 = Font(family="Calibri", size=10, weight="bold", slant="italic")

# Charger une image avec PIL
image_path = "images/logo.png"
image = Image.open(image_path)
image = image.resize((298, 148))
photo = ImageTk.PhotoImage(image)

# Ajouter l'image à la première frame
image_label = tk.Label(frame1, image=photo, bg="white")
image_label.grid(row=4, column=0, pady=20)

# Ajouter un label et un bouton
label = ttk.Label(frame1, text="Bienvenue dans l'application de prévalidation de DMOS !", font=custom_font,
                  background="white")
label.grid(row=5, column=0, pady=10)

button = ttk.Button(frame1, text="Commencer", command=lambda: show_frame(frame2), style="TButton")
button.grid(row=6, column=0, pady=10, sticky='n')

label2 = ttk.Label(frame1, text="Application en Bêta - LT", font=custom_font2, foreground="grey", background="white")
label2.grid(row=19, column=0, pady=10, sticky='s')


# Configurer la grille des frames pour redimensionner les widgets à l'intérieur
frame2.grid_rowconfigure(0, weight=1)
frame2.grid_rowconfigure(1, weight=1)
frame2.grid_rowconfigure(2, weight=1)
frame2.grid_rowconfigure(3, weight=1)
frame2.grid_rowconfigure(4, weight=1)
frame2.grid_rowconfigure(5, weight=1)
frame2.grid_rowconfigure(6, weight=1)
frame2.grid_rowconfigure(7, weight=1)
frame2.grid_rowconfigure(8, weight=1)
frame2.grid_rowconfigure(9, weight=1)
frame2.grid_rowconfigure(10, weight=1)
frame2.grid_rowconfigure(11, weight=1)
frame2.grid_rowconfigure(12, weight=1)
frame2.grid_rowconfigure(13, weight=1)
frame2.grid_rowconfigure(14, weight=1)
frame2.grid_rowconfigure(15, weight=1)
frame2.grid_rowconfigure(16, weight=1)
frame2.grid_rowconfigure(17, weight=1)
frame2.grid_rowconfigure(18, weight=1)
frame2.grid_rowconfigure(19, weight=1)
frame2.grid_columnconfigure(0, weight=1)
frame2.grid_columnconfigure(1, weight=1)
frame2.grid_columnconfigure(2, weight=1)
frame2.grid_columnconfigure(3, weight=1)
frame2.grid_columnconfigure(4, weight=1)
frame2.grid_columnconfigure(5, weight=1)
frame2.grid_columnconfigure(6, weight=1)
frame2.grid_columnconfigure(7, weight=1)
frame2.grid_columnconfigure(8, weight=1)
frame2.grid_columnconfigure(9, weight=1)
frame2.grid_columnconfigure(10, weight=1)
frame2.grid_columnconfigure(11, weight=1)
frame2.grid_columnconfigure(12, weight=1)
frame2.grid_columnconfigure(13, weight=1)
frame2.grid_columnconfigure(14, weight=1)
frame2.grid_columnconfigure(15, weight=1)
frame2.grid_columnconfigure(16, weight=1)

# Charger une image avec PIL
image_path2 = "images/logopdf.png"
image2 = Image.open(image_path2)
image2 = image2.resize((128, 128))
photo2 = ImageTk.PhotoImage(image2)

# Ajouter l'image à la première frame
image_label2 = tk.Label(frame2, image=photo2, bg="white")
image_label2.grid(row=2, column=8, pady=20)

# Ajouter un label et un bouton
label3 = ttk.Label(frame2, text="Sélectionner le fichier pdf", font=custom_font, background="white")
label3.grid(row=3, column=8, pady=10, sticky='n')


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
        display_pdf_in_canvas(pdf_canvas)
        show_frame(frame4)
        # utiliser_fichier()


# Crée un label pour afficher le chemin du fichier sélectionné
label_fichier = ttk.Label(frame2, text="Aucun fichier sélectionné")
label_fichier.grid(row=4, column=8, pady=10)

# Crée un bouton pour ouvrir la boîte de dialogue de sélection de fichier
bouton_ouvrir = ttk.Button(frame2, text="Ouvrir un fichier", command=ouvrir_fichier)
bouton_ouvrir.grid(row=5, column=8, pady=10)

label5 = ttk.Label(frame2, text="L'application ne prend en charge que les DMOS d'une seule page.", font=custom_font2,
                   foreground="grey", background="white")
label5.grid(row=6, column=8, pady=10)

# Crée un bouton pour valider la sélection
button3 = ttk.Button(frame2, text="Valider", command=valider, style="TButton")
button3.grid(row=19, column=16, pady=10, sticky='s')

button2 = ttk.Button(frame2, text="Retour", command=lambda: show_frame(frame1), style="TButton")
button2.grid(row=19, column=0, pady=10, sticky='s')

label4 = ttk.Label(frame2, text="Application en Bêta - LT", font=custom_font2, foreground="grey", background="white")
label4.grid(row=19, column=8, pady=10, sticky='s')


# Configurer la grille des frames pour redimensionner les widgets à l'intérieur
frame3.grid_rowconfigure(0, weight=1)
frame3.grid_rowconfigure(1, weight=1)
frame3.grid_rowconfigure(2, weight=1)
frame3.grid_rowconfigure(3, weight=1)
frame3.grid_rowconfigure(4, weight=1)
frame3.grid_rowconfigure(5, weight=1)
frame3.grid_rowconfigure(6, weight=1)
frame3.grid_rowconfigure(7, weight=1)
frame3.grid_rowconfigure(8, weight=1)
frame3.grid_rowconfigure(9, weight=1)
frame3.grid_rowconfigure(10, weight=1)
frame3.grid_rowconfigure(11, weight=1)
frame3.grid_rowconfigure(12, weight=1)
frame3.grid_rowconfigure(13, weight=1)
frame3.grid_rowconfigure(14, weight=1)
frame3.grid_rowconfigure(15, weight=1)
frame3.grid_rowconfigure(16, weight=1)
frame3.grid_rowconfigure(17, weight=1)
frame3.grid_rowconfigure(18, weight=1)
frame3.grid_rowconfigure(19, weight=1)
frame3.grid_columnconfigure(0, weight=1)


# Fonction pour animer le GIF
def update_frame(ind):
    frame = frames[ind]
    ind += 1
    if ind == frame_count:
        ind = 0
    label5.configure(image=frame)
    root.after(100, update_frame, ind)


# Charger le GIF
gif_path = "images/chargement3.gif"  # Remplacez par le chemin de votre GIF
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
label5.grid(row=8, column=0, pady=10)

# Démarrer l'animation
frame3.after(0, update_frame, 0)

label6 = ttk.Label(frame3, text="Application en Bêta - LT", font=custom_font2, foreground="grey", background="white")
label6.grid(row=19, column=0, pady=10, sticky='s')

label8 = ttk.Label(frame3,
                   text="Le scan est en cours. L'application peut se figer pendant une minute. Merci de patienter.",
                   font=custom_font2, foreground="grey", background="white")
label8.grid(row=10, column=0, pady=10)

label7 = ttk.Label(frame3, text="Scan en cours...", font=custom_font, background="white")
label7.grid(row=6, column=0, pady=10)




# Fonction pour afficher toutes les pages du PDF dans un Canvas avec défilement
def display_pdf_in_canvas(canvas):
    try:
        document = fitz.open(chemin_fichier)

        # Créer un cadre dans le Canvas pour contenir les images
        canvas_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

        # Charger et afficher chaque page du PDF
        for page_num in range(len(document)):
            page = document[page_num]
            pix = page.get_pixmap()
            img_bytes = pix.tobytes()
            img = Image.open(io.BytesIO(img_bytes))

            # Redimensionner l'image si nécessaire
            img = img.resize((475, 700))  # Ajustez la taille selon vos besoins
            img_tk = ImageTk.PhotoImage(img)

            # Créer un widget Label pour chaque image de page
            label = tk.Label(canvas_frame, image=img_tk, bg="white")
            label.image = img_tk  # Garder une référence à l'image
            label.pack()

        # Ajuster la région de défilement du Canvas pour inclure toutes les images
        canvas_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Fermer le document PDF
        document.close()

    except Exception as e:
        print(f"Erreur lors de l'extraction et de l'affichage du PDF: {e}")

# Crée deux cadres, un pour le PDF et un pour les tableaux
pdf_frame = tk.Frame(frame4, bg="white")
pdf_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

tables_frame = tk.Frame(frame4, bg="white")
tables_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

# Créer un Canvas dans le cadre PDF
pdf_canvas = tk.Canvas(pdf_frame, bg="white")
pdf_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Ajouter une barre de défilement verticale
scrollbar = tk.Scrollbar(pdf_frame, orient="vertical", command=pdf_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
pdf_canvas.configure(yscrollcommand=scrollbar.set)


treeview = tk.ttk.Treeview(tables_frame, columns=("col1"), show="headings", height=2)
treeview.heading("col1", text="DESCRIPTIF DE MODE OPERATOIRE DE SOUDAGE")
treeview.column("col1", width=100, anchor=tk.W)
tableau1 = [
    ("Imputation/EOTP", " "),
    ("DMOS N°", " "),
    ("QMOS de Référence", " "),
    ("Procédé de Soudage", " "),
    ("Type de joint", " "),
    ("Pression", " "),
    ("Courant", " "),
]
for row in tableau1:
    treeview.insert("", tk.END, values=row)
treeview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

treeview = tk.ttk.Treeview(tables_frame, columns=("col1", "col2"), show="headings", height=2)
treeview.heading("col1", text="Elément 1")
treeview.heading("col2", text="Elément 2")
treeview.column("col1", width=100, anchor=tk.W)
treeview.column("col2", width=100, anchor=tk.W)
tableau2 = [
    ("Nuance 1", "Nuance 2"),
    ("D. extérieur 1", "D. extérieur 2"),
    ("Epaisseur 1", "Epaisseur 2"),
    ("Norme 1", "Norme 2"),
]
for row in tableau2:
    treeview.insert("", tk.END, values=row)
treeview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

treeview = tk.ttk.Treeview(tables_frame, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8",
                                                  "col9", "col10"), show="headings", height=2)
treeview.heading("col1", text="Passe N°")
treeview.heading("col2", text="Diamètre")
treeview.heading("col3", text="Réf.")
treeview.heading("col4", text="Polarité")
treeview.heading("col5", text="Designation")
treeview.heading("col6", text="Position")
treeview.heading("col7", text="Vitesse")
treeview.heading("col8", text="Tension")
treeview.heading("col9", text="Intensité")
treeview.heading("col10", text="Energie")
treeview.column("col1", width=20, anchor=tk.W)
treeview.column("col2", width=20, anchor=tk.W)
treeview.column("col3", width=100, anchor=tk.W)
treeview.column("col4", width=20, anchor=tk.W)
treeview.column("col5", width=100, anchor=tk.W)
treeview.column("col6", width=20, anchor=tk.W)
treeview.column("col7", width=20, anchor=tk.W)
treeview.column("col8", width=20, anchor=tk.W)
treeview.column("col9", width=20, anchor=tk.W)
treeview.column("col10", width=20, anchor=tk.W)
tableau3 = [
    ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"),
]
for row in tableau3:
    treeview.insert("", tk.END, values=row)
treeview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

treeview = tk.ttk.Treeview(tables_frame, columns=("col1"), show="headings", height=2)
treeview.heading("col1", text="Mode de préparation, Conditions thermiques et Moyen d'accostage")
treeview.column("col1", width=100, anchor=tk.W)
tableau2 = [
    ("Meulage", " "),
    ("Etuvage des électrodes", " "),
    ("Chanfrein d'origine", " "),
    ("Oxycoupage", " "),
    ("Séchage/dégourdissage", " "),
    ("Température de préchauffage", " "),
    ("Température entre passes", " "),
    ("Type", " "),
    ("Longueur", " "),
]
for row in tableau2:
    treeview.insert("", tk.END, values=row)
treeview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)




# Afficher la première frame au lancement
show_frame(frame1)

# Démarrer la boucle principale
root.mainloop()
