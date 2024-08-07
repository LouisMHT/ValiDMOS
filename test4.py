import pandas as pd
import os
from tkinter import Tk, filedialog

# Créer des données
data = {
    'Nom': ['Alice', 'Bob', 'Charlie'],
    'Âge': [25, 30, 35],
    'Ville': ['Paris', 'Lyon', 'Marseille']
}

# Créer un DataFrame pandas à partir des données
df = pd.DataFrame(data)

# Cacher la fenêtre principale de tkinter
root = Tk()
root.withdraw()

# Ouvrir une boîte de dialogue pour choisir le dossier
dossier = filedialog.askdirectory()

# Vérifier si un dossier a été sélectionné
if dossier:
    # Spécifier le nom du fichier
    nom_fichier = 'output.xlsx'

    # Créer le chemin complet
    chemin_complet = os.path.join(dossier, nom_fichier)

    # Exporter le DataFrame vers un fichier Excel à l'endroit spécifié
    df.to_excel(chemin_complet, index=False)

    print(f"Données exportées avec succès vers '{chemin_complet}'")
else:
    print("Aucun dossier sélectionné. Opération annulée.")
