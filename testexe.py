import tkinter as tk
from tkinter import ttk

# Crée la fenêtre principale pour l'exemple
root = tk.Tk()
root.title("Exemple Treeview")
root.geometry("600x400")

# Crée un cadre pour contenir le Treeview
tables_frame = tk.Frame(root, bg="white")
tables_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Crée le Treeview avec plusieurs colonnes
treeview = ttk.Treeview(tables_frame, columns=("col1", "col2", "col3"), show="headings", height=5)

# Définir les en-têtes des colonnes
treeview.heading("col1", text="Imputation/EOTP")
treeview.heading("col2", text="DMOS N°")
treeview.heading("col3", text="QMOS de Référence")

# Définir la largeur des colonnes
treeview.column("col1", width=150, anchor=tk.W)
treeview.column("col2", width=150, anchor=tk.W)
treeview.column("col3", width=300, anchor=tk.W)

# Données à insérer dans le Treeview
tableau1 = [
    ("Data 1", "Value 1", "Reference 1"),
    ("Data 2", "Value 2", "Reference 2"),
    ("Data 3", "Value 3", "Reference 3"),
]

# Insérer les données dans le Treeview
for row in tableau1:
    treeview.insert("", tk.END, values=row)

# Pack le Treeview
treeview.pack(fill=tk.BOTH, expand=True)

# Lancer la boucle principale
root.mainloop()
