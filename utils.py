import subprocess
import importlib
import sys
import os
import re
import xml.etree.ElementTree as ET
from deepl import Translator

# Liste des modules nécessaires
required_modules = [
    'deepl', 'tkinter', 'threading', 'datetime', 'os', 'xml.etree.ElementTree', 
    'zipfile', 're', 'tkinter.filedialog', 'tkinter.messagebox', 'tkinter.ttk',
    'PIL', 'PIL.Image', 'PIL.ImageTk'
]

# Vérifier et installer les modules manquants
def check_and_install_modules():
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"Le module '{module}' est déjà installé.")
        except ImportError:
            print(f"Le module '{module}' n'est pas installé. Installation en cours...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])
            print(f"Le module '{module}' a été installé.")

def is_valid_api_key(api_key):
    pattern = r'^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}:fx$'
    return bool(re.match(pattern, api_key))

def hide_file(filepath):
    if os.name == 'nt':
        subprocess.check_call(['attrib', '+H', filepath])

def save_api_key(api_key):
    file_path = os.path.join(os.path.dirname(__file__), 'deepl_api_key.txt')
    try:
        with open(file_path, 'w') as key_file:
            key_file.write(api_key)
        hide_file(file_path)
    except PermissionError as e:
        print(f"Erreur lors de l'enregistrement de la clé API : {str(e)}")

def load_api_key():
    file_path = os.path.join(os.path.dirname(__file__), 'deepl_api_key.txt')
    if os.path.exists(file_path):
        print("Chargement de la clé API enregistrée.")
        with open(file_path, 'r') as key_file:
            return key_file.read()
    else:
        print("Aucune clé API enregistrée trouvée.")
    return ''
