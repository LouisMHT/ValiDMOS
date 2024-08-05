import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter.font import Font
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import fitz  # PyMuPDF
import io

Imputation = ''
QMOS = ''
ProcedeSoudage = ''
Diametre = ''
TypeJoint = ''
Pression = ''
Epaisseur = ''
Norme = ''
Courant = ''
Passes = ''
Meulage = ''
Etuvage = ''
Chanfrein = ''
Oxycoupage = ''
Sechage = ''
Prechauffage = ''
TemperatureEntrePasses = ''
Type = ''
Longueur = ''


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
custom_font3 = Font(family="Calibri", size=10, weight="bold")

# Charger une image avec PIL
image_path = "logo.png"
image = Image.open(image_path)
image = image.resize((298, 148))
photo = ImageTk.PhotoImage(image)

# Ajouter l'image à la première frame
image_label = tk.Label(frame1, image=photo, bg="white")
image_label.place(x=278, y=75)

# Ajouter un label et un bouton
label = ttk.Label(frame1, text="Bienvenue dans l'application de prévalidation de DMOS !", font=custom_font,
                  background="white")
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


all_extracted_text = ""


def scan(chemin_fichier):
    global all_extracted_text
    try:
        # Open the PDF file
        pdf_document = fitz.open(chemin_fichier)
        text_list = []

        # Iterate through each page
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)  # Load each page
            blocks = page.get_text("dict")["blocks"]  # Get text as dictionary

            for block in blocks:
                if "lines" in block:  # Check if the block contains lines of text
                    for line in block["lines"]:
                        line_text = "".join([span["text"] for span in line["spans"]])  # The actual text
                        text_list.append(line_text)

        print(text_list)
        all_extracted_text = text_list
        utiliser_text()
    except Exception as e:
        pass


