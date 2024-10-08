# Importation des modules nécessaires
import tkinter as tk  # Interface graphique avec Tkinter
from tkinter import ttk  # Extension de Tkinter pour des widgets thématisés
from ttkthemes import ThemedTk  # Support des thèmes pout Tkinter
from tkinter.font import Font  # Gestion des polices
from PIL import Image, ImageTk  # Gestion des images avec PIL (pillow)
from tkinter import filedialog, messagebox  # Pour boîtes de dialogue
import fitz  # PyMuPDF pour travailler avec des fichiers PDF
import easyocr  # OCR (Reconnaissance Optique de Caractères) avec EasyOCR
import io  # Gestion des flux d'entrée/sortie
import numpy as np  # Calcul numérique et manipulation de tableaux
import re  # Expressions régulières pour le traitement des chaînes
import os  # Module pour les opérations système
import cv2  # OpenCV, pour la manipulation d'images
import pdfplumber  # Extraction de texte et tables des fichiers PDF
import pandas as pd  # Manipulation et analyse des données
import sys  # Module système
import urllib.parse  # Parsing et manipulation des URLs
from reportlab.lib.pagesizes import A4  # Gestion des formats de page (ici A4)
from reportlab.lib import colors  # Couleurs pour le rapport PDF
from reportlab.lib.units import cm  # Conversion d'unités (cm)
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer  # Création de rapports PDF
from reportlab.platypus import Image as mage  # Inclusion d'images dans les rapports PDF
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle  # Styles pour les paragraphes
import webbrowser  # Ouvrir des pages web avec le navigateur
import csv  # Gestion des fichiers CSV


# Initialisation de diverses variables globales
all_text_info = []  # Contient les informations textuelles extraites
all_passes = []  # Contient les passes extraites
Liste_Excel = []  # Liste pour les données Excel
MsgValide = []  # Message de validation
MsgErreur = []  # Message d'erreur
chemins_fichiers = None  # Stockage des chemins de fichiers
Etat = []  # Contient l'état des fichiers traités
MsgValides = []  # Messages de validation
MsgErreurs = []  # Messages d'erreur


# Fonction pour basculer entre les différentes frames de l'interface
def show_frame(frame):
    frame.tkraise()


