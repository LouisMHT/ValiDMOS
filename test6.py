import tkinter as tk
import os
import sys
import urllib.parse

def open_email():
    recipient = "destinataire@example.com"
    subject = "Sujet de l'email"
    body = """Bonjour,

Ceci est un message personnalisé. 

Merci de me contacter pour plus d'informations.

Cordialement,
Votre nom"""

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

# Configuration de l'interface Tkinter
root = tk.Tk()
root.title("Redirection Email")

# Bouton pour envoyer l'email
email_button = tk.Button(root, text="Envoyer un email", command=open_email)
email_button.pack(pady=20)

# Boucle principale Tkinter
root.mainloop()
