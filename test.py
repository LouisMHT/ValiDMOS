import re

def process_data(data):
    # Initialiser les variables globales
    global Imputation, QMOS, ProcedeSoudage, Diametre, TypeJoint, Pression, Epaisseur, Norme, Courant, Passes
    global Meulage, Etuvage, Chanfrein, Oxycoupage, Sechage, Prechauffage, TemperatureEntrePasses, Type, Longueur

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

    def modify_string(data, keywords, attribute_name, slice_index):
        global_vars = globals()
        if any(keyword in data for keyword in keywords):
            global_vars[attribute_name] = data[slice_index:]
            return data[slice_index:]
        return data

    modifications = [
        (['Imputation'], 'Imputation', 16),
        (['QMOS'], 'QMOS', 18),
        (['Procédé'], 'ProcedeSoudage', 19),
        (['extérieur'], 'Diametre', 10),
        (['joint'], 'TypeJoint', 14),
        (['Pression'], 'Pression', 29),
        (['Epaisseur'], 'Epaisseur', 10),
        (['Norme'], 'Norme', 13),
        (['CC'], 'Courant', 0),
        (['%'], 'Passes', 2),
        (['Meulage'], 'Meulage', 8),
        (['Etuvage'], 'Etuvage', 23),
        (['Chanfrein'], 'Chanfrein', 20),
        (['Oxycoupage'], 'Oxycoupage', 11),
        (['Séchage'], 'Sechage', 23),
        (['préchauffage'], 'Prechauffage', 33),
        (['passes'], 'TemperatureEntrePasses', 30),
        (['Type'], 'Type', 5),
        (['Longueur'], 'Longueur', 68),
    ]

    for keywords, attribute_name, slice_index in modifications:
        cleaned_data_list = [modify_string(data, keywords, attribute_name, slice_index) for data in cleaned_data_list]

    Courant = Courant[:2]
    Oxycoupage = Oxycoupage[:3]

    print(Imputation)
    print(QMOS)
    print(ProcedeSoudage)

    print(Diametre)
    print(round(len(Diametre)/2))
    n = round(len(Diametre)/2)
    Diametre1 = Diametre[:n]
    Diametre1 = Diametre1.replace(" ", "")
    print(Diametre1)
    Diametre2 = Diametre[n:]
    Diametre2 = Diametre2.replace(" ", "")
    print(Diametre2)

    print(TypeJoint)
    print(Pression)

    print(Epaisseur)
    i = round(len(Epaisseur)/2)
    print(i)
    Epaisseur1 = Epaisseur[:i]
    Epaisseur1 = Epaisseur1.replace(" ", "")
    print(Epaisseur1)
    Epaisseur2 = Epaisseur[i:]
    Epaisseur2 = Epaisseur2.replace(" ", "")
    print(Epaisseur2)

    print(Norme)
    keywordannee = "Année"
    if keywordannee in Norme:
        Norme1 = Norme[:18]
        print(Norme1)
        Norme2 = Norme[19:]
        print(Norme2)
    else:
        f = round(len(Norme)/2)
        Norme1 = Norme[:f]
        print(Norme1)
        Norme2 = Norme[f:]
        print(Norme2)

    print(Courant)

    print(Passes)
    Chaine = Passes.split()
    print(Chaine)
    print(len(Chaine))
    num = len(Chaine)/14
    num = int(num)
    def diviser_liste_en_n_groupes(liste, nombre_de_groupes):
        taille_du_groupe, reste = divmod(len(liste), nombre_de_groupes)
        return [liste[i * taille_du_groupe + min(i, reste):(i + 1) * taille_du_groupe + min(i + 1, reste)] for i in
                range(nombre_de_groupes)]
    groupes = diviser_liste_en_n_groupes(Chaine, num)
    print(groupes)
    for i, groupe in enumerate(groupes):
        print(groupe)

    print(Meulage)
    print(Etuvage)
    print(Chanfrein)
    print(Oxycoupage)
    print(Sechage)
    print(Prechauffage)
    print(TemperatureEntrePasses)
    print(Type)
    print(Longueur)

    # Retourner les valeurs extraites


# Exemple de grande chaîne de caractères
data = """
GRDF Materiau de pe Sheu Iqlu ole soudage Type Intensité (A) 415% GRDF DESCRIPTIF DE MODE OPERATOIRE DE SOUDAGE Imputation/EOTP V61DD-RD33 DMOS N' 2 Adresse du chantier RUE DE I'AGRICULTURE TARBES 65 base Elément 1 Elément 2 QMOS de Référence 378785-2011-27262 Nature TUBE ACIER REDUCTION ACIER Fabricant GRDF AMSG SO PAU Adresse 67 rue Gaston PLANTE 64140 LONS Nuance & Ancien tube GRDF 1/1.1 P26SGH 1/1.1 Grou acier Procédé de soudage 111 extérieur 70 mm 70 mm Type de joint Bout à Bout (BW) Pression maximale de service MPB Epaisseur 2.9 mm 2.9 mm Norme/spécif Année de pose 1960 NF EN 10253-2 Schéma de préparation Disposition et nombre de passes 60 à 80' 2,0à 3,0 mm 1,5 à2,5 mm Paramètre de Procédé 111 d'enrobage RUTILE Type de courant CC - 1 soudeur Passe N' de Réf. Commerciale du Polarité Designation du métal Position Vitesse (cm/min) Tension (V) Energie (Kj/cm) I'electrode métal d'apport électrode d'apport soudage 425% 415% 425% 1 2.5 SAFER GTI (E42) E42 0 RC 11 PH 4.03 22.6 65 17.49 2 2.5 SAFER GTI (E42) E42 0 RC 11 PH 7.73 22.6 65 9.12 Mode de préparation des extrémités Meulage Non Etuvage des électrodes Non Coordonnateur en soudage Chanfrein d'origine Oui Oxycoupage Non Frederic HERBAUT Conditions thermiques Séchage_ dégourdissage 70 C si T< 5 C Temperature de préchauffage ('C) Sans préchauffage Température entre passes ('C) maxi 155'C Direction Réseaux Moven d'accostage S0 Type CLAMP Longueur minimale soudée avant le retrait du dispositif d'accostage Lmini = 55 mm Autre information DAMBAX PIERRE pierre.dambax@grdf.fr V7.5 29/07/2024  AMSG SO - PAU 67 rue Gaston PLANTE 64140 LONS 
"""
process_data(data)