def utiliser_text():
    global all_extracted_text
    print("Texte extrait de toutes les images:\n", all_extracted_text)
    data = all_extracted_text
    display_pdf_in_frame()
    root.after(3000, lambda: show_frame(frame4))
    # Initialiser les variables globales
    global Imputation, QMOS, ProcedeSoudage, Diametre, TypeJoint, Pression, Epaisseur, Norme, Courant, Passes
    global Meulage, Etuvage, Chanfrein, Oxycoupage, Sechage, Prechauffage, TemperatureEntrePasses, Type, Longueur

    Imputation = all_extracted_text[109]
    Imputation = Imputation[18:]

    QMOS = all_extracted_text[36]
    QMOS = QMOS[22:]

    ProcedeSoudage = all_extracted_text[126]

    TypeJoint = all_extracted_text[4]

    Pression = all_extracted_text[6]

    Diametre = all_extracted_text[37]

    Epaisseur = all_extracted_text[38]

    Norme = all_extracted_text[124]

    Courant = all_extracted_text[8]
    Courant = Courant[55:]
    Courant = Courant[:2]

    Meulage = all_extracted_text[10]
    Meulage = Meulage[12:]

    Etuvage = all_extracted_text[11]
    Etuvage = Etuvage[27:]

    Chanfrein = all_extracted_text[13]
    Chanfrein = Chanfrein[24:]

    Oxycoupage = all_extracted_text[14]
    Oxycoupage = Oxycoupage[15:]

    Sechage = all_extracted_text[17]
    Sechage = Sechage[28:]

    Prechauffage = all_extracted_text[18]
    Prechauffage = Prechauffage[37:]

    TemperatureEntrePasses = all_extracted_text[19]
    TemperatureEntrePasses = TemperatureEntrePasses[34:]

    Type = all_extracted_text[22]
    Type = Type[9:]

    Longueur = all_extracted_text[25]
    Longueur = Longueur[25:]









    # labels

    label32 = ttk.Label(frame4, text=Imputation, font=custom_font3, background="white")
    label32.place(x=725, y=40)

    label33 = ttk.Label(frame4, text=QMOS, font=custom_font3, background="white")
    label33.place(x=480, y=40)

    label34 = ttk.Label(frame4, text=ProcedeSoudage, font=custom_font3, background="white")
    label34.place(x=560, y=60)

    label35 = ttk.Label(frame4, text=TypeJoint, font=custom_font3, background="white")
    label35.place(x=560, y=80)

    label36 = ttk.Label(frame4, text=Pression, font=custom_font3, background="white")
    label36.place(x=560, y=100)

    label37 = ttk.Label(frame4, text=Diametre, font=custom_font3, background="white")
    label37.place(x=560, y=120)

    label38 = ttk.Label(frame4, text=Epaisseur, font=custom_font3, background="white")
    label38.place(x=560, y=140)

    label39 = ttk.Label(frame4, text=Norme, font=custom_font3, background="white")
    label39.place(x=560, y=160)

    label40 = ttk.Label(frame4, text=Courant, font=custom_font3, background="white")
    label40.place(x=560, y=180)

    label42 = ttk.Label(frame4, text=Meulage, font=custom_font3, background="white")
    label42.place(x=500, y=200)

    label43 = ttk.Label(frame4, text=Etuvage, font=custom_font3, background="white")
    label43.place(x=750, y=200)

    label44 = ttk.Label(frame4, text=Chanfrein, font=custom_font3, background="white")
    label44.place(x=500, y=220)

    label45 = ttk.Label(frame4, text=Oxycoupage, font=custom_font3, background="white")
    label45.place(x=750, y=220)

    label46 = ttk.Label(frame4, text=Sechage, font=custom_font3, background="white")
    label46.place(x=560, y=240)

    label47 = ttk.Label(frame4, text=Prechauffage, font=custom_font3, background="white")
    label47.place(x=560, y=260)

    label48 = ttk.Label(frame4, text=TemperatureEntrePasses, font=custom_font3, background="white")
    label48.place(x=560, y=280)

    label49 = ttk.Label(frame4, text=Type, font=custom_font3, background="white")
    label49.place(x=560, y=300)

    label50 = ttk.Label(frame4, text=Longueur, font=custom_font3, background="white")
    label50.place(x=750, y=320)

    label41 = ttk.Label(frame4, text=Passes, font=custom_font3, background="white")
    label41.place(x=435, y=340)

    # Retourner les valeurs extraites
    return {
        "Imputation": Imputation,
        "QMOS": QMOS,
        "ProcedeSoudage": ProcedeSoudage,
        "Diametre": Diametre,
        "TypeJoint": TypeJoint,
        "Pression": Pression,
        "Epaisseur": Epaisseur,
        "Norme": Norme,
        "Courant": Courant,
        "Passes": Passes,
        "Meulage": Meulage,
        "Etuvage": Etuvage,
        "Chanfrein": Chanfrein,
        "Oxycoupage": Oxycoupage,
        "Sechage": Sechage,
        "Prechauffage": Prechauffage,
        "TemperatureEntrePasses": TemperatureEntrePasses,
        "Type": Type,
        "Longueur": Longueur
    }


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

label5 = ttk.Label(frame2, text="L'application ne prend en charge que les DMOS d'une seule page.", font=custom_font2,
                   foreground="grey", background="white")
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

label6 = ttk.Label(frame3, text="Application en Bêta - LT", font=custom_font2, foreground="grey", background="white")
label6.place(relx=0.5, anchor='center', y=460)

label8 = ttk.Label(frame3,
                   text="Le scan est en cours. L'application peut se figer pendant une minute. Merci de patienter.",
                   font=custom_font2, foreground="grey", background="white")
label8.place(relx=0.5, anchor='center', y=350)

label7 = ttk.Label(frame3, text="Scan en cours...", font=custom_font, background="white")
label7.place(relx=0.5, anchor='center', y=170)


def display_pdf_in_frame():
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
        label = tk.Label(frame4, image=img_tk)
        label.image = img_tk  # Garder une référence à l'image pour éviter le garbage collection
        label.place(x=25, y=25)

    except Exception as e:
        print(f"Erreur lors de l'extraction et de l'affichage de l'image: {e}")


button4 = ttk.Button(frame4, text="Retour", command=lambda: show_frame(frame2), style="TButton")
button4.place(x=350, y=420)

button5 = ttk.Button(frame4, text="Valider", command=lambda: show_frame(frame5), style="TButton")
button5.place(x=745, y=420)

label13 = ttk.Label(frame4, text="DESCRIPTIF DE MODE OPERATOIRE DE SOUDAGE", font=custom_font, background="white")
label13.place(x=380, y=10)

