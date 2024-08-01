import tkinter as tk
import sys
import io

# Fonction pour rediriger la sortie vers le widget Text
class RedirectText(io.StringIO):
    def __init__(self, widget):
        super().__init__()
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)  # Faire défiler vers le bas si nécessaire

# Création de la fenêtre principale
root = tk.Tk()
root.title("Affichage de la sortie")

# Création du widget Text
text_widget = tk.Text(root, wrap=tk.WORD)
text_widget.pack(expand=True, fill='both')

# Redirection de sys.stdout vers le widget Text
sys.stdout = RedirectText(text_widget)

# Exemple de texte imprimé
print("Ceci est un test.")
print("Voici une autre ligne.")

# Ajout d'un bouton pour fermer la fenêtre
button = tk.Button(root, text="Fermer", command=root.quit)
button.pack()

# Démarrer la boucle principale de Tkinter
root.mainloop()
