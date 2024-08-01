import re


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



# Exemple de grande chaîne de caractères
data = """
GRDF Materiau de pe Sheu Iqlu ole soudage Type Intensité (A) 415% GRDF DESCRIPTIF DE MODE OPERATOIRE DE SOUDAGE Imputation/EOTP V61DD-RD33 DMOS N' 2 Adresse du chantier RUE DE I'AGRICULTURE TARBES 65 base Elément 1 Elément 2 QMOS de Référence 378785-2011-27262 Nature TUBE ACIER REDUCTION ACIER Fabricant GRDF AMSG SO PAU Adresse 67 rue Gaston PLANTE 64140 LONS Nuance & Ancien tube GRDF 1/1.1 P26SGH 1/1.1 Grou acier Procédé de soudage 111 extérieur 70 mm 70 mm Type de joint Bout à Bout (BW) Pression maximale de service MPB Epaisseur 2.9 mm 2.9 mm Norme/spécif Année de pose 1960 NF EN 10253-2 Schéma de préparation Disposition et nombre de passes 60 à 80' 2,0à 3,0 mm 1,5 à2,5 mm Paramètre de Procédé 111 d'enrobage RUTILE Type de courant CC - 1 soudeur Passe N' de Réf. Commerciale du Polarité Designation du métal Position Vitesse (cm/min) Tension (V) Energie (Kj/cm) I'electrode métal d'apport électrode d'apport soudage 425% 415% 425% 1 2.5 SAFER GTI (E42) E42 0 RC 11 PH 4.03 22.6 65 17.49 2 2.5 SAFER GTI (E42) E42 0 RC 11 PH 7.73 22.6 65 9.12 Mode de préparation des extrémités Meulage Non Etuvage des électrodes Non Coordonnateur en soudage Chanfrein d'origine Oui Oxycoupage Non Frederic HERBAUT Conditions thermiques Séchage_ dégourdissage 70 C si T< 5 C Temperature de préchauffage ('C) Sans préchauffage Température entre passes ('C) maxi 155'C Direction Réseaux Moven d'accostage S0 Type CLAMP Longueur minimale soudée avant le retrait du dispositif d'accostage Lmini = 55 mm Autre information DAMBAX PIERRE pierre.dambax@grdf.fr V7.5 29/07/2024  AMSG SO - PAU 67 rue Gaston PLANTE 64140 LONS 
"""

# Liste des mots-clés
keywords = ['DESCRIPTIF', 'Imputation', 'DMOS', 'Adresse', 'Elément', 'QMOS', 'Nature', 'Fabricant', 'Nuance', 'Grou',
            'Procédé', 'extérieur', 'Type', 'Pression', 'Epaisseur', 'Norme', 'Schéma', 'Disposition', 'Mode', 'Meulage',
            'Etuvage', 'Coordonnateur', 'Chanfrein', 'Oxycoupage', 'Conditions', 'Séchage', 'Température', 'Temperature',
            'Direction', 'Moyen', 'Moven', 'Longueur', 'Autre', 'Passe', '%', 'Paramètre', 'CC']

# Créer un motif d'expression régulière pour séparer aux mots-clés
pattern = r'({})'.format('|'.join(keywords))

# Diviser la chaîne en sections basées sur les mots-clés
sections = re.split(pattern, data)

# Initialiser des variables pour stocker les sections
current_section = ""
sections_list = []

for i, part in enumerate(sections):
    if part in keywords:
        if current_section:
            sections_list.append(current_section.strip())
        current_section = part
    else:
        current_section += part

# Ajouter la dernière section si elle existe
if current_section:
    sections_list.append(current_section.strip())


# Liste des mots-clés à rechercher
keywords_to_remove = ['GRDF', 'Intensité', 'Elément', 'Fabricant', 'Grou', 'Schéma', 'Direction', 'Moyen', 'Moven',
                      'Autre', 'Paramètre', 'Passe', '415', '425', 'enrobage', 'DESCRIPTIF', 'DMOS', 'Adresse',
                      'Mode', 'Conditions', 'Nature', 'Coordonnateur', 'Disposition', 'courant']

