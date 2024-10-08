import os

translations = {
    'fr': {
        'title': "Indesign Traduction",
        'browse_dir': "Parcourir Dossier",
        'langs_selected': "Langue(s) sélectionnée(s) :",
        'notify_users': "Prévenir les utilisateurs : (Bientôt disponible)",
        'api_key': "Clé API DeepL :",
        'glossary': "Glossaire : ",
        'translate': "Traduire",
        'stop': "Arrêter",
        'progress': "Traduction : {percentage}%",
        'error': "Erreur",
        'warning': "Avertissement",
        'info': "Information",
        'select_all': "Tout sélectionner",
        'deselect_all': "Tout désélectionner",
        'confirm': "Confirmer",
        'dir_path': "Chemin des répertoires :",
        'notify_yes': "Oui",
        'notify_no': "Non",
        'save_key': "Sauvegarder la clé",
        'popup_title': "Sélection des fichiers",
        'file_explorer_title': "Explorateur de fichiers",
        'english': "Anglais",
        'german': "Allemand",
        'spanish': "Espagnol",
        'french': "Français",
        'source_lang': "Langue d'origine :",
        'languages': ["FR", "EN", "DE", "ES"],
        'error_extraction': "Erreur lors de l'extraction du fichier {file}: {error}",
        'file_not_found': "Le fichier spécifié {file} est introuvable.",
        'permission_error': "Vous n'avez pas les droits nécessaires pour accéder au fichier {file}.",
        'error_parsing': "Erreur lors du parsing du fichier {file}: {error}",
        'error_writing': "Erreur lors de l'écriture du fichier {file}: {error}",
        'error_authorization': "La clé API est invalide ou n'a pas les permissions nécessaires.",
        'error_connection': "Une erreur s'est produite lors de la vérification de la clé API : {error}",
        'warning_no_files': "Veuillez sélectionner au moins un fichier à traduire.",
        'warning_no_lang': "Veuillez sélectionner au moins une langue.",
        'warning_no_stories_dir': "Le répertoire 'Stories' n'existe pas pour le fichier {file}.",
        'warning_no_xml': "Aucun fichier XML trouvé dans les répertoires 'Stories'.",
        'file_already_translated': "Le texte est déjà en {language}, {text} ne sera pas traduit.",
        'text_translated': "Texte traduit: {text}",
        'loading_api_key': "Chargement de la clé API enregistrée.",
        'no_saved_api_key': "Aucune clé API enregistrée trouvée.",
        'saving_api_key': "La clé API a été sauvegardée.",
        'invalid_api_key': "Veuillez saisir une clé API valide avant de sauvegarder.",
        'language_mismatch': "Le fichier {file} est en {detected} au lieu de {expected}.",
        'same_language': "Le fichier {file} est déjà en {language}.",
        'confirm_unzip': "Le répertoire 'Stories' est manquant. Voulez-vous dézipper le fichier IDML?",
        'same_language_warning': "Vous ne pouvez pas traduire dans une langue similaire à la langue d'origine.",
        'browse_glossary': "Parcourir Glossaire",
        'glossary_loaded': "Le glossaire a été chargé avec succès.",
        'error_loading_glossary': "Erreur lors du chargement du glossaire : {error}",
        'error_creating_glossary': "Erreur lors de la création du glossaire : {error}",
    },
    'en': {
        'title': "Indesign Translation",
        'browse_dir': "Browse Directory",
        'langs_selected': "Selected Language(s) :",
        'notify_users': "Notify Users : (Coming Soon)",
        'api_key': "DeepL API Key :",
        'glossary': "Glossary :",
        'translate': "Translate",
        'stop': "Stop",
        'progress': "Translation : {percentage}%",
        'error': "Error",
        'warning': "Warning",
        'info': "Information",
        'select_all': "Select All",
        'deselect_all': "Deselect All",
        'confirm': "Confirm",
        'dir_path': "Directory Path :",
        'notify_yes': "Yes",
        'notify_no': "No",
        'save_key': "Save Key",
        'popup_title': "File Selection",
        'file_explorer_title': "File Explorer",
        'english': "English",
        'german': "German",
        'spanish': "Spanish",
        'french': "French",
        'source_lang': "Source Language :",
        'languages': ["FR", "EN", "DE", "ES"],
        'error_extraction': "Error extracting file {file}: {error}",
        'file_not_found': "Specified file {file} not found.",
        'permission_error': "You do not have the necessary permissions to access file {file}.",
        'error_parsing': "Error parsing file {file}: {error}",
        'error_writing': "Error writing file {file}: {error}",
        'error_authorization': "The API key is invalid or lacks necessary permissions.",
        'error_connection': "An error occurred while verifying the API key: {error}",
        'warning_no_files': "Please select at least one file to translate.",
        'warning_no_lang': "Please select at least one language.",
        'warning_no_stories_dir': "The 'Stories' directory does not exist for file {file}.",
        'warning_no_xml': "No XML files found in the 'Stories' directories.",
        'file_already_translated': "Text is already in {language}, {text} will not be translated.",
        'text_translated': "Translated text: {text}",
        'loading_api_key': "Loading saved API key.",
        'no_saved_api_key': "No saved API key found.",
        'saving_api_key': "The API key has been saved.",
        'invalid_api_key': "Please enter a valid API key before saving.",
        'language_mismatch': "File {file} is in {detected} instead of {expected}.",
        'same_language': "File {file} is already in {language}.",
        'confirm_unzip': "The 'Stories' directory is missing. Would you like to unzip the IDML file?",
        'same_language_warning': "You cannot translate to a language similar to the source language.",
        'browse_glossary': "Browse Glossary",
        'glossary_loaded': "Glossary loaded successfully.",
        'error_loading_glossary': "Error loading glossary: {error}",
        'error_creating_glossary': "Error creating glossary: {error}",
    }
}

def load_translation_text():
    texts = {}
    for lang in translations:
        texts[lang] = {}
        for key in translations[lang]:
            if key.endswith('_text'):
                with open(os.path.join('messages', f'{key}_{lang}.txt'), 'r', encoding='utf-8') as file:
                    texts[lang][key] = file.read()
    return texts