label14 = ttk.Label(frame4, text="QMOS de Référence", font=custom_font3, foreground="grey", background="white")
label14.place(x=360, y=40)

label12 = ttk.Label(frame4, text="Imputation/EOTP", font=custom_font3, foreground="grey", background="white")
label12.place(x=620, y=40)

label15 = ttk.Label(frame4, text="Procédé de Soudage", font=custom_font3, foreground="grey", background="white")
label15.place(x=360, y=60)

label16 = ttk.Label(frame4, text="Type de Joint", font=custom_font3, foreground="grey", background="white")
label16.place(x=360, y=80)

label17 = ttk.Label(frame4, text="Pression maximale de service", font=custom_font3, foreground="grey",
                    background="white")
label17.place(x=360, y=100)

label18 = ttk.Label(frame4, text="Diamètre extérieur", font=custom_font3, foreground="grey", background="white")
label18.place(x=360, y=120)

label19 = ttk.Label(frame4, text="Epaisseur", font=custom_font3, foreground="grey", background="white")
label19.place(x=360, y=140)

label20 = ttk.Label(frame4, text="Norme", font=custom_font3, foreground="grey", background="white")
label20.place(x=360, y=160)

label21 = ttk.Label(frame4, text="Type de courant", font=custom_font3, foreground="grey", background="white")
label21.place(x=360, y=180)

label23 = ttk.Label(frame4, text="Meulage", font=custom_font3, foreground="grey", background="white")
label23.place(x=360, y=200)

label24 = ttk.Label(frame4, text="Etuvage des électrodes", font=custom_font3, foreground="grey", background="white")
label24.place(x=560, y=200)

label25 = ttk.Label(frame4, text="Chanfrein d'origine", font=custom_font3, foreground="grey", background="white")
label25.place(x=360, y=220)

label26 = ttk.Label(frame4, text="Oxycoupage", font=custom_font3, foreground="grey", background="white")
label26.place(x=560, y=220)

label27 = ttk.Label(frame4, text="Séchage / dégourdissage", font=custom_font3, foreground="grey", background="white")
label27.place(x=360, y=240)

label28 = ttk.Label(frame4, text="Température de préchauffage", font=custom_font3, foreground="grey",
                    background="white")
label28.place(x=360, y=260)

label29 = ttk.Label(frame4, text="Température entre passes", font=custom_font3, foreground="grey", background="white")
label29.place(x=360, y=280)

label30 = ttk.Label(frame4, text="Type", font=custom_font3, foreground="grey", background="white")
label30.place(x=360, y=300)

label31 = ttk.Label(frame4, text="Longueur minimale soudée avant le retrait du dispositif d'accostage",
                    font=custom_font3, foreground="grey", background="white")
label31.place(x=360, y=320)

label22 = ttk.Label(frame4, text="Passes", font=custom_font3, foreground="grey", background="white")
label22.place(x=360, y=340)

# Charger une image avec PIL
image_path3 = "logoexcel.png"
image3 = Image.open(image_path3)
image3 = image3.resize((200, 200))
photo3 = ImageTk.PhotoImage(image3)

# Ajouter l'image à la première frame
image_label3 = tk.Label(frame5, image=photo3, bg="white")
image_label3.place(x=327, y=20)

# Ajouter un label et un bouton
label11 = ttk.Label(frame5, text="Télécharger le fichier Excel du DMOS", font=custom_font, background="white")
label11.place(relx=0.5, anchor='center', y=230)

button8 = ttk.Button(frame5, text="Télécharger", command=lambda: show_frame(frame5), style="TButton")
button8.place(relx=0.5, anchor='center', y=300)

button6 = ttk.Button(frame5, text="Retour", command=lambda: show_frame(frame4), style="TButton")
button6.place(x=25, y=420)

button7 = ttk.Button(frame5, text="Quitter", command=lambda: show_frame(frame5), style="TButton")
button7.place(x=745, y=420)

label10 = ttk.Label(frame5, text="Application en Bêta - LT", font=custom_font2, foreground="grey", background="white")
label10.place(relx=0.5, anchor='center', y=460)

show_frame(frame1)

# Démarrer la boucle principale
root.mainloop()
