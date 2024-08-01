# Déclaration de la variable globale
reste_chaine = ""

def traiter_chaine(data):
    global reste_chaine
    # Supposons que nous voulons conserver seulement les 10 premiers caractères
    # et mettre le reste dans la variable globale
    premiers_dix_caracteres = data[:10]
    reste_chaine = data[10:]

    print(f"Premiers dix caractères : {premiers_dix_caracteres}")
    print(f"Reste de la chaîne : {reste_chaine}")

# Exemple d'utilisation
data = "Voici une chaîne de caractères longue."
traiter_chaine(data)

# Affichage du reste de la chaîne après l'appel de la fonction
print(f"Variable globale 'reste_chaine' après appel de la fonction : {reste_chaine}")
