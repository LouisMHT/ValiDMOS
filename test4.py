import fitz  # PyMuPDF


def is_scanned_pdf(file_path):
    # Ouvrir le document PDF
    document = fitz.open(file_path)

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text()

        # Si du texte est trouvé sur la page, ce n'est probablement pas un PDF scanné
        if text.strip():
            return False

    # Si aucune page n'a de texte, c'est probablement un PDF scanné
    return True


# Chemin vers votre fichier PDF
file_path = 'DMOS2.pdf'

if is_scanned_pdf(file_path):
    print("Le fichier PDF est une version scannée.")
else:
    print("Le fichier PDF est une version native.")