# Utiliser une liste de compréhension pour filtrer les chaînes
cleaned_data_list = [
    data for data in sections_list
    if not any(keyword in data for keyword in keywords_to_remove)
]
"""
# Afficher les résultats nettoyés
for cleaned_data in cleaned_data_list:
    print(cleaned_data)
"""

MotImputation = ['Imputation']
def modify_string(data, keywords):
    global Imputation
    # Si l'une des mots-clés est trouvée dans la chaîne
    if any(keyword in data for keyword in keywords):
        # Retirer les 3 derniers caractères de la chaîne
        Imputation = data[16:]
        return data[16:]
    return data

# Appliquer la modification à chaque chaîne de la liste
modified_data_list = [modify_string(data, MotImputation) for data in cleaned_data_list]
# Afficher les résultats modifiés
cleaned_data_list = modified_data_list

#print(Imputation)

MotQMOS = ['QMOS']
def modify_string(data, keywords):
    global QMOS
    # Si l'une des mots-clés est trouvée dans la chaîne
    if any(keyword in data for keyword in keywords):
        # Retirer les 3 derniers caractères de la chaîne
        QMOS = data[18:]
        return data[18:]
    return data


# Appliquer la modification à chaque chaîne de la liste
modified_data_list = [modify_string(data, MotQMOS) for data in cleaned_data_list]
# Afficher les résultats modifiés
cleaned_data_list = modified_data_list

MotProcede = ['Procédé']
def modify_string(data, keywords):
    global ProcedeSoudage
    # Si l'une des mots-clés est trouvée dans la chaîne
    if any(keyword in data for keyword in keywords):
        # Retirer les 3 derniers caractères de la chaîne
        ProcedeSoudage = data[19:]
        return data[19:]
    return data


# Appliquer la modification à chaque chaîne de la liste
modified_data_list = [modify_string(data, MotProcede) for data in cleaned_data_list]
# Afficher les résultats modifiés
cleaned_data_list = modified_data_list

Motexterieur = ['extérieur']
def modify_string(data, keywords):
    global Diametre
    # Si l'une des mots-clés est trouvée dans la chaîne
    if any(keyword in data for keyword in keywords):
        # Retirer les 3 derniers caractères de la chaîne
        Diametre = data[10:]
        return data[10:]
    return data


# Appliquer la modification à chaque chaîne de la liste
modified_data_list = [modify_string(data, Motexterieur) for data in cleaned_data_list]
# Afficher les résultats modifiés
cleaned_data_list = modified_data_list

Motjoint = ['joint']
def modify_string(data, keywords):
    global TypeJoint
    # Si l'une des mots-clés est trouvée dans la chaîne
    if any(keyword in data for keyword in keywords):
        # Retirer les 3 derniers caractères de la chaîne
        TypeJoint = data[14:]
        return data[14:]
    return data


# Appliquer la modification à chaque chaîne de la liste
modified_data_list = [modify_string(data, Motjoint) for data in cleaned_data_list]
# Afficher les résultats modifiés
cleaned_data_list = modified_data_list

MotPression = ['Pression']
def modify_string(data, keywords):
    global Pression
    # Si l'une des mots-clés est trouvée dans la chaîne
    if any(keyword in data for keyword in keywords):
        # Retirer les 3 derniers caractères de la chaîne
        Pression = data[29:]
        return data[29:]
    return data


# Appliquer la modification à chaque chaîne de la liste
modified_data_list = [modify_string(data, MotPression) for data in cleaned_data_list]
# Afficher les résultats modifiés
cleaned_data_list = modified_data_list

MotEpaisseur = ['Epaisseur']
def modify_string(data, keywords):
    global Epaisseur
    # Si l'une des mots-clés est trouvée dans la chaîne
    if any(keyword in data for keyword in keywords):
        # Retirer les 3 derniers caractères de la chaîne
        Epaisseur = data[10:]
        return data[10:]
    return data


