import subprocess
import importlib
import sys
import os
import re
import xml.etree.ElementTree as ET
import platform

# Liste des modules nécessaires (exclure tkinter car il est intégré)
required_modules = [
    'deepl', 'PIL', 'tkinter', 'requests', 'xml.etree.ElementTree', 'platform',
    'os', 're', 'subprocess', 'importlib', 'sys', 'json', 'io', 'time', 'datetime'
]

def is_frozen():
    return getattr(sys, 'frozen', False)

def check_and_install_modules():
    if is_frozen():
        # Ne pas tenter d'installer les modules si le script est exécuté en tant que fichier .exe
        print("Exécution depuis un fichier .exe, les modules doivent déjà être inclus.")
        return

    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"Le module '{module}' est déjà installé.")
        except ImportError:
            print(f"Le module '{module}' n'est pas installé. Installation en cours...")
            try:
                # Tentative d'installation du module
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
                # Vérification après installation
                importlib.import_module(module)
                print(f"Le module '{module}' a été installé.")
            except Exception as e:
                print(f"Erreur lors de l'installation du module '{module}': {e}")
                print("Assurez-vous que l'environnement d'exécution permet l'installation de nouveaux modules.")
                raise

def get_api_key_filepath():
    documents_path = os.path.join(os.path.expanduser("~"), 'Documents')
    if not os.path.exists(documents_path):
        os.makedirs(documents_path)
    
    if platform.system() == 'Windows':
        return os.path.join(documents_path, 'deepl_api_key.txt')
    else:
        return os.path.join(documents_path, '.deepl_api_key.txt')

def is_valid_api_key(api_key):
    pattern = r'^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}:fx$'
    return bool(re.match(pattern, api_key))

def hide_file(filepath):
    if platform.system() == 'Windows':
        subprocess.check_call(['attrib', '+H', filepath])
    else:
        hidden_filepath = os.path.join(os.path.dirname(filepath), '.' + os.path.basename(filepath))
        os.rename(filepath, hidden_filepath)
        filepath = hidden_filepath

def save_api_key(api_key):
    file_path = get_api_key_filepath()
    try:
        with open(file_path, 'w') as key_file:
            key_file.write(api_key)
        hide_file(file_path)
        print(f"Clé API sauvegardée et cachée à l'emplacement: {file_path}")
    except PermissionError as e:
        print(f"Erreur lors de l'enregistrement de la clé API : {str(e)}")

def load_api_key():
    file_path = get_api_key_filepath()
    if os.path.exists(file_path):
        print("Chargement de la clé API enregistrée.")
        with open(file_path, 'r') as key_file:
            return key_file.read()
    else:
        print("Aucune clé API enregistrée trouvée.")
    return ''
