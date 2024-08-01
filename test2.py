import re

# Exemple de liste de chaînes de caractères
data_list = [
    """
    Nom: Alice
    Âge: 30
    Poste: Ingénieur
    """,
    """
    Nom: Bob
    Âge: 25
    Poste: Designer
    """,
    """
    Nom: Carol
    Âge: 40
    Poste: Manager
    """
]

# Liste des mots-clés à supprimer
keywords_to_remove = ['Âge']

# Créer un motif d'expression régulière pour les mots-clés à supprimer
pattern_remove = r'\b(?:' + '|'.join(re.escape(keyword) for keyword in keywords_to_remove) + r'):\s*.*?\n'

# Initialiser une liste pour stocker les résultats nettoyés
cleaned_data_list = []

# Appliquer le nettoyage à chaque chaîne de la liste
for data in data_list:
    cleaned_data = re.sub(pattern_remove, '', data)
    cleaned_data_list.append(cleaned_data.strip())

# Afficher les résultats nettoyés
for cleaned_data in cleaned_data_list:
    print(cleaned_data)