# Appliquer la modification à chaque chaîne de la liste
modified_data_list = [modify_string(data, MotEpaisseur) for data in cleaned_data_list]
# Afficher les résultats modifiés
cleaned_data_list = modified_data_list

MotNorme = ['Norme']
def modify_string(data, keywords):
    global Norme
    # Si l'une des mots-clés est trouvée dans la chaîne
    if any(keyword in data for keyword in keywords):
        # Retirer les 3 derniers caractères de la chaîne
        Norme = data[13:]
        return data[13:]
    return data


# Appliquer la modification à chaque chaîne de la liste
modified_data_list = [modify_string(data, MotNorme) for data in cleaned_data_list]
# Afficher les résultats modifiés
cleaned_data_list = modified_data_list

MotCC = ['CC']
def modify_string(data, keywords):
    global Courant
    # Si l'une des mots-clés est trouvée dans la chaîne
    if any(keyword in data for keyword in keywords):
        # Retirer les 3 derniers caractères de la chaîne
        Courant = data[:-12]
        return data[:-12]
    return data


# Appliquer la modification à chaque chaîne de la liste
modified_data_list = [modify_string(data, MotCC) for data in cleaned_data_list]
# Afficher les résultats modifiés
cleaned_data_list = modified_data_list

MotPourcent = ['%']
def modify_string(data, keywords):
    global Passes
    # Si l'une des mots-clés est trouvée dans la chaîne
    if any(keyword in data for keyword in keywords):
        # Retirer les 3 derniers caractères de la chaîne
        Passes = data[2:]
        return data[2:]
    return data


# Appliquer la modification à chaque chaîne de la liste
modified_data_list = [modify_string(data, MotPourcent) for data in cleaned_data_list]
# Afficher les résultats modifiés
cleaned_data_list = modified_data_list

MotMeulage = ['Meulage']
def modify_string(data, keywords):
    global Meulage
    # Si l'une des mots-clés est trouvée dans la chaîne
    if any(keyword in data for keyword in keywords):
        # Retirer les 3 derniers caractères de la chaîne
        Meulage = data[8:]
        return data[8:]
    return data


# Appliquer la modification à chaque chaîne de la liste
modified_data_list = [modify_string(data, MotMeulage) for data in cleaned_data_list]
# Afficher les résultats modifiés
cleaned_data_list = modified_data_list

MotEtuvage = ['Etuvage']
def modify_string(data, keywords):
    global Etuvage
    # Si l'une des mots-clés est trouvée dans la chaîne
    if any(keyword in data for keyword in keywords):
        # Retirer les 3 derniers caractères de la chaîne
        Etuvage = data[23:]
        return data[23:]
    return data


# Appliquer la modification à chaque chaîne de la liste
modified_data_list = [modify_string(data, MotEtuvage) for data in cleaned_data_list]
# Afficher les résultats modifiés
cleaned_data_list = modified_data_list

MotChanfrein = ['Chanfrein']
def modify_string(data, keywords):
    global Chanfrein
    # Si l'une des mots-clés est trouvée dans la chaîne
    if any(keyword in data for keyword in keywords):
        # Retirer les 3 derniers caractères de la chaîne
        Chanfrein = data[20:]
        return data[20:]
    return data


# Appliquer la modification à chaque chaîne de la liste
modified_data_list = [modify_string(data, MotChanfrein) for data in cleaned_data_list]
# Afficher les résultats modifiés
cleaned_data_list = modified_data_list

MotOxy = ['Oxycoupage']
def modify_string(data, keywords):
    # Si l'une des mots-clés est trouvée dans la chaîne
    if any(keyword in data for keyword in keywords):
        # Retirer les 3 derniers caractères de la chaîne
        return data[:14]
    return data


