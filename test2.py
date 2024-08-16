import tkinter as tk
from tkinter import ttk

# Création de la fenêtre principale
root = tk.Tk()
root.title("Tableau avec Tkinter")

# Création du widget Treeview
tree = ttk.Treeview(root)

# Définition des colonnes
tree['columns'] = ('Nom', 'Age', 'Ville')

# Formatage des colonnes
tree.column('#0', width=0, stretch=tk.NO)  # Colonne fantôme pour l'index
tree.column('Nom', anchor=tk.W, width=120)
tree.column('Age', anchor=tk.CENTER, width=80)
tree.column('Ville', anchor=tk.W, width=100)

# Création des en-têtes de colonnes
tree.heading('#0', text='', anchor=tk.W)  # En-tête de la colonne fantôme
tree.heading('Nom', text='Nom', anchor=tk.W)
tree.heading('Age', text='Age', anchor=tk.CENTER)
tree.heading('Ville', text='Ville', anchor=tk.W)

# Insertion des données dans le tableau
data = [
    ('Alice', 30, 'Paris'),
    ('Bob', 25, 'Lyon'),
    ('Charlie', 35, 'Marseille'),
]

for item in data:
    tree.insert(parent='', index='end', iid=None, text='', values=item)

# Affichage du Treeview
tree.pack(pady=20)

# Lancement de la boucle principale Tkinter
root.mainloop()
