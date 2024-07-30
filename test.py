import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter.font import Font
from PIL import Image, ImageTk

# Crée la fenêtre principale avec le thème Adapta
root = ThemedTk(theme="adapta")  # Appliquer le thème Adapta
root.title("GRDF - DMOSControl")
root.geometry("1280x720")
root.resizable(False, False)
icon = tk.PhotoImage(file="logo3.png")
root.iconphoto(False, icon)
root.configure(bg="white")
custom_font = Font(family="Calibri", size=16, weight="bold")
custom_font2 = Font(family="Calibri", size=10, weight="bold", slant="italic")

# Charger une image avec PIL
image_path = "logo.png"
image = Image.open(image_path)
image = image.resize((298, 148))
photo = ImageTk.PhotoImage(image)

# Ajouter l'image à la première frame
image_label = tk.Label(image=photo, bg="white")
image_label.place(x=491, y=150)

# Ajouter un label et un bouton
label = ttk.Label(root, text="Bienvenue dans l'application de prévalidation de DMOS !", font=custom_font, background="white")
label.place(relx=0.5, anchor='center', y=330)

button = ttk.Button(root, text="Commencer")
button.place(relx=0.5, anchor='center', y=400)

label2 = ttk.Label(root, text="Application en Bêta - Louis THIERRY", font=custom_font2, foreground="grey", background="white")
label2.place(relx=0.5, anchor='center', y=700)

# Démarrer la boucle principale
root.mainloop()
