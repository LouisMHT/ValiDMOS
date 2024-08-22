from PIL import Image, ImageTk
from tkinter import filedialog, messagebox
import io
import re
import fitz  # PyMuPDF
import cv2
import numpy as np
import easyocr
import os


all_text_info = []
all_passes = []


def scan(chemin_fichier):
    global all_text_info
    global all_passes
    all_text = []
    all_extracted_text = []
    extratext = []
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
        messagebox.showerror("Erreur", f"Une erreur est survenue : {e}")
        pass

    data = all_extracted_text

    # Initialiser les variables globales
    global Imputation, QMOS, ProcedeSoudage, Diametre, TypeJoint, Pression, Epaisseur, Norme, Courant, Passes, Nuance, DMOS
    global Meulage, Etuvage, Chanfrein, Oxycoupage, Sechage, Prechauffage, TemperatureEntrePasses, Type, Longueur, Mail

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

    # Liste des mots-clés à rechercher pour supprimer les chaines de caractère inutile
    keywords_to_remove = ['Materiau', 'Intensité', 'Elément', 'Fabricant', 'Grou', 'Schéma', 'Direction', 'Moyen', 'Moven',
                          'Paramètre', 'Passe', '415', '425', 'enrobage', 'DESCRIPTIF', 'Adresse',
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
        (['Nuance'], 'Nuance', 0),
        (['DMOS'], 'DMOS', 8),
        (['Autre'], 'Mail', 0),
    ]

    for keywords, attribute_name, slice_index in modifications:
        cleaned_data_list = [modify_string(data, keywords, attribute_name, slice_index) for data in cleaned_data_list]

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

    Diametre1 = Diametre[:(round(len(Diametre)/2))]
    Diametre1 = Diametre1.replace(" ", "")

    Diametre2 = Diametre[(round(len(Diametre)/2)):]
    Diametre2 = Diametre2.replace(" ", "")

    Epaisseur1 = Epaisseur[:(round(len(Epaisseur)/2))]
    Epaisseur1 = Epaisseur1.replace(" ", "")

    Epaisseur2 = Epaisseur[(round(len(Epaisseur)/2)):]
    Epaisseur2 = Epaisseur2.replace(" ", "")

    keywordannee = "Année"
    if keywordannee in Norme:
        Norme1 = Norme[:18]
        Norme2 = Norme[19:]
    else:
        Norme1 = Norme[:(round(len(Norme)/2))]
        Norme2 = Norme[(round(len(Norme)/2)):]

    Chaine = Passes.split()

    num = len(Chaine)/14
    num = int(num)

    def diviser_liste_en_n_groupes(liste, nombre_de_groupes):
        taille_du_groupe, reste = divmod(len(liste), nombre_de_groupes)
        return [liste[i * taille_du_groupe + min(i, reste):(i + 1) * taille_du_groupe + min(i + 1, reste)] for i in
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
    all_text.append(Courant)
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

    # Spécifier les pourcentages pour chaque partie (assurez-vous que la somme égale 100)
    percentages = [28.2, 6.3, 1.5, 21, 43]

    # Vérifier que la somme des pourcentages est égale à 100
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

    # Sélectionner trois parties (par exemple, la première, la troisième et la cinquième)
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
    k=0
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
                break  # Sortir de la boucle une fois que le tiret est trouvé

        # Créer une liste qui va de la position 2 jusqu'à la position du tiret
        liste = list(range(2, position))

        rowbis = []
        # Ajouter les éléments correspondants dans row3
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
        # Ajouter les éléments correspondants dans row3
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

    all_text_info.append(all_text)
    all_passes.append(extratext)

    os.remove('page.png')
    os.remove('plus_grand_tableau.png')
    os.remove('assembled_image.png')


scan('DMOS TEST.pdf')

print(all_text_info)
print(all_passes)