# Appliquer la modification à chaque chaîne de la liste
modified_data_list = [modify_string(data, MotOxy) for data in cleaned_data_list]
# Afficher les résultats modifiés
cleaned_data_list = modified_data_list

MotOxy2 = ['Oxycoupage']
def modify_string(data, keywords):
    global Oxycoupage
    # Si l'une des mots-clés est trouvée dans la chaîne
    if any(keyword in data for keyword in keywords):
        # Retirer les 3 derniers caractères de la chaîne
        Oxycoupage = data[11:]
        return data[11:]
    return data


# Appliquer la modification à chaque chaîne de la liste
modified_data_list = [modify_string(data, MotOxy) for data in cleaned_data_list]
# Afficher les résultats modifiés
cleaned_data_list = modified_data_list

MotSechage = ['Séchage']
def modify_string(data, keywords):
    global Sechage
    # Si l'une des mots-clés est trouvée dans la chaîne
    if any(keyword in data for keyword in keywords):
        # Retirer les 3 derniers caractères de la chaîne
        Sechage = data[23:]
        return data[23:]
    return data


# Appliquer la modification à chaque chaîne de la liste
modified_data_list = [modify_string(data, MotSechage) for data in cleaned_data_list]
# Afficher les résultats modifiés
cleaned_data_list = modified_data_list

MotPrechauffage = ['préchauffage']
def modify_string(data, keywords):
    global Prechauffage
    # Si l'une des mots-clés est trouvée dans la chaîne
    if any(keyword in data for keyword in keywords):
        # Retirer les 3 derniers caractères de la chaîne
        Prechauffage = data[33:]
        return data[33:]
    return data


# Appliquer la modification à chaque chaîne de la liste
modified_data_list = [modify_string(data, MotPrechauffage) for data in cleaned_data_list]
# Afficher les résultats modifiés
cleaned_data_list = modified_data_list

Motpasses = ['passes']
def modify_string(data, keywords):
    global TemperatureEntrePasses
    # Si l'une des mots-clés est trouvée dans la chaîne
    if any(keyword in data for keyword in keywords):
        # Retirer les 3 derniers caractères de la chaîne
        TemperatureEntrePasses = data[30:]
        return data[30:]
    return data


# Appliquer la modification à chaque chaîne de la liste
modified_data_list = [modify_string(data, Motpasses) for data in cleaned_data_list]
# Afficher les résultats modifiés
cleaned_data_list = modified_data_list

MotType = ['Type']
def modify_string(data, keywords):
    global Type
    # Si l'une des mots-clés est trouvée dans la chaîne
    if any(keyword in data for keyword in keywords):
        # Retirer les 3 derniers caractères de la chaîne
        Type = data[5:]
        return data[5:]
    return data


# Appliquer la modification à chaque chaîne de la liste
modified_data_list = [modify_string(data, MotType) for data in cleaned_data_list]
# Afficher les résultats modifiés
cleaned_data_list = modified_data_list

MotLongueur = ['Longueur']
def modify_string(data, keywords):
    global Longueur
    # Si l'une des mots-clés est trouvée dans la chaîne
    if any(keyword in data for keyword in keywords):
        # Retirer les 3 derniers caractères de la chaîne
        Longueur = data[68:]
        return data[68:]
    return data


# Appliquer la modification à chaque chaîne de la liste
modified_data_list = [modify_string(data, MotLongueur) for data in cleaned_data_list]
# Afficher les résultats modifiés
cleaned_data_list = modified_data_list

"""
for cleaned_data in cleaned_data_list:
    print(cleaned_data)
"""

print(Imputation)
print(QMOS)
print(ProcedeSoudage)
print(Diametre)
print(TypeJoint)
print(Pression)
print(Epaisseur)
print(Norme)
print(Courant)
print(Passes)
print(Meulage)
print(Etuvage)
print(Chanfrein)
print(Oxycoupage)
print(Sechage)
print(Prechauffage)
print(TemperatureEntrePasses)
print(Type)
print(Longueur)
