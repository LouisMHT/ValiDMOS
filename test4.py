import pdfplumber
import re


# Liste pour stocker tous les tableaux
all_tables_2 = []
all_tables_origin_2 = []


def scan_num(chemin_fichier):
    # Listes et variables du programme
    pdf_file = chemin_fichier
    all_tables = []
    all_tables_origin = []
    global all_tables_2
    global all_tables_origin_2

    # Listes de mots-clés pour lesquels ajouter un espace après le mot-clé
    keywords_to_add_space_after = ["DESCRIPTIF", "OPERATOIRE", "DMOS", "Matériau", "Adresse", "EOTP", ":",
                                   "chantier", "QMOS", "Procédé", "Nature", "Type", "Epaisseur", "Paramètre",
                                   "Parametre", "1.1", "1.2", "Température", "Temperature", "Pression", "maximale", "enrobage",
                                   "Oui", "Non", "Meulage", "Etuvage", "Chanfrein", "origine", "accostage",
                                   "dispositif", "Oxycoupage", "mm", "cm"]

    # Listes de mots-clés pour lesquels ajouter un espace avant et après
    keywords_to_add_double_space = ["MODE", "Elément", "Référence", "soudage", "extérieur", "joint", "courant",
                                    "service", "passes", "électrodes"]

    # Listes de mots-clés pour lesquels ajouter un espace avant
    keywords_to_add_space_before = ["SOUDAGE", "chantier", "soudeur", "Direction"]

    # Listes de mots-clés pour séparer
    keywords_to_split = ["Adresse", "DMOS", "Matériau", "Nuance", "Ø", "Etuvage", "Oxycoupage", "Coordonnateur",
                         "Direction"]

    # Listes de mots-clés à garder
    keywords_to_keep = ["Imputation", "EOTP", "DMOS", "QMOS", "1.1", "Procédé", "extérieur", "joint",
                        "Epaisseur", "Pression", "Paramètre", "Meulage", "Etuvage", "Chanfrein", "Oxycoupage",
                        "Séchage", "Sechage", "préchauffage", "prechauffage", "entre", "Température", "Temperature",
                        "Type", "dispositif", "Norme", "@"]

    # Créer un motif d'expression régulière pour séparer aux mots-clés
    pattern = r'({})'.format('|'.join(keywords_to_split))

    # Ouvrir le PDF avec pdfplumber
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            # Extraction des caractères individuels avec les stratégies "text"
            table_settings = {
                "vertical_strategy": "text",
                "horizontal_strategy": "text"
            }

            tables = page.extract_tables(table_settings)

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
                    chaines_filtrees = [chaine for chaine in final_table if any(mot_cle in chaine for mot_cle in
                                                                                keywords_to_keep)]

                # Triage des passes
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
        table[10] = table[10][74:]
        table[10] = table[10][:2]
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

    # Division des chaines de caractère par les espaces
    for table in all_tables:
        final_table_2 = []
        for row in table:
            # Diviser la chaîne par des espaces
            sections = row.split()
            final_table_2.extend(sections)
        del final_table_2[-2]
        all_tables_2.append(final_table_2)

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
                    break  # Sortir de la boucle une fois que le tiret est trouvé
                elif row2[0][i] == 'PA':
                    position2 = i
                    break  # Sortir de la boucle une fois que le tiret est trouvé
                elif row2[0][i] == 'PC':
                    position2 = i
                    break  # Sortir de la boucle une fois que le tiret est trouvé
                elif row2[0][i] == 'PH':
                    position2 = i
                    break  # Sortir de la boucle une fois que le tiret est trouvé

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
        all_tables_origin_2.append(final_table_origin_3)


scan_num("DMOS2.pdf")

print(all_tables_2)
print(all_tables_origin_2)