# Fonction pour analyser un DMOS en PDF
def scan(chemin_fichier):
    # Déclaration des variables globales
    global Etat
    global MsgErreurs
    global MsgValides
    global all_text_info
    global all_passes
    try:
        # Variables locales pour stocker les données extraites
        all_text = []
        all_extracted_text = []
        extratext = []
        pdf_file = chemin_fichier  # Chemin du fichier PDF à traiter
        all_tables = []
        all_tables_origin = []
        all_text_infotemp = []
        all_passestemp = []
        Liste_Excel = []

        document = fitz.open(chemin_fichier)  # Ouvre le fichier PDF avec PyMuPDF

        # Vérifier chaque page du document
        for page_num in range(len(document)):
            page = document.load_page(page_num)  # Charge une page du PDF
            text = page.get_text()  # Extrait le texte de la page

            # Si du texte est trouvé sur la page, ce n'est pas un PDF scanné
            if text.strip():
                print(f"Texte trouvé dans le fichier {chemin_fichier}, page {page_num}")

                # Listes de mots-clés pour lesquels ajouter un espace après le mot-clé
                keywords_to_add_space_after = ["DESCRIPTIF", "OPERATOIRE", "DMOS", "Matériau", "Adresse", "EOTP",
                                               ":",
                                               "chantier", "QMOS", "Procédé", "Nature", "Type", "Epaisseur",
                                               "Paramètre",
                                               "Parametre", "1.1", "1.2", "Température", "Temperature", "Pression",
                                               "maximale",
                                               "enrobage",
                                               "Oui", "Non", "Meulage", "Etuvage", "Chanfrein", "origine",
                                               "accostage",
                                               "dispositif", "Oxycoupage", "mm", "cm"]

                # Listes de mots-clés pour lesquels ajouter un espace avant et après le mot-clé
                keywords_to_add_double_space = ["MODE", "Elément", "Référence", "soudage", "extérieur", "joint",
                                                "courant",
                                                "service", "passes", "électrodes"]

                # Listes de mots-clés pour lesquels ajouter un espace avant le mot-clé
                keywords_to_add_space_before = ["SOUDAGE", "chantier", "soudeur", "Direction"]

                # Listes de mots-clés pour diviser les chaînes de caractères
                keywords_to_split = ["Adresse", "DMOS", "Matériau", "Nuance", "Ø", "Etuvage", "Oxycoupage",
                                     "Coordonnateur",
                                     "Direction"]

                # Listes de mots-clés à garder
                keywords_to_keep = ["Imputation", "EOTP", "DMOS", "QMOS", "1.1", "Procédé", "extérieur", "joint",
                                    "Epaisseur", "Pression", "Paramètre", "Meulage", "Etuvage", "Chanfrein",
                                    "Oxycoupage",
                                    "Séchage", "Sechage", "préchauffage", "prechauffage", "entre", "Température",
                                    "Temperature",
                                    "Type", "dispositif", "Norme", "@"]

                # Créer un motif d'expression régulière pour diviser le texte aux mots-clés
                pattern = r'({})'.format('|'.join(keywords_to_split))

                # Ouvrir le PDF avec pdfplumber pour extraire le texte
                with pdfplumber.open(pdf_file) as pdf:
                    for page in pdf.pages:

                        # Extraction des caractères individuels avec les stratégies "text"
                        table_settings = {
                            "vertical_strategy": "text",
                            "horizontal_strategy": "text"
                        }

                        # Extraction du texte à partir de la page
                        tables = page.extract_tables(table_settings)

                        # Nettoyage des tables extraites
                        for table in tables:
                            # Supprimer les éléments vides dans chaque ligne du tableau
                            cleaned_table = [[cell for cell in row if cell] for row in table]

                            # Supprimer les lignes vides (qui peuvent être des listes vides après nettoyage)
                            cleaned_table = [row for row in cleaned_table if row]

                            # Fusionner les chaînes de caractères dans chaque ligne
                            merged_table = [" ".join(row) for row in cleaned_table]

                            # Supprimer les espaces dans chaque chaîne de caractères fusionnée
                            cleaned_and_merged_table = [row.replace(" ", "") for row in merged_table]

                            final_table = []
                            for row in cleaned_and_merged_table:
                                # Ajouter un espace avant ou après certains mots-clés spécifiques (listes au-dessus)
                                for keyword in keywords_to_add_space_after:
                                    row = row.replace(keyword, keyword + " ")
                                for keyword in keywords_to_add_double_space:
                                    row = row.replace(keyword, " " + keyword + " ")
                                for keyword in keywords_to_add_space_before:
                                    row = row.replace(keyword, " " + keyword)

                                # Si on a un - au début de la chaîne de caractère, on le supprime
                                if row.startswith("-"):
                                    row = row[1:]

                                # Diviser la chaîne en sections basées sur les mots-clés
                                sections = re.split(pattern, row)

                                # Initialiser des variables pour stocker les sections
                                current_section = ""
                                sections_list = []

                                # Boucle for pour séparer les chaines de caractère avec les mots-clés
                                for i, part in enumerate(sections):
                                    if part in keywords_to_split:
                                        if current_section:
                                            sections_list.append(current_section.strip())
                                        current_section = part
                                    else:
                                        current_section += part

                                # Ajouter la dernière section si elle existe
                                if current_section:
                                    sections_list.append(current_section.strip())

                                final_table.extend(sections_list)

                                # Boucle pour garder les chaines de caractère avec les mots-clés
                                chaines_filtrees = [chaine for chaine in final_table if
                                                    any(mot_cle in chaine for mot_cle in
                                                        keywords_to_keep)]

                            # Filtrage et tri des passes
                            for row in merged_table:
                                chaines_filtrees_origin = [chaine for chaine in merged_table if chaine[0].isdigit()]
                                if not chaines_filtrees_origin[0].startswith('1'):
                                    chaines_filtrees_origin.pop(0)
                                if not chaines_filtrees_origin[-1].startswith(str(len(chaines_filtrees_origin))):
                                    chaines_filtrees_origin.pop(-1)

                            all_tables.append(chaines_filtrees)
                            all_tables_origin.append(chaines_filtrees_origin)

                # Sécurité pour les listes, s'il y a un schéma au début du document, il sera supprimé
                if len(all_tables[0]) <= 18:
                    all_tables.pop(0)

                # Tri des chaines de caractère
                for table in all_tables:
                    table[0] = table[0][18:]
                    table[1] = table[1][7:]
                    table[2] = table[2][20:]

                    table[4] = table[4][21:]
                    table[5] = table[5][12:]
                    table[6] = table[6][16:]
                    table[7] = table[7][10:]
                    table[8] = table[8][31:]
                    table[9] = table[9].replace(" ", "")
                    table[9] = table[9][12:]
                    if "Année" in table[9]:
                        temp1 = table[9][:16]
                        temp2 = table[9][16:]
                        table[9] = temp1 + " " + temp2
                    else:
                        temp1 = table[9][:11]
                        temp2 = table[9][11:]
                        table[9] = temp1 + " " + temp2
                    table[10] = table[10][51:]
                    table[10] = table[10].replace(' ', '')
                    table[10] = table[10].replace('-', ' ')
                    table[10] = table[10].replace('Typedecourant', '')
                    table[11] = table[11][10:]
                    table[11] = table[11][:3]
                    table[12] = table[12][25:]
                    table[13] = table[13][22:]
                    table[13] = table[13][:3]
                    table[14] = table[14][13:]
                    table[14] = table[14][:3]
                    table[15] = table[15][23:]
                    table[16] = table[16][32:]
                    table[17] = table[17][31:]
                    table[18] = table[18][7:]
                    table[19] = table[19][25:]
                    table[19] = table[19].split(' ', 1)[0]

                # Division des chaines de caractère par les espaces
                for table in all_tables:
                    final_table_2 = []
                    for row in table:
                        # Diviser la chaîne par des espaces
                        sections = row.split()
                        final_table_2.extend(sections)
                    all_text_infotemp.append(final_table_2)

                # Tri des passes
                for table in all_tables_origin:
                    final_table_origin_2 = []
                    final_table_origin_3 = []
                    for row in table:
                        row2 = []
                        row3 = []
                        row4 = []
                        # Diviser la chaîne par des espaces
                        sections = row.split()
                        row2.append(sections)
                        row3.append(row2[0][0])
                        row3.append(row2[0][1])

                        # Trouver la position du '-'
                        position = 0
                        for i in range(len(row2[0])):
                            if row2[0][i] == '-':
                                position = i
                                break  # Sortir de la boucle une fois que le tiret est trouvé
                            elif row2[0][i] == '+':
                                position = i
                                break  # Sortir de la boucle une fois que le plus est trouvé

                        # Créer une liste qui va de la position 2 jusqu'à la position du tiret
                        liste = list(range(2, position))
                        rowbis = []
                        # Ajouter les éléments correspondants dans row3
                        for i in liste:
                            rowbis.append(row2[0][i])
                        fusion = ' '.join(rowbis)
                        if fusion[-2] == ' ':
                            fusion = fusion[:-2] + fusion[-1]
                        row3.append(fusion)
                        row3.append(row2[0][position])
                        position = position + 1
                        # Trouver la position de la position de soudage
                        position2 = 0
                        for i in range(len(row2[0])):
                            if row2[0][i] == 'PB':
                                position2 = i
                                break  # Sortir de la boucle une fois que le PB est trouvé
                            elif row2[0][i] == 'PA':
                                position2 = i
                                break  # Sortir de la boucle une fois que le PA est trouvé
                            elif row2[0][i] == 'PC':
                                position2 = i
                                break  # Sortir de la boucle une fois que le PC est trouvé
                            elif row2[0][i] == 'PH':
                                position2 = i
                                break  # Sortir de la boucle une fois que le PH est trouvé

                        # Créer une liste qui va de la position 2 jusqu'à la position du tiret
                        liste2 = list(range(position, position2))

                        rowbis2 = []
                        # Ajouter les éléments correspondants dans row3
                        for i in liste2:
                            rowbis2.append(row2[0][i])
                        fusion = ' '.join(rowbis2)
                        row3.append(fusion)
                        row3.append(row2[0][position2])

                        row3.append(row2[0][(position2 + 1)])
                        row3.append(row2[0][(position2 + 2)])
                        row3.append(row2[0][(position2 + 3)])
                        row3.append(row2[0][(position2 + 4)])

                        row4.append(row3)
                        final_table_origin_2.extend(row2)
                        final_table_origin_3.extend(row4)
                    if len(final_table_origin_3) == 0:
                        pass
                    else:
                        all_passestemp.append(final_table_origin_3)

                all_text_info.append(all_text_infotemp)
                all_passes.append(all_passestemp)

                break  # Passer au fichier suivant si du texte a été trouvé

        else:
            # Si aucune page n'a de texte, c'est un PDF scanné
            print(f"Aucun texte trouvé dans le fichier {chemin_fichier}. Scan probable.")
            try:
                # Initialiser le lecteur easyocr pour la langue française
                reader = easyocr.Reader(['fr'], model_storage_directory='model', download_enabled=False)

                # Ouvrir le PDF
                pdf_path = chemin_fichier
                document = fitz.open(pdf_path)

                # Variable pour regrouper toutes les informations extraites
                all_texts = []

                # Sélectionner la page (ici la première page, index 0)
                page = document[0]

                # Extraire l'image de la page
                image_list = page.get_images(full=True)
                for img_index, img in enumerate(image_list, start=1):
                    xref = img[0]
                    base_image = document.extract_image(xref)
                    image_bytes = base_image["image"]

                    # Convertir l'image en format PIL
                    image = Image.open(io.BytesIO(image_bytes))

                    # Convertir l'image PIL en tableau de pixels
                    image_np = np.array(image)

                    # Utiliser easyocr pour effectuer l'OCR
                    result = reader.readtext(image_np, detail=0)  # detail=0 pour obtenir seulement le texte

                    # Regrouper le texte extrait dans une seule variable
                    extracted_text = " ".join(result)
                    all_texts.append(extracted_text)

                # Fermer le document PDF
                document.close()

                # Afficher toutes les informations extraites
                all_extracted_text = " ".join(all_texts)

            except Exception as e:
                print(e)
                pass

            data = all_extracted_text

            # Initialiser les variables globales
            global Imputation, QMOS, ProcedeSoudage, Diametre, TypeJoint, Pression, Epaisseur, Norme, Courant, Passes, Nuance, DMOS
            global Meulage, Etuvage, Chanfrein, Oxycoupage, Sechage, Prechauffage, TemperatureEntrePasses, Type, Longueur, Mail, Soudeur, Enrobage

            Imputation = ''
            DMOS = ''
            QMOS = ''
            Nuance = ''
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
            Mail = ''
            Soudeur = ''
            Enrobage = ''

            # Liste des mots-clés
            keywords = ['DESCRIPTIF', 'Imputation', 'DMOS', 'Adresse', 'Elément', 'QMOS', 'Nature', 'Fabricant',
                        'Nuance',
                        'Grou',
                        'Procédé', 'extérieur', 'Type', 'Pression', 'Epaisseur', 'Norme', 'Schéma', 'Disposition',
                        'Mode',
                        'Meulage',
                        'Etuvage', 'Coordonnateur', 'Chanfrein', 'Oxycoupage', 'Conditions', 'Séchage', 'Température',
                        'Temperature',
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

            # Liste des mots-clés à rechercher pour supprimer les chaines de caractère inutile
            keywords_to_remove = ['Materiau', 'Intensité', 'Elément', 'Fabricant', 'Grou', 'Schéma', 'Direction',
                                  'Moyen',
                                  'Moven',
                                  'Paramètre', 'Passe', '415', '425', 'DESCRIPTIF', 'Adresse',
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
                (['Procédé de soudage'], 'ProcedeSoudage', 19),
                (['extérieur'], 'Diametre', 10),
                (['joint'], 'TypeJoint', 14),
                (['Pression'], 'Pression', 29),
                (['Epaisseur'], 'Epaisseur', 10),
                (['Norme'], 'Norme', 13),
                (['enrobage'], 'Enrobage', 23),
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
                (['Nuance'], 'Nuance', 0),
                (['DMOS'], 'DMOS', 8),
                (['Autre'], 'Mail', 0),
            ]

            for keywords, attribute_name, slice_index in modifications:
                cleaned_data_list = [modify_string(data, keywords, attribute_name, slice_index) for data in
                                     cleaned_data_list]

            Soudeur = Courant
            Soudeur = Soudeur[5:]

            Courant = Courant[:2]
            Oxycoupage = Oxycoupage[:3]

            Nuance = Nuance[9:]

            Nuance = Nuance.replace(" ", "")

            mot = '1.1'
            Nuance = Nuance.replace(mot, mot + " ")
            Nuance = Nuance[:-1]

            NuanceSuppr = []
            NuanceSuppr = Nuance.split()

            Nuance1 = NuanceSuppr[0]
            Nuance2 = NuanceSuppr[1]

            Diametre1 = Diametre[:(round(len(Diametre) / 2))]
            Diametre1 = Diametre1.replace(" ", "")

            Diametre2 = Diametre[(round(len(Diametre) / 2)):]
            Diametre2 = Diametre2.replace(" ", "")

            Epaisseur1 = Epaisseur[:(round(len(Epaisseur) / 2))]
            Epaisseur1 = Epaisseur1.replace(" ", "")

            Epaisseur2 = Epaisseur[(round(len(Epaisseur) / 2)):]
            Epaisseur2 = Epaisseur2.replace(" ", "")

            keywordannee = "Année"
            if keywordannee in Norme:
                Norme1 = Norme[:18]
                Norme2 = Norme[19:]
            else:
                Norme1 = Norme[:(round(len(Norme) / 2))]
                Norme2 = Norme[(round(len(Norme) / 2)):]

            Chaine = Passes.split()

            num = len(Chaine) / 14
            num = int(num)

            def diviser_liste_en_n_groupes(liste, nombre_de_groupes):
                taille_du_groupe, reste = divmod(len(liste), nombre_de_groupes)
                return [liste[i * taille_du_groupe + min(i, reste):(i + 1) * taille_du_groupe + min(i + 1, reste)] for i
                        in
                        range(nombre_de_groupes)]

            groupes = diviser_liste_en_n_groupes(Chaine, num)

            all_text.append(Imputation)
            all_text.append(DMOS)
            all_text.append(QMOS)
            all_text.append(Nuance1)
            all_text.append(Nuance2)
            all_text.append(ProcedeSoudage)
            all_text.append(Diametre1)
            all_text.append(Diametre2)
            all_text.append(TypeJoint)
            all_text.append(Epaisseur1)
            all_text.append(Epaisseur2)
            all_text.append(Pression)
            all_text.append(Norme1)
            all_text.append(Norme2)
            all_text.append(Enrobage)
            all_text.append(Courant)
            all_text.append(Soudeur)
            all_text.append(Meulage)
            all_text.append(Etuvage)
            all_text.append(Chanfrein)
            all_text.append(Oxycoupage)
            all_text.append(Sechage)
            all_text.append(Prechauffage)
            all_text.append(TemperatureEntrePasses)
            all_text.append(Type)
            all_text.append(Longueur)

            all_text.append(Mail)

            mail = all_text[-1].split()
            resultat = []
            for chaine in mail:
                if '@' in chaine:
                    resultat.append(chaine)
            all_text[-1] = resultat[0]

            # Chemin vers le fichier PDF
            pdf_path = chemin_fichier

            # Ouvrir le fichier PDF
            pdf_document = fitz.open(pdf_path)

            # Convertir chaque page du PDF en image

            # Charger la page
            page = pdf_document.load_page(0)

            # Définir le zoom (facteur de redimensionnement de l'image)
            zoom_x = 2.0  # facteur de zoom horizontal
            zoom_y = 2.0  # facteur de zoom vertical
            mat = fitz.Matrix(zoom_x, zoom_y)

            # Convertir la page en image
            pix = page.get_pixmap(matrix=mat)

            # Sauvegarder l'image en format PNG
            image_filename = 'page.png'
            pix.save(image_filename)

            # Fermer le document PDF
            pdf_document.close()

            def save_largest_table_image(image_path, output_file):
                # Charger l'image
                img = cv2.imread(image_path)

                # Convertir l'image en niveaux de gris
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Appliquer un seuillage pour binariser l'image
                _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

                # Détecter les contours dans l'image binaire
                contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                # Vérifier s'il y a des contours
                if not contours:
                    print("Aucun tableau détecté.")
                    return

                # Trouver le contour du tableau le plus grand
                largest_contour = max(contours, key=cv2.contourArea)

                # Dessiner un rectangle autour du contour le plus grand
                x, y, w, h = cv2.boundingRect(largest_contour)
                largest_table = img[y:y + h, x:x + w]

                # Sauvegarder l'image du plus grand tableau
                cv2.imwrite(output_file, largest_table)

            # Chemin vers l'image d'origine
            image_path = 'page.png'
            # Fichier où l'image du plus grand tableau sera sauvegardée
            output_file = 'plus_grand_tableau.png'

            # Exécuter la fonction
            save_largest_table_image(image_path, output_file)

            # Charger l'image d'origine
            img = cv2.imread(output_file)

            # Obtenir les dimensions de l'image
            height, width = img.shape[:2]

            # Spécifier les pourcentages pour chaque partie (somme égale 100)
            percentages = [28.2, 6.3, 1.5, 21, 43]

            # Somme des pourcentages égale à 100
            if sum(percentages) != 100:
                raise ValueError("La somme des pourcentages spécifiés ne correspond pas à 100")

            # Calculer les largeurs en pixels en fonction des pourcentages
            widths = [int(p * width / 100) for p in percentages]

            # Découper l'image selon les largeurs calculées
            parts = []
            current_x = 0
            for w in widths:
                part = img[:, current_x:current_x + w]
                parts.append(part)
                current_x += w

            # Sélectionner trois parties
            selected_parts = [parts[0], parts[2], parts[4]]

            # Assembler les parties sélectionnées horizontalement
            assembled_image = np.hstack(selected_parts)

            # Sauvegarder l'image assemblée
            cv2.imwrite('assembled_image.png', assembled_image)

            # Initialiser le lecteur OCR
            reader = easyocr.Reader(['fr'], model_storage_directory='model', download_enabled=False)

            # Lire le texte de l'image assemblée
            results = reader.readtext('assembled_image.png')

            # Extraire et afficher uniquement le texte détecté
            extracted_text = " ".join([text for (_, text, _) in results])
            extracted_text = extracted_text.replace("+", " + ").replace("-", " - ")

            extratextbis = extracted_text.split()

            verif = []
            # Parcourir la liste tout en vérifiant la chaîne actuelle et la suivante
            for i in range(len(extratextbis) - 1):
                chaine = extratextbis[i]
                chaine_suivante = extratextbis[i + 1]

                # Vérifier si la chaîne contient '+' ou '-' et si la suivante contient 'PH', 'PB', 'PA' ou 'PC'
                if ('+' in chaine or '-' in chaine) and (chaine_suivante in ['PH', 'PB', 'PA', 'PC']):
                    verif.append(extratextbis[i - 1])
                    extratext.append(chaine)

            resultotal = []
            k = 0
            result = []
            for groupe in groupes:
                result = []
                for chaine in groupe:
                    # Ajouter la chaîne actuelle à la liste de résultats
                    result.append(chaine)

                    # Vérifier si le mot est détecté
                    if verif[0] in chaine:
                        # Ajouter la nouvelle chaîne avec un "+" après le mot détecté
                        result.append(extratext[k])
                resultotal.append(result)
                k = k + 1
            extratext = resultotal

            o = 0
            newextra = []
            for table in extratext:
                tablefinal = []
                tablefinal.append(table[0])
                tablefinal.append(table[1])
                # Trouver la position du '-'
                position = 0
                for i in range(len(extratext[0])):
                    if extratext[0][i] == '-':
                        position = i
                        break  # Sortir de la boucle une fois que le tiret est trouvé
                    elif extratext[0][i] == '+':
                        position = i
                        break  # Sortir de la boucle une fois que le plus est trouvé

                # Créer une liste qui va de la position 2 jusqu'à la position du tiret
                liste = list(range(2, position))

                rowbis = []
                for n in liste:
                    rowbis.append(extratext[o][n])
                fusion = ' '.join(rowbis)
                if fusion[-2] == ' ':
                    fusion = fusion[:-2] + fusion[-1]
                tablefinal.append(fusion)
                tablefinal.append(extratext[o][position])
                position = position + 1

                position2 = 0
                for i in range(len(extratext[0])):
                    if extratext[0][i] == 'PB':
                        position2 = i
                        break
                    elif extratext[0][i] == 'PA':
                        position2 = i
                        break
                    elif extratext[0][i] == 'PC':
                        position2 = i
                        break
                    elif extratext[0][i] == 'PH':
                        position2 = i
                        break

                # Créer une liste qui va de la position 2 jusqu'à la position du tiret
                liste2 = list(range(position, position2))

                rowbis2 = []
                for i in liste2:
                    rowbis2.append(extratext[o][i])
                fusion = ' '.join(rowbis2)
                tablefinal.append(fusion)
                tablefinal.append(extratext[o][position2])

                tablefinal.append(extratext[o][(position2 + 1)])
                tablefinal.append(extratext[o][(position2 + 2)])
                tablefinal.append(extratext[o][(position2 + 3)])
                tablefinal.append(extratext[o][(position2 + 4)])

                newextra.append(tablefinal)
                o = o + 1

            extratext = newextra
            all_text_infotemp.append(all_text)
            all_text_info.append(all_text_infotemp)
            all_passestemp.append(extratext)
            all_passes.append(all_passestemp)

            os.remove('page.png')
            os.remove('plus_grand_tableau.png')
            os.remove('assembled_image.png')

        # Charger le fichier Excel
        file_path = 'QMOS/QMOS.xlsx'
        df = pd.read_excel(file_path)

        # Convertir le DataFrame en une liste de listes
        liste_de_listes = df.values.tolist()

        def find_position(data, keyword):
            for i, row in enumerate(data):  # Parcourt chaque ligne
                for j, value in enumerate(row):  # Parcourt chaque élément de la ligne
                    if value == keyword:  # Si l'élément correspond au mot clé
                        return (i, j)  # Retourne la position (ligne, colonne)
            return None  # Si le mot clé n'est pas trouvé

        # Recherche de la position du QMOS
        position = find_position(liste_de_listes, all_text_infotemp[0][2])

        # Si la position est trouvée
        if position:
            print(f"La référence du QMOS se trouve à la position : Ligne {position[0]}, Colonne {position[1]}")
            # Extraction des informations de la ligne trouvée
            nouvelle_liste = []
            nouvelle_liste.append(liste_de_listes[position[0]])
            liste_verification = []
            liste_verification.append(nouvelle_liste[0][0])
            if 'à' in str(nouvelle_liste[0][1]):
                temp = []
                temp.append(nouvelle_liste[0][1])
                temp2 = temp[0].split()
                liste_verification.append(float(temp2[0].replace(',', '.')))
                liste_verification.append(float(temp2[2].replace(',', '.')))
            else:
                liste_verification.append(nouvelle_liste[0][1])
            if 'à' in str(nouvelle_liste[0][2]):
                temp = []
                temp.append(nouvelle_liste[0][2])
                temp2 = temp[0].split()
                liste_verification.append(float(temp2[0].replace(',', '.')))
                liste_verification.append(float(temp2[2].replace(',', '.')))
            else:
                liste_verification.append(nouvelle_liste[0][2])
            liste_verification.append(nouvelle_liste[0][3])
            liste_verification.append(nouvelle_liste[0][4])
            liste_verification.append(nouvelle_liste[0][5])
            liste_verification.append(nouvelle_liste[0][6])
            liste_verification.append(nouvelle_liste[0][7])
            liste_verification.append(nouvelle_liste[0][8])
            if 'à' in str(nouvelle_liste[0][9]):
                temp = []
                temp.append(nouvelle_liste[0][9])
                temp2 = temp[0].split()
                liste_verification.append(float(temp2[0].replace(',', '.')))
                liste_verification.append(float(temp2[2].replace(',', '.')))
            else:
                liste_verification.append(nouvelle_liste[0][9])
            if 'à' in str(nouvelle_liste[0][10]):
                temp = []
                temp.append(nouvelle_liste[0][10])
                temp2 = temp[0].split()
                liste_verification.append(float(temp2[0].replace(',', '.')))
                liste_verification.append(float(temp2[2].replace(',', '.')))
            else:
                liste_verification.append(nouvelle_liste[0][10])
            if 'à' in str(nouvelle_liste[0][11]):
                temp = []
                temp.append(nouvelle_liste[0][11])
                temp2 = temp[0].split()
                liste_verification.append(float(temp2[0].replace(',', '.')))
                liste_verification.append(float(temp2[2].replace(',', '.')))
            else:
                liste_verification.append(nouvelle_liste[0][11])
            Liste_Excel = liste_verification

        else:
            print("Le mot clé n'a pas été trouvé.")
            print("QMOS INCONNU")

        MsgErreur = []
        MsgValide = []

        ExcelDiametreMin = Liste_Excel[1]
        ExcelDiametreMax = Liste_Excel[2]
        ExcelEpaisseurMin = Liste_Excel[3]
        ExcelEpaisseurMax = Liste_Excel[4]
        ExcelGroupeAcier1 = None
        ExcelGroupeAcier2 = None
        ExcelGroupeAcier = None
        ExcelPosition11 = None
        ExcelPosition12 = None
        ExcelPosition1 = None
        ExcelPosition21 = None
        ExcelPosition22 = None
        ExcelPosition2 = None
        ExcelDiametreElectrode1 = None
        ExcelDiametreElectrode11 = None
        ExcelDiametreElectrode12 = None

        if ',' in Liste_Excel[5]:
            ExcelGroupeAcier1 = Liste_Excel[5][:5]
            ExcelGroupeAcier2 = Liste_Excel[5][7:]
        else:
            ExcelGroupeAcier = Liste_Excel[5]
        if '/' in Liste_Excel[6]:
            ExcelPosition11 = Liste_Excel[6][:2]
            ExcelPosition12 = Liste_Excel[6][5:]
        else:
            ExcelPosition1 = Liste_Excel[6]
        ExcelPolarite1 = Liste_Excel[7]
        ExcelDiametreElectrode0 = Liste_Excel[8]
        if '/' in Liste_Excel[9]:
            ExcelPosition21 = Liste_Excel[9][:2]
            ExcelPosition22 = Liste_Excel[9][5:]
        else:
            ExcelPosition2 = Liste_Excel[9]
        ExcelPolarite2 = Liste_Excel[10]
        if len(Liste_Excel) == 15:
            ExcelDiametreElectrode1 = Liste_Excel[11]
        if len(Liste_Excel) == 16:
            ExcelDiametreElectrode11 = Liste_Excel[11]
            ExcelDiametreElectrode12 = Liste_Excel[12]
        ExcelNumPassesMin = Liste_Excel[-3]
        ExcelNumPassesMax = Liste_Excel[-2]
        ExcelNumSoudeur = Liste_Excel[-1]

        for table in all_text_infotemp:
            NumDMOS = int(table[1])
            VerifDiametre1 = float(table[6][:-2])
            VerifDiametre2 = float(table[7][:-2])
            if VerifDiametre1 >= ExcelDiametreMin and VerifDiametre1 <= ExcelDiametreMax:
                MsgValide.append("Diamètre extérieur élément 1 du DMOS N°" + str(NumDMOS) + " validé")
            else:
                MsgErreur.append("Diamètre extérieur élément 1 du DMOS N°" + str(NumDMOS) + " incorrect")
            if VerifDiametre2 >= ExcelDiametreMin and VerifDiametre2 <= ExcelDiametreMax:
                MsgValide.append("Diamètre extérieur élément 2 du DMOS N°" + str(NumDMOS) + " validé")
            else:
                MsgErreur.append("Diamètre extérieur élément 2 du DMOS N°" + str(NumDMOS) + " incorrect")
            if VerifDiametre1 == VerifDiametre2:
                MsgValide.append("Diamètre extérieur du DMOS N°" + str(NumDMOS) + " validé")
            else:
                MsgErreur.append("Diamètre extérieur du DMOS N°" + str(NumDMOS) + " incorrect")
            VerifEpaisseur1 = float(table[9][:-2])
            VerifEpaisseur2 = float(table[10][:-2])
            if VerifEpaisseur1 >= ExcelEpaisseurMin and VerifEpaisseur1 <= ExcelEpaisseurMax:
                MsgValide.append("Epaisseur élément 1 du DMOS N°" + str(NumDMOS) + " validé")
            else:
                MsgErreur.append("Epaisseur élément 1 du DMOS N°" + str(NumDMOS) + " incorrect")
            if VerifEpaisseur2 >= ExcelEpaisseurMin and VerifEpaisseur2 <= ExcelEpaisseurMax:
                MsgValide.append("Epaisseur élément 2 du DMOS N°" + str(NumDMOS) + " validé")
            else:
                MsgErreur.append("Epaisseur élément 2 du DMOS N°" + str(NumDMOS) + " incorrect")
            VerifGroupeAcier1 = table[3][-5:]
            VerifGroupeAcier2 = table[4][-5:]
            if ExcelGroupeAcier1 and ExcelGroupeAcier2:
                if ExcelGroupeAcier1 in VerifGroupeAcier1 or ExcelGroupeAcier2 in VerifGroupeAcier1:
                    MsgValide.append("Groupe Acier élément 1 du DMOS N°" + str(NumDMOS) + " validé")
                else:
                    MsgErreur.append("Groupe Acier élément 1 du DMOS N°" + str(NumDMOS) + " incorrect")
                if ExcelGroupeAcier1 in VerifGroupeAcier2 or ExcelGroupeAcier2 in VerifGroupeAcier2:
                    MsgValide.append("Groupe Acier élément 2 du DMOS N°" + str(NumDMOS) + " validé")
                else:
                    MsgErreur.append("Groupe Acier élément 2 du DMOS N°" + str(NumDMOS) + " incorrect")
            if ExcelGroupeAcier:
                if ExcelGroupeAcier in VerifGroupeAcier1:
                    MsgValide.append("Groupe Acier élément 1 du DMOS N°" + str(NumDMOS) + " validé")
                else:
                    MsgErreur.append("Groupe Acier élément 1 du DMOS N°" + str(NumDMOS) + " incorrect")
                if ExcelGroupeAcier in VerifGroupeAcier2:
                    MsgValide.append("Groupe Acier élément 2 du DMOS N°" + str(NumDMOS) + " validé")
                else:
                    MsgErreur.append("Groupe Acier élément 2 du DMOS N°" + str(NumDMOS) + " incorrect")
            VerifNumSoudeur = float(table[16][:1])
            if VerifNumSoudeur == ExcelNumSoudeur:
                MsgValide.append("Nombre de soudeur du DMOS N°" + str(NumDMOS) + " validé")
            else:
                MsgErreur.append("Nombre de soudeur du DMOS N°" + str(NumDMOS) + " incorrect")
        for table in all_passestemp:
            NumDMOS = int(all_text_infotemp[0][1])
            if len(table) >= ExcelNumPassesMin and len(table) <= ExcelNumPassesMax:
                MsgValide.append("Nombre de passes du DMOS N°" + str(NumDMOS) + " validé")
            else:
                MsgErreur.append("Nombre de passes du DMOS N°" + str(NumDMOS) + " incorrect")

            VerifDiametreElectrode1 = table[0][1]
            if float(VerifDiametreElectrode1) == ExcelDiametreElectrode0 or float(VerifDiametreElectrode1) == 2.0 or \
                    float(VerifDiametreElectrode1) == 2.5:
                MsgValide.append("Diamètre électrode première passe du DMOS N°" + str(NumDMOS) + " validé")
            else:
                MsgErreur.append("Diamètre électrode première passe du DMOS N°" + str(NumDMOS) + " incorrect")
            VerifPolarite1 = table[0][3]
            if '-' in VerifPolarite1:
                VerifPolarite1 = "Négative"
            elif '+' in VerifPolarite1:
                VerifPolarite1 = "Positive"
            if VerifPolarite1 in ExcelPolarite1:
                MsgValide.append("Polarité première passe du DMOS N°" + str(NumDMOS) + " validé")
            else:
                MsgErreur.append("Polarité première passe du DMOS N°" + str(NumDMOS) + " incorrect")
            VerifPosition1 = table[0][5]
            if ExcelPosition11 and ExcelPosition12:
                if ExcelPosition11 in VerifPosition1 or ExcelPosition12 in VerifPosition1:
                    MsgValide.append("Position première passe du DMOS N°" + str(NumDMOS) + " validé")
                else:
                    MsgErreur.append("Position première passe du DMOS N°" + str(NumDMOS) + " incorrect")
            if ExcelPosition1:
                if ExcelPosition1 in VerifPosition1:
                    MsgValide.append("Position première passe du DMOS N°" + str(NumDMOS) + " validé")
                else:
                    MsgErreur.append("Position première passe du DMOS N°" + str(NumDMOS) + " incorrect")
            numtemp = 2
            for row in table:
                if int(row[0]) == 1:
                    continue
                VerifDiametreElectrode2 = float(row[1])
                if ExcelDiametreElectrode11 and ExcelDiametreElectrode12:
                    if VerifDiametreElectrode2 >= ExcelDiametreElectrode11 and VerifDiametreElectrode2 <= ExcelDiametreElectrode12:
                        MsgValide.append(
                            "Diamètre électrode passe " + str(numtemp) + " du DMOS N°" + str(NumDMOS) + " validé")
                    else:
                        MsgErreur.append(
                            "Diamètre électrode passe " + str(numtemp) + " du DMOS N°" + str(NumDMOS) + " incorrect")
                if ExcelDiametreElectrode1:
                    if VerifDiametreElectrode2 == ExcelDiametreElectrode1:
                        MsgValide.append(
                            "Diamètre électrode passe " + str(numtemp) + " du DMOS N°" + str(NumDMOS) + " validé")
                    else:
                        MsgErreur.append(
                            "Diamètre électrode passe " + str(numtemp) + " du DMOS N°" + str(NumDMOS) + " incorrect")
                VerifPolarite2 = row[3]
                if '-' in VerifPolarite2:
                    VerifPolarite2 = "Négative"
                elif '+' in VerifPolarite2:
                    VerifPolarite2 = "Positive"
                if VerifPolarite2 in ExcelPolarite2:
                    MsgValide.append("Polarité passe " + str(numtemp) + " du DMOS N°" + str(NumDMOS) + " validé")
                else:
                    MsgErreur.append("Polarité passe " + str(numtemp) + " du DMOS N°" + str(NumDMOS) + " incorrect")
                VerifPosition2 = row[5]
                if ExcelPosition21 and ExcelPosition22:
                    if ExcelPosition21 in VerifPosition2 or ExcelPosition22 in VerifPosition2:
                        MsgValide.append("Position passe " + str(numtemp) + " du DMOS N°" + str(NumDMOS) + " validé")
                    else:
                        MsgErreur.append("Position passe " + str(numtemp) + " du DMOS N°" + str(NumDMOS) + " incorrect")
                if ExcelPosition2:
                    if ExcelPosition1 in VerifPosition1:
                        MsgValide.append("Position passe " + str(numtemp) + " du DMOS N°" + str(NumDMOS) + " validé")
                    else:
                        MsgErreur.append("Position passe " + str(numtemp) + " du DMOS N°" + str(NumDMOS) + " incorrect")
                numtemp = numtemp + 1

        # Résultats et état global
        MsgValides.append(MsgValide)
        MsgErreurs.append(MsgErreur)
        if len(MsgErreur) > 0:
            Etat.append("NON")
        else:
            Etat.append("OUI")
    except Exception as e:
        print(e)
        Etat.append("KO")
        Listetemp = [['']]
        MsgValides.append(Listetemp)
        MsgErreurs.append(Listetemp)
        all_text_info.append(Listetemp)
        all_passes.append(Listetemp)
        pass
    # Affichage des résultats dans la console
    print(Etat)
    print(MsgErreurs)
    print(MsgValides)
    print(all_text_info)
    print(all_passes)


# Fonction pour traiter les fichiers sélectionnés
def utiliser_fichiers():
    global chemins_fichiers
    global Etat
    # Vérifie si frame3 est affichée
    if frame3.winfo_ismapped():
        print("Frame 3 affichée")

        # Parcourir tous les fichiers sélectionnés
        for chemin_fichier in chemins_fichiers:
            print(f"Traitement du fichier : {chemin_fichier}")
            # Ouvrir le document PDF
            scan(chemin_fichier)
        if len(chemins_fichiers) == len(Etat):
            tableauframe4()
            root.after(2000, lambda: show_frame(frame4))


# Crée la fenêtre principale avec le thème Adapta
root = ThemedTk(theme="adapta")  # Appliquer le thème Adapta
root.title("GRDF - ValiDMOS")  # Définit le titre de la fenêtre
root.geometry("1000x560")  # Définit la taille de la fenêtre
root.minsize(1000, 560)  # Fixe la taille minimale
icon = tk.PhotoImage(file="images/logo3.png")  # Charge une image pour l'icône de l'application
root.iconphoto(False, icon)  # Définit l'icône de la fenêtre
root.configure(bg="white")  # Définit le fond blanc de la fenêtre principale

# Crée plusieurs frames (zones de contenu)
frame1 = tk.Frame(root, bg="white")
frame2 = tk.Frame(root, bg="white")
frame3 = tk.Frame(root, bg="white")
frame4 = tk.Frame(root, bg="white")
frame5 = tk.Frame(root, bg="white")
frame6 = tk.Frame(root, bg="white")

# Utilisation de grid pour les frames
frame1.grid(row=0, column=0, sticky='nsew')
frame2.grid(row=0, column=0, sticky='nsew')
frame3.grid(row=0, column=0, sticky='nsew')
frame4.grid(row=0, column=0, sticky='nsew')
frame5.place(x=0, y=0, relwidth=1, relheight=1)
frame6.grid(row=0, column=0, sticky='nsew')

# Configurer la grille de la fenêtre principale pour redimensionner les frames
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Configurer la grille des frames pour redimensionner les widgets à l'intérieur
frame1.grid_rowconfigure(0, weight=1)
frame1.grid_rowconfigure(1, weight=1)
frame1.grid_rowconfigure(2, weight=1)
frame1.grid_rowconfigure(3, weight=1)
frame1.grid_rowconfigure(4, weight=1)
frame1.grid_rowconfigure(5, weight=1)
frame1.grid_rowconfigure(6, weight=1)
frame1.grid_rowconfigure(7, weight=1)
frame1.grid_rowconfigure(8, weight=1)
frame1.grid_rowconfigure(9, weight=1)
frame1.grid_rowconfigure(10, weight=1)
frame1.grid_rowconfigure(11, weight=1)
frame1.grid_rowconfigure(12, weight=1)
frame1.grid_rowconfigure(13, weight=1)
frame1.grid_rowconfigure(14, weight=1)
frame1.grid_rowconfigure(15, weight=1)
frame1.grid_rowconfigure(16, weight=1)
frame1.grid_rowconfigure(17, weight=1)
frame1.grid_rowconfigure(18, weight=1)
frame1.grid_rowconfigure(19, weight=1)
frame1.grid_columnconfigure(0, weight=1)

# Définition des polices de caractères personnalisées
custom_font = Font(family="Calibri", size=16, weight="bold")
custom_font2 = Font(family="Calibri", size=10, weight="bold", slant="italic")
custom_font3 = Font(family="Calibri", size=100, weight="bold")
custom_font4 = Font(family="Calibri", size=150, weight="bold")

# Charger une image avec PIL
image_path = "images/logo.png"
image = Image.open(image_path)
image = image.resize((298, 148))
photo = ImageTk.PhotoImage(image)

# Ajouter l'image à la première frame
image_label = tk.Label(frame1, image=photo, bg="white")
image_label.grid(row=4, column=0, pady=20)

# Ajouter un label et un bouton
label = ttk.Label(frame1, text="Bienvenue dans l'application de prévalidation de DMOS !", font=custom_font,
                  background="white")
label.grid(row=5, column=0, pady=10)

# Ajout d'un bouton pour passer à la frame suivante (frame2)
button = ttk.Button(frame1, text="Commencer", command=lambda: show_frame(frame2), style="TButton")
button.grid(row=6, column=0, pady=10, sticky='n')

# Configurer la grille des frames pour redimensionner les widgets à l'intérieur
frame2.grid_rowconfigure(0, weight=1)
frame2.grid_rowconfigure(1, weight=1)
frame2.grid_rowconfigure(2, weight=1)
frame2.grid_rowconfigure(3, weight=1)
frame2.grid_rowconfigure(4, weight=1)
frame2.grid_rowconfigure(5, weight=1)
frame2.grid_rowconfigure(6, weight=1)
frame2.grid_rowconfigure(7, weight=1)
frame2.grid_rowconfigure(8, weight=1)
frame2.grid_rowconfigure(9, weight=1)
frame2.grid_rowconfigure(10, weight=1)
frame2.grid_rowconfigure(11, weight=1)
frame2.grid_rowconfigure(12, weight=1)
frame2.grid_rowconfigure(13, weight=1)
frame2.grid_rowconfigure(14, weight=1)
frame2.grid_rowconfigure(15, weight=1)
frame2.grid_rowconfigure(16, weight=1)
frame2.grid_rowconfigure(17, weight=1)
frame2.grid_rowconfigure(18, weight=1)
frame2.grid_rowconfigure(19, weight=1)
frame2.grid_columnconfigure(0, weight=1)
frame2.grid_columnconfigure(1, weight=1)
frame2.grid_columnconfigure(2, weight=1)
frame2.grid_columnconfigure(3, weight=1)
frame2.grid_columnconfigure(4, weight=1)
frame2.grid_columnconfigure(5, weight=1)
frame2.grid_columnconfigure(6, weight=1)
frame2.grid_columnconfigure(7, weight=1)
frame2.grid_columnconfigure(8, weight=1)
frame2.grid_columnconfigure(9, weight=1)
frame2.grid_columnconfigure(10, weight=1)
frame2.grid_columnconfigure(11, weight=1)
frame2.grid_columnconfigure(12, weight=1)
frame2.grid_columnconfigure(13, weight=1)
frame2.grid_columnconfigure(14, weight=1)
frame2.grid_columnconfigure(15, weight=1)
frame2.grid_columnconfigure(16, weight=1)

# Charger une image avec PIL
image_path2 = "images/logopdf.png"
image2 = Image.open(image_path2)
image2 = image2.resize((128, 128))
photo2 = ImageTk.PhotoImage(image2)

# Ajouter l'image à la première frame
image_label2 = tk.Label(frame2, image=photo2, bg="white")
image_label2.grid(row=2, column=8, pady=20)

# Ajouter un label et un bouton
label3 = ttk.Label(frame2, text="Sélectionner le fichier pdf", font=custom_font, background="white")
label3.grid(row=3, column=8, pady=10, sticky='n')


# Fonction pour ouvrir un explorateur de fichiers et choisir des fichiers
def ouvrir_fichiers():
    global chemins_fichiers
    # Ouvre la boîte de dialogue pour sélectionner plusieurs fichiers
    chemins_fichiers = filedialog.askopenfilenames(
        title="Sélectionner un ou plusieurs fichiers",
        filetypes=[("Tous les fichiers", "*.*"), ("Fichiers texte", "*.txt")]
    )
    # Affiche les chemins des fichiers sélectionnés
    if chemins_fichiers:
        fichiers = "\n".join(chemins_fichiers)  # Concaténer les chemins de fichiers pour les afficher
        label_fichier.config(text=fichiers)
    else:
        label_fichier.config(text="Aucun fichier sélectionné")


# Fonction pour valider la sélection de fichiers
def valider():
    # Vérifie si un fichier a été sélectionné
    if not chemins_fichiers:
        # Affiche un message d'erreur si aucun fichier n'a été sélectionné
        messagebox.showerror("Erreur", "Veuillez sélectionner un fichier avant de valider.")
    else:
        show_frame(frame3)
        root.after(2000, lambda: utiliser_fichiers())


# Crée un label pour afficher le chemin du fichier sélectionné
label_fichier = ttk.Label(frame2, text="Aucun fichier sélectionné")
label_fichier.grid(row=4, column=8, pady=10)

# Crée un bouton pour ouvrir la boîte de dialogue de sélection de fichier
bouton_ouvrir = ttk.Button(frame2, text="Ouvrir un fichier", command=ouvrir_fichiers)
bouton_ouvrir.grid(row=5, column=8, pady=10)

label5 = ttk.Label(frame2,
                   text="L'application prend en charge les DMOS scannés d'une seule page ainsi que les DMOS numériques de plusieurs pages.",
                   font=custom_font2,
                   foreground="grey", background="white")
label5.grid(row=6, column=8, pady=10)

# Crée un bouton pour valider la sélection
button3 = ttk.Button(frame2, text="Valider", command=valider, style="TButton")
button3.grid(row=19, column=16, pady=10, sticky='s')

button2 = ttk.Button(frame2, text="Retour", command=lambda: show_frame(frame1), style="TButton")
button2.grid(row=19, column=0, pady=10, sticky='s')

# Configurer la grille des frames pour redimensionner les widgets à l'intérieur
frame3.grid_rowconfigure(0, weight=1)
frame3.grid_rowconfigure(1, weight=1)
frame3.grid_rowconfigure(2, weight=1)
frame3.grid_rowconfigure(3, weight=1)
frame3.grid_rowconfigure(4, weight=1)
frame3.grid_rowconfigure(5, weight=1)
frame3.grid_rowconfigure(6, weight=1)
frame3.grid_rowconfigure(7, weight=1)
frame3.grid_rowconfigure(8, weight=1)
frame3.grid_rowconfigure(9, weight=1)
frame3.grid_rowconfigure(10, weight=1)
frame3.grid_rowconfigure(11, weight=1)
frame3.grid_rowconfigure(12, weight=1)
frame3.grid_rowconfigure(13, weight=1)
frame3.grid_rowconfigure(14, weight=1)
frame3.grid_rowconfigure(15, weight=1)
frame3.grid_rowconfigure(16, weight=1)
frame3.grid_rowconfigure(17, weight=1)
frame3.grid_rowconfigure(18, weight=1)
frame3.grid_rowconfigure(19, weight=1)
frame3.grid_columnconfigure(0, weight=1)


# Fonction pour animer le GIF
def update_frame(ind):
    frame = frames[ind]
    ind += 1
    if ind == frame_count:
        ind = 0
    label5.configure(image=frame)
    root.after(100, update_frame, ind)


# Charger le GIF
gif_path = "images/chargement3.gif"  # Remplacez par le chemin de votre GIF
im = Image.open(gif_path)

# Charger toutes les frames du GIF
frames = []
try:
    while True:
        frames.append(ImageTk.PhotoImage(im.copy()))
        im.seek(len(frames))  # Aller à la frame suivante
except EOFError:
    pass

frame_count = len(frames)

# Créer un widget Label pour afficher le GIF
label5 = tk.Label(frame3)
label5.grid(row=8, column=0, pady=10)

# Démarrer l'animation
frame3.after(0, update_frame, 0)

label8 = ttk.Label(frame3,
                   text="L'analyse de vos documents est en cours. L'application peut se figer pendant une minute. Merci de patienter.",
                   font=custom_font2, foreground="grey", background="white")
label8.grid(row=10, column=0, pady=10)

label7 = ttk.Label(frame3, text="Analyse en cours...", font=custom_font, background="white")
label7.grid(row=6, column=0, pady=10)


# Configurer la grille des frames pour redimensionner les widgets à l'intérieur
frame4.grid_rowconfigure(0, weight=1)
frame4.grid_rowconfigure(1, weight=1)
frame4.grid_rowconfigure(2, weight=1)
frame4.grid_rowconfigure(3, weight=1)
frame4.grid_rowconfigure(4, weight=1)
frame4.grid_rowconfigure(5, weight=1)
frame4.grid_rowconfigure(6, weight=1)
frame4.grid_rowconfigure(7, weight=1)
frame4.grid_rowconfigure(8, weight=1)
frame4.grid_rowconfigure(9, weight=1)
frame4.grid_rowconfigure(10, weight=1)
frame4.grid_rowconfigure(11, weight=1)
frame4.grid_rowconfigure(12, weight=1)
frame4.grid_rowconfigure(13, weight=1)
frame4.grid_rowconfigure(14, weight=1)
frame4.grid_rowconfigure(15, weight=1)
frame4.grid_rowconfigure(16, weight=1)
frame4.grid_rowconfigure(17, weight=1)
frame4.grid_rowconfigure(18, weight=1)
frame4.grid_rowconfigure(19, weight=1)
frame4.grid_columnconfigure(0, weight=1)
frame4.grid_columnconfigure(1, weight=1)
frame4.grid_columnconfigure(2, weight=1)
frame4.grid_columnconfigure(3, weight=1)
frame4.grid_columnconfigure(4, weight=1)
frame4.grid_columnconfigure(5, weight=1)
frame4.grid_columnconfigure(6, weight=1)
frame4.grid_columnconfigure(7, weight=1)
frame4.grid_columnconfigure(8, weight=1)
frame4.grid_columnconfigure(9, weight=1)
frame4.grid_columnconfigure(10, weight=1)
frame4.grid_columnconfigure(11, weight=1)
frame4.grid_columnconfigure(12, weight=1)
frame4.grid_columnconfigure(13, weight=1)
frame4.grid_columnconfigure(14, weight=1)
frame4.grid_columnconfigure(15, weight=1)
frame4.grid_columnconfigure(16, weight=1)


# Charger une image avec PIL
image_path4 = "images/logo.png"
image4 = Image.open(image_path4)
image4 = image4.resize((149, 74))
photo4 = ImageTk.PhotoImage(image4)

# Ajouter l'image à la première frame
image_label4 = tk.Label(frame4, image=photo4, bg="white")
image_label4.grid(row=0, column=8, pady=10, sticky='s')

image5 = Image.open("images/logoexcel.png")
image5 = image5.resize((20, 20))  # Redimensionner à 20x20 pixels
photo5 = ImageTk.PhotoImage(image5)

image6 = Image.open("images/logopdf.png")
image6 = image6.resize((20, 20))  # Redimensionner à 20x20 pixels
photo6 = ImageTk.PhotoImage(image6)

image7 = Image.open("images/logocrayon.png")
image7 = image7.resize((20, 20))  # Redimensionner à 20x20 pixels
photo7 = ImageTk.PhotoImage(image7)

image8 = Image.open("images/logomail.png")
image8 = image8.resize((20, 20))  # Redimensionner à 20x20 pixels
photo8 = ImageTk.PhotoImage(image8)

image9 = Image.open("images/logooeil.png")
image9 = image9.resize((20, 20))  # Redimensionner à 20x20 pixels
photo9 = ImageTk.PhotoImage(image9)

custom_font3 = Font(family="Calibri", size=20, weight="bold")


def tableauframe4():
    global Etat
    global all_text_info
    data = []
    all_entries = []  # Liste pour stocker toutes les entrées
    info = []
    print(all_text_info)

    for i in range(len(Etat)):
        print(Etat[i])
        listetemp = []
        listetemp.append(Etat[i])
        listetemp.append(all_text_info[i][0][0])
        listetemp.append(len(all_text_info[i]))
        data.append(listetemp)

    def onFrameConfigure(canvas):
        '''Reset the scroll region to encompass the inner frame'''
        canvas.configure(scrollregion=canvas.bbox("all"))

    # Créer une Frame pour organiser le tableau
    table_frame = ttk.Frame(frame4)
    table_frame.grid(row=1, column=8, pady=10, sticky='s')

    # Add a canvas in that frame
    canvas = tk.Canvas(table_frame, width=970, height=300)
    canvas.grid(row=0, column=0)

    frame_buttons = ttk.Frame(canvas)
    vsb = ttk.Scrollbar(table_frame, orient="vertical", command=canvas.yview)
    vsb.grid(row=0, column=1, sticky='ns')
    canvas.configure(yscrollcommand=vsb.set)
    canvas.create_window((0, 0), window=frame_buttons, anchor='nw')
    frame_buttons.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

    # Créer les en-têtes de colonnes
    headers = ["Etat", "Imputation", "Nbre DMOS", "Date Demande", "Date Réponse", "Commune", "Mail"]
    for idx, header in enumerate(headers):
        label = ttk.Label(frame_buttons, text=header, font=("Arial", 10, "bold"))
        label.grid(row=1, column=idx, padx=10, pady=5)

    # Ajouter les lignes avec les données et des boutons
    for row_idx, (etat, imputation, NbreDMOS) in enumerate(data, start=2):
        entries_list = []  # Liste pour stocker les ttk.Entry de chaque ligne
        if etat != "KO":
            info.append(etat)
            info.append(imputation)
            info.append(NbreDMOS)

        # Créer un label pour chaque colonne de données
        if etat == "OUI":
            etat = "✓"
            ttk.Label(frame_buttons, text=etat, font=custom_font3, foreground="green").grid(row=row_idx, column=0,
                                                                                           padx=10, pady=5)
        elif etat == "NON":
            etat = "X"
            ttk.Label(frame_buttons, text=etat, font=custom_font3, foreground="red").grid(row=row_idx, column=0, padx=10,
                                                                                         pady=5)
        else:
            ttk.Label(frame_buttons, text=etat, font=custom_font3, foreground="orange").grid(row=row_idx, column=0,
                                                                                            padx=10, pady=5)

        ttk.Label(frame_buttons, text=imputation).grid(row=row_idx, column=1, padx=10, pady=5)
        ttk.Label(frame_buttons, text=NbreDMOS).grid(row=row_idx, column=2, padx=10, pady=5)

        if etat != "KO":
            # Ajouter des champs Entry et les stocker dans la liste
            date_demande_entry = ttk.Entry(frame_buttons, width=10)
            date_demande_entry.grid(row=row_idx, column=3, padx=10, pady=5)
            entries_list.append(date_demande_entry)

            date_reponse_entry = ttk.Entry(frame_buttons, width=10)
            date_reponse_entry.grid(row=row_idx, column=4, padx=10, pady=5)
            entries_list.append(date_reponse_entry)

            commune_entry = ttk.Entry(frame_buttons, width=10)
            commune_entry.grid(row=row_idx, column=5, padx=10, pady=5)
            entries_list.append(commune_entry)

            mail_entry = ttk.Entry(frame_buttons, width=10)
            mail_entry.grid(row=row_idx, column=6, padx=10, pady=5)
            entries_list.append(mail_entry)

            all_entries.append(entries_list)

        if etat != "KO":
            action_button = ttk.Button(frame_buttons, text="", command=lambda idx=row_idx: bouton_action_excel(idx),
                                       image=photo5)
            action_button.grid(row=row_idx, column=7, padx=10, pady=5)

            action_button2 = ttk.Button(frame_buttons, text="", command=lambda idx=row_idx: bouton_action_pdf(idx),
                                        image=photo6)
            action_button2.grid(row=row_idx, column=8, padx=10, pady=5)

            if etat == "OUI" or etat == "✓":
                action_button3 = ttk.Button(frame_buttons, text="",
                                            command=lambda idx=row_idx: bouton_action_signature(idx), image=photo7)
                action_button3.grid(row=row_idx, column=9, padx=10, pady=5)

            action_button4 = ttk.Button(frame_buttons, text="", command=lambda idx=row_idx: bouton_action_mail(idx),
                                        image=photo8)
            action_button4.grid(row=row_idx, column=10, padx=10, pady=5)

            action_button5 = ttk.Button(frame_buttons, text="", command=lambda idx=row_idx: bouton_action_oeil(idx),
                                        image=photo9)
            action_button5.grid(row=row_idx, column=11, padx=10, pady=5)

    # Fonction pour récupérer les valeurs des champs Entry
    def get_entries_data():
        entries_data = []
        i = 0
        for entry_row in all_entries:
            entries_data2 = []
            entries_data2.append(str(info[i]))
            entries_data2.append(str(info[i+1]))
            entries_data2.append(str(info[i+2]))
            row_data = [entry.get() for entry in entry_row]  # Récupérer les valeurs de chaque ligne
            for k in range(len(row_data)):
                entries_data2.append(row_data[k])
            entries_data.append(entries_data2)
            i = i + 3
        print(entries_data)
        return entries_data

    # Fonction pour sauvegarder les données dans un fichier CSV
    def save_to_file():
        entries_data = get_entries_data()
        print(entries_data)
        with open('data/data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            # Écrire les données
            writer.writerows(entries_data)
        messagebox.showinfo("Sauvegarde", "Données sauvegardées avec succès !")

    # Bouton de sauvegarde
    save_button = ttk.Button(frame4, text="Sauvegarder", command=save_to_file)
    save_button.grid(row=17, column=8, pady=10, sticky='s')


# Fonctions des boutons pour chaque ligne
def bouton_action_excel(row_idx):
    global all_text_info
    global all_passes
    row_idx = row_idx - 2
    try:
        # Ouvrir une boîte de dialogue pour choisir le dossier
        dossier = filedialog.askdirectory()

        # Vérifier si un dossier a été sélectionné
        if dossier:
            # Spécifier le nom du fichier
            nom_fichier = 'DMOS_' + all_text_info[row_idx][0][0] + '.xlsx'

            # Créer le chemin complet
            chemin_complet = os.path.join(dossier, nom_fichier)

            # Créer un writer pour exporter plusieurs DataFrames
            with pd.ExcelWriter(chemin_complet, engine='xlsxwriter') as writer:
                # Boucler sur tous les ensembles de données dans all_text_info
                for index, current_text_info in enumerate(all_text_info[row_idx]):
                    current_passes = all_passes[row_idx][index]  # Récupérer les passes correspondantes

                    # Créer des données pour l'exportation
                    noms = ['Imputation', 'DMOS', 'QMOS de Référence', 'Procédé de Soudage', 'Diametre',
                            'Type de joint', 'Pression',
                            'Epaisseur', 'Norme', "Type d'enrobage", 'Courant', 'Soudeur', 'Meulage',
                            'Etuvage des électrodes',
                            'Chanfrein d\'origine', 'Oxycoupage',
                            'Séchage/dégourdissage', 'Température de préchauffage', 'Température entre passes', 'Type',
                            'Longueur']

                    valeurs = [
                        current_text_info[0],  # Imputation
                        current_text_info[1],  # DMOS
                        current_text_info[2],  # QMOS de Référence
                        current_text_info[5],  # Procédé de Soudage
                        ' ',
                        current_text_info[8],  # Type de joint
                        current_text_info[11],  # Pression
                        ' ',
                        ' ',
                        current_text_info[14],
                        current_text_info[15],  # Courant
                        current_text_info[16],
                        current_text_info[17],  # Meulage
                        current_text_info[18],  # Etuvage des électrodes
                        current_text_info[19],  # Chanfrein d'origine
                        current_text_info[20],  # Oxycoupage
                        current_text_info[21],  # Séchage/dégourdissage
                        current_text_info[22],  # Température de préchauffage
                        current_text_info[23],  # Température entre passes
                        current_text_info[24],  # Type
                        current_text_info[25]  # Longueur
                    ]

                    # Ajouter les détails de l'élément 1
                    element1 = [
                        ' ', ' ', ' ', ' ',
                        current_text_info[6],  # Diamètre extérieur 1
                        ' ', ' ', current_text_info[9],  # Épaisseur 1
                        current_text_info[12],  # Norme 1
                        ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                    ]

                    # Ajouter les détails de l'élément 2
                    element2 = [
                        ' ', ' ', ' ', ' ',
                        current_text_info[7],  # Diamètre extérieur 2
                        ' ', ' ', current_text_info[10],  # Épaisseur 2
                        current_text_info[13],  # Norme 2
                        ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                    ]

                    # Créer un DataFrame pandas à partir des données
                    data = {
                        'Nom': noms,
                        'Valeur': valeurs,
                        'Elément 1': element1,
                        'Elément 2': element2
                    }

                    df = pd.DataFrame(data)

                    # Créer un deuxième DataFrame pour les passes
                    passes_data = pd.DataFrame(current_passes, columns=[
                        'Passe N°', 'Diamètre', 'Réf.', 'Polarité', 'Designation', 'Position',
                        'Vitesse', 'Tension', 'Intensité', 'Energie'
                    ])

                    # Exporter le premier DataFrame pour ce jeu de données
                    sheet_name_info = f'Informations Générales {index + 1}'
                    df.to_excel(writer, sheet_name=sheet_name_info, index=False)

                    # Exporter le second DataFrame pour ce jeu de données
                    sheet_name_passes = f'Passes {index + 1}'
                    passes_data.to_excel(writer, sheet_name=sheet_name_passes, index=False)

            print(f"Données exportées avec succès vers '{chemin_complet}'")
            messagebox.showinfo("Succès", f"Données exportées avec succès vers '{chemin_complet}'")
        else:
            print("Aucun dossier sélectionné. Opération annulée.")
            messagebox.showwarning("Annulé", "Aucun dossier sélectionné. Opération annulée.")
    except Exception as e:
        # Afficher un message d'erreur en cas de problème
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")
    print(f"Action 1 pour la ligne {row_idx}")


def bouton_action_pdf(row_idx):
    global MsgValides
    global MsgErreurs
    global all_text_info
    row_idx = row_idx - 2
    try:
        # Ouvrir une boîte de dialogue pour choisir le dossier
        dossier = filedialog.askdirectory()

        if dossier:
            # Définir le chemin complet du fichier PDF
            chemin_complet = os.path.join(dossier, "Rapport_DMOS_" + all_text_info[row_idx][0][0] + ".pdf")

            # Créer un document PDF avec une taille de page A4
            pdf = SimpleDocTemplate(chemin_complet, pagesize=A4)

            # Créer un style de texte
            styles = getSampleStyleSheet()
            style_bold = styles['Heading2']

            # Styles personnalisés
            style_valide = ParagraphStyle(
                'Valide',
                parent=styles['Normal'],
                textColor=colors.green
            )

            style_erreur = ParagraphStyle(
                'Erreur',
                parent=styles['Normal'],
                textColor=colors.red
            )

            # Styles personnalisés
            style_valide2 = ParagraphStyle(
                'Valide',
                parent=styles['Heading2'],
                textColor=colors.green
            )

            style_erreur2 = ParagraphStyle(
                'Erreur',
                parent=styles['Heading2'],
                textColor=colors.red
            )

            # Contenu du PDF
            elements = []

            # Ajouter une image
            chemin_image = "images/logo.png"  # Remplace ceci par le chemin réel de ton image
            if os.path.exists(chemin_image):
                img = mage(chemin_image, width=5 * cm, height=2.5 * cm)  # Ajuste la taille selon tes besoins
                elements.append(img)
                elements.append(Spacer(1, 1 * cm))

            # Ajouter un titre principal
            titre = Paragraph("Rapport d'analyse de ValiDMOS", styles['Title'])
            elements.append(titre)
            elements.append(Spacer(1, 0.5 * cm))

            # Ajouter une sous-section "Imputation"
            sous_titre = Paragraph("Imputation : " + all_text_info[row_idx][0][0], styles['Title'])
            elements.append(sous_titre)
            elements.append(Spacer(1, 0.5 * cm))

            if len(MsgErreurs[row_idx]) > 0:
                titre_refuse = Paragraph("[REFUSÉ]", style_erreur2)
                elements.append(titre_refuse)
                elements.append(Spacer(1, 0.5 * cm))
            else:
                titre_valide0 = Paragraph("[VALIDÉ]", style_valide2)
                elements.append(titre_valide0)
                elements.append(Spacer(1, 0.5 * cm))

            # Titre de la section "Validations"
            titre_valide = Paragraph("Messages Validés :", style_bold)
            elements.append(titre_valide)
            elements.append(Spacer(1, 0.5 * cm))

            # Ajouter chaque message validé en vert
            for msg in MsgValides[row_idx]:
                paragraphe = Paragraph(f"- {msg}", style_valide)
                elements.append(paragraphe)
                elements.append(Spacer(1, 0.2 * cm))

            elements.append(Spacer(1, 1 * cm))

            # Titre de la section "Erreurs"
            titre_erreur = Paragraph("Messages d'Erreur :", style_bold)
            elements.append(titre_erreur)
            elements.append(Spacer(1, 0.5 * cm))

            # Ajouter chaque message d'erreur en rouge
            for msg in MsgErreurs[row_idx]:
                paragraphe = Paragraph(f"- {msg}", style_erreur)
                elements.append(paragraphe)
                elements.append(Spacer(1, 0.2 * cm))

            # Générer le PDF
            pdf.build(elements)
            print(f"Données exportées avec succès vers '{chemin_complet}'")
            messagebox.showinfo("Succès", f"Données exportées avec succès vers '{chemin_complet}'")
        else:
            print("Aucun dossier sélectionné. Opération annulée.")
            messagebox.showwarning("Annulé", "Aucun dossier sélectionné. Opération annulée.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
    print(f"Action 2 pour la ligne {row_idx}")


def bouton_action_signature(row_idx):
    global chemins_fichiers
    global all_text_info
    row_idx = row_idx - 2
    image_path = "signature/Signature.png"
    x = 450
    y = 540
    zoom = 2
    # Ouvrir une boîte de dialogue pour choisir le dossier de destination
    root = tk.Tk()
    root.withdraw()  # Cacher la fenêtre principale Tkinter
    destination_folder = filedialog.askdirectory()  # Ouvre une boîte de dialogue pour choisir le dossier

    if not destination_folder:
        print("Aucun dossier sélectionné.")
        messagebox.showwarning("Annulé", "Aucun dossier sélectionné. Opération annulée.")
        return

    output_pdf = os.path.join(destination_folder, "DMOS_" + all_text_info[row_idx][0][0] + "_signé.pdf")

    # Ouvrir le fichier PDF existant
    doc = fitz.open(chemins_fichiers[row_idx])

    # Définir la taille et la position de l'image
    image_rect = fitz.Rect(x, y, x + zoom * 50, y + zoom * 50)

    # Parcourir toutes les pages du PDF
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        rect = page.rect  # Récupérer la taille de la page pour vérifier son orientation

        # Insérer l'image uniquement pour les pages en orientation portrait
        if rect.height > rect.width:
            page.insert_image(image_rect, filename=image_path)
        else:
            print(f"Page {page_num + 1} est en paysage, image non insérée.")

    # Enregistrer le fichier PDF modifié
    doc.save(output_pdf)
    doc.close()

    print(f"PDF signé enregistré à : {output_pdf}")
    messagebox.showinfo("Succès", f"Données exportées avec succès vers '{output_pdf}'")
    print(f"Action 3 pour la ligne {row_idx}")


def bouton_action_mail(row_idx):
    global all_text_info
    global MsgErreurs
    keywordmail = '@'
    row_idx = row_idx - 2
    if keywordmail in all_text_info[row_idx][0][-1]:
        recipient = all_text_info[row_idx][0][-1]
    else:
        recipient = " "
    if len(MsgErreurs[row_idx]) > 0:
        subject = "[REFUSÉ] Données du DMOS"
        body = """Bonjour,

    L'application ValiDMOS a bien scanné votre DMOS.

    Après analyse, le DMOS a été refusé.

    Vous trouverez ci-joint les données du DMOS sous la forme d'un fichier Excel.

    Merci de me contacter pour plus d'informations.

    Cordialement,
            """
    else:
        subject = "[VALIDÉ] Données du DMOS"
        body = """Bonjour,

    L'application ValiDMOS a bien scanné votre DMOS.

    Après analyse, le DMOS a été validé.

    Vous trouverez ci-joint les données du DMOS sous la forme d'un fichier Excel.

    Merci de me contacter pour plus d'informations.

    Cordialement,
            """

    # Encodage des éléments du mailto
    subject_encoded = urllib.parse.quote(subject)
    body_encoded = urllib.parse.quote(body)
    mailto_url = f"mailto:{recipient}?subject={subject_encoded}&body={body_encoded}"

    try:
        if sys.platform == "win32":
            os.startfile(mailto_url)
        elif sys.platform == "darwin":
            os.system(f"open '{mailto_url}'")
        else:
            os.system(f"xdg-open '{mailto_url}'")
    except Exception as e:
        print(f"Erreur lors de l'ouverture de l'application de messagerie: {e}")
    print(f"Action 4 pour la ligne {row_idx}")


def bouton_action_oeil(row_idx):
    global chemins_fichiers
    global all_text_info
    global all_passes
    global frame5
    global frame4
    global canvas
    global scrollbar
    global inner_frame
    current_index = 0
    trees = []

    row_idx = row_idx - 2  # Ajuster pour le bon index de ligne

    # Chemin vers votre fichier PDF
    pdf_path = chemins_fichiers[row_idx]

    # Convertir le chemin du fichier en URL
    pdf_url = 'file://' + os.path.abspath(pdf_path)

    # Ouvrir le fichier PDF dans le navigateur
    webbrowser.open(pdf_url)

    show_frame(frame5)

    # Clear the inner frame if already exists
    for widget in inner_frame.winfo_children():
        widget.destroy()

    n = 0
    for i in range(len(all_text_info[row_idx])):
        # Création des tableaux
        # Premier tableau
        tree1 = ttk.Treeview(inner_frame, columns=("col1"), show="headings", height=2)
        tree1.heading("col1", text="DESCRIPTIF DE MODE OPERATOIRE DE SOUDAGE")
        tree1.column("col1", width=400, anchor=tk.W)
        tree1.pack(fill=tk.BOTH, padx=5, pady=5)
        trees.append(tree1)

        # Deuxième tableau
        tree2 = ttk.Treeview(inner_frame, columns=("col1", "col2"), show="headings", height=2)
        tree2.heading("col1", text="Elément 1")
        tree2.heading("col2", text="Elément 2")
        tree2.column("col1", width=200, anchor=tk.W)
        tree2.column("col2", width=200, anchor=tk.W)
        tree2.pack(fill=tk.BOTH, padx=5, pady=5)
        trees.append(tree2)

        # Troisième tableau (Passe N°)
        tree3 = ttk.Treeview(inner_frame,
                             columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8", "col9", "col10"),
                             show="headings", height=2)
        tree3.heading("col1", text="Passe N°")
        tree3.heading("col2", text="Diamètre")
        tree3.heading("col3", text="Réf.")
        tree3.heading("col4", text="Polarité")
        tree3.heading("col5", text="Designation")
        tree3.heading("col6", text="Position")
        tree3.heading("col7", text="Vitesse")
        tree3.heading("col8", text="Tension")
        tree3.heading("col9", text="Intensité")
        tree3.heading("col10", text="Energie")
        for i in range(1, 11):
            tree3.column(f"col{i}", width=100, anchor=tk.W)
        tree3.pack(fill=tk.BOTH, padx=5, pady=5)
        trees.append(tree3)

        # Quatrième tableau
        tree4 = ttk.Treeview(inner_frame, columns=("col1"), show="headings", height=2)
        tree4.heading("col1", text="Mode de préparation, Conditions thermiques et Moyen d'accostage")
        tree4.column("col1", width=400, anchor=tk.W)
        tree4.pack(fill=tk.BOTH, padx=5, pady=5)
        trees.append(tree4)

        tableau1 = [
            ("Imputation/EOTP : " + all_text_info[row_idx][current_index][0],),
            ("DMOS N°" + all_text_info[row_idx][current_index][1],),
            ("QMOS de Référence : " + all_text_info[row_idx][current_index][2],),
            ("Procédé de Soudage : " + all_text_info[row_idx][current_index][5],),
            ("Type de joint : " + all_text_info[row_idx][current_index][8],),
            ("Pression : " + all_text_info[row_idx][current_index][11],),
            ("Type d'enrobage : " + all_text_info[row_idx][current_index][14],),
            ("Courant : " + all_text_info[row_idx][current_index][15],),
            ("Nombre de soudeur : " + all_text_info[row_idx][current_index][16],),
        ]
        for row in tableau1:
            trees[n].insert("", tk.END, values=row)
        n = n + 1

        tableau2 = [
            ("Nuance 1 : " + all_text_info[row_idx][current_index][3], "Nuance 2 : " + all_text_info[row_idx][current_index][4]),
            ("D. extérieur 1 : " + all_text_info[row_idx][current_index][6], "D. extérieur 2 : " + all_text_info[row_idx][current_index][7]),
            ("Epaisseur 1 : " + all_text_info[row_idx][current_index][9], "Epaisseur 2 : " + all_text_info[row_idx][current_index][10]),
            ("Norme 1 : " + all_text_info[row_idx][current_index][12], "Norme 2 : " + all_text_info[row_idx][current_index][13]),
        ]
        for row in tableau2:
            trees[n].insert("", tk.END, values=row)
        n = n + 1

        tableau3 = all_passes[row_idx][current_index]
        for row in tableau3:
            trees[n].insert("", tk.END, values=row)
        n = n + 1

        tableau4 = [
            ("Meulage : " + all_text_info[row_idx][current_index][17],),
            ("Etuvage des électrodes : " + all_text_info[row_idx][current_index][18],),
            ("Chanfrein d'origine : " + all_text_info[row_idx][current_index][19],),
            ("Oxycoupage : " + all_text_info[row_idx][current_index][20],),
            ("Séchage/dégourdissage : " + all_text_info[row_idx][current_index][21],),
            ("Température de préchauffage : " + all_text_info[row_idx][current_index][22],),
            ("Température entre passes : " + all_text_info[row_idx][current_index][23],),
            ("Type : " + all_text_info[row_idx][current_index][24],),
            ("Longueur : " + all_text_info[row_idx][current_index][25],),
        ]
        for row in tableau4:
            trees[n].insert("", tk.END, values=row)
        n = n + 1
        current_index += 1

    # Mise à jour de la taille du canvas pour s'adapter à l'inner_frame
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    print(f"Action 5 pour la ligne {row_idx}")


# Créer un cadre principal pour les boutons
btn_frame = tk.Frame(frame5, bg="white")
btn_frame.pack(side="bottom", fill="x")

# Créer un cadre pour le bouton à droite
right_frame = tk.Frame(btn_frame, bg="white")
right_frame.pack(side="right", padx=5)

# Créer le bouton pour le côté droit
vali_button = ttk.Button(right_frame, text="Retour", command=lambda: show_frame(frame4), style="TButton")
vali_button.pack(side="right", padx=5)

# Canvas et scrollbar
canvas = tk.Canvas(frame5)
scrollbar = ttk.Scrollbar(frame5, orient="vertical", command=canvas.yview)
inner_frame = tk.Frame(canvas)

inner_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=inner_frame, anchor="nw")
canvas.config(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


# Réinitialisation des variables pour scanner de nouveaux documents
def newscan():
    global all_text_info
    global all_passes
    global Liste_Excel
    global MsgValide
    global MsgErreur
    global MsgValides
    global MsgErreurs
    global Etat
    MsgValide = []
    MsgErreur = []
    Liste_Excel = []
    all_text_info = []
    all_passes = []
    all_text_info = []
    all_passes = []
    Liste_Excel = []
    Etat = []
    MsgValides = []
    MsgErreurs = []
    show_frame(frame2)


button6 = ttk.Button(frame4, text="Nouveau Scan", command=newscan, style="TButton")
button6.grid(row=18, column=8, pady=10, sticky='s')


# Configurer la grille des frames pour redimensionner les widgets à l'intérieur
frame6.grid_rowconfigure(0, weight=1)
frame6.grid_rowconfigure(1, weight=1)
frame6.grid_rowconfigure(2, weight=1)
frame6.grid_rowconfigure(3, weight=1)
frame6.grid_rowconfigure(4, weight=1)
frame6.grid_rowconfigure(5, weight=1)
frame6.grid_rowconfigure(6, weight=1)
frame6.grid_rowconfigure(7, weight=1)
frame6.grid_rowconfigure(8, weight=1)
frame6.grid_rowconfigure(9, weight=1)
frame6.grid_rowconfigure(10, weight=1)
frame6.grid_rowconfigure(11, weight=1)
frame6.grid_rowconfigure(12, weight=1)
frame6.grid_rowconfigure(13, weight=1)
frame6.grid_rowconfigure(14, weight=1)
frame6.grid_rowconfigure(15, weight=1)
frame6.grid_rowconfigure(16, weight=1)
frame6.grid_rowconfigure(17, weight=1)
frame6.grid_rowconfigure(18, weight=1)
frame6.grid_rowconfigure(19, weight=1)
frame6.grid_columnconfigure(0, weight=1)
frame6.grid_columnconfigure(1, weight=1)
frame6.grid_columnconfigure(2, weight=1)
frame6.grid_columnconfigure(3, weight=1)
frame6.grid_columnconfigure(4, weight=1)
frame6.grid_columnconfigure(5, weight=1)
frame6.grid_columnconfigure(6, weight=1)
frame6.grid_columnconfigure(7, weight=1)
frame6.grid_columnconfigure(8, weight=1)
frame6.grid_columnconfigure(9, weight=1)
frame6.grid_columnconfigure(10, weight=1)
frame6.grid_columnconfigure(11, weight=1)
frame6.grid_columnconfigure(12, weight=1)
frame6.grid_columnconfigure(13, weight=1)
frame6.grid_columnconfigure(14, weight=1)
frame6.grid_columnconfigure(15, weight=1)
frame6.grid_columnconfigure(16, weight=1)

# Charger une image avec PIL
image_path66 = "images/logo.png"
image66 = Image.open(image_path66)
image66 = image66.resize((149, 74))
photo66 = ImageTk.PhotoImage(image66)

# Ajouter l'image à la première frame
image_label66 = tk.Label(frame6, image=photo66, bg="white")
image_label66.grid(row=0, column=8, pady=10, sticky='s')

# Ajouter un label et un bouton
label62 = ttk.Label(frame6, text="HISTORIQUE DE SCAN", font=custom_font,
                  background="white")
label62.grid(row=1, column=8, pady=10)


def afficher_tableau_stat():
    show_frame(frame6)
    # Création d'une nouvelle frame pour le tableau
    tableau_frame = ttk.Frame(frame6)
    tableau_frame.grid(row=2, column=8, pady=10, sticky='n')

    # Création du Treeview (tableau) avec les colonnes nécessaires
    columns = ("N°", "Etat", "Imputation", "Nbre DMOS", "Date Demande", "Date Réponse", "Commune", "Mail")

    tree = ttk.Treeview(tableau_frame, columns=columns, show="headings")

    # Définir les titres des colonnes et leur largeur
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")  # Ajuster la largeur à votre besoin

    # Ajouter une barre de défilement verticale
    scrollbar = ttk.Scrollbar(tableau_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tree.pack(fill="both", expand=True)

    # Lire les données depuis le fichier CSV et les insérer dans le tableau
    try:
        with open('data/data.csv', mode='r') as file:
            reader = csv.reader(file)
            for idx, row in enumerate(reader, start=1):  # Numérotation commence à 1
                tree.insert("", "end", values=(idx, *row))  # Ajouter la numérotation dans la première colonne
    except FileNotFoundError:
        print("Le fichier data.csv n'existe pas encore.")


button_stat = ttk.Button(frame1, text="Historique de Scan", command=afficher_tableau_stat, style="TButton")
button_stat.grid(row=19, column=0, pady=10, sticky='n')

button_stat_retour = ttk.Button(frame6, text="Retour", command=lambda: show_frame(frame1), style="TButton")
button_stat_retour.grid(row=19, column=8, pady=10, sticky='n')


def quitter():
    print("Fermeture de la fenêtre")
    root.destroy()
    sys.exit()


button7 = ttk.Button(frame4, text="Quitter", command=quitter, style="TButton")
button7.grid(row=19, column=8, pady=10, sticky='s')


def on_closing():
    print("Fermeture de la fenêtre")
    root.destroy()  # Ferme la fenêtre principale
    sys.exit()  # Termine le programme Python


# Remplacement de la méthode de fermeture par défaut
root.protocol("WM_DELETE_WINDOW", on_closing)

# Afficher la première frame au lancement
show_frame(frame1)

# Démarrer la boucle principale
root.mainloop()
