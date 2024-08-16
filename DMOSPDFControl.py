import tkinter as tk


def on_resize(event):
    # Obtenir les dimensions de la fenêtre
    width = root.winfo_width()
    height = root.winfo_height()
    print(f"Taille actuelle de la fenêtre : {width}x{height}")


# Crée la fenêtre principale
root = tk.Tk()
root.title("Obtenir la Taille de la Fenêtre")
root.geometry("854x480")

# Lier l'événement de redimensionnement à la fonction on_resize
root.bind("<Configure>", on_resize)

# Démarrer la boucle principale
root.mainloop()
