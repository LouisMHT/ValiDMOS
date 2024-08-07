import easyocr

reader = easyocr.Reader(['fr'], model_storage_directory='C:/Users/louis/.EasyOCR/model', download_enabled=False)  # Télécharge les modèles nécessaires pour le français
print(reader.model_storage_directory)  # Affiche le répertoire où les modèles sont stockés
