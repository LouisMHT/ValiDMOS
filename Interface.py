import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter.font import Font
from PIL import Image, ImageTk

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

# Utilisation de place pour les frames
frame1.place(x=0, y=0, relwidth=1, relheight=1)
frame2.place(x=0, y=0, relwidth=1, relheight=1)

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

button = ttk.Button(frame1, text="Commencer")
button.place(relx=0.5, anchor='center', y=315)

label2 = ttk.Label(frame1, text="Application en Bêta - LT", font=custom_font2, foreground="grey", background="white")
label2.place(relx=0.5, anchor='center', y=460)

show_frame(frame1)

# Démarrer la boucle principale
root.mainloop()
