import subprocess
import importlib
import sys
import os
import re
import xml.etree.ElementTree as ET
import platform

# Liste des modules nécessaires (exclure tkinter car il est intégré)
required_modules = [
    'deepl', ('PIL','pillow'), 'tkinter', 'requests', 'xml.etree.ElementTree', 'platform',
    'os', 're', 'subprocess', 'importlib', 'sys', 'json', 'io', 'time', 'datetime',
    'pandas', 'openpyxl'
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
            if isinstance(module,tuple) and len(module) == 2:
                module_name = module[0]
                install_name = module [1]
            else:
                module_name = module
                install_name = module
            importlib.import_module(module_name)
            print(f"Le module '{install_name}' est déjà installé.")
        except ImportError:
            print(f"Le module {f"'{install_name}'"} n'est pas installé. Installation en cours...")
            try:
                # Tentative d'installation du module
                subprocess.check_call([sys.executable, "-m", "pip", "install", install_name])
                # Vérification après installation
                importlib.import_module(module_name)
                print(f"Le module '{install_name}' a été installé.")
            except Exception as e:
                print(f"Erreur lors de l'installation du module '{install_name}': {e}")
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
    free_pattern = r'^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}:fx$'
    paid_pattern = r'^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{11}[a-z]$'
    return bool(re.match(free_pattern, api_key)) or bool(re.match(paid_pattern, api_key))

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
        if os.path.exists(file_path):
            os.remove(file_path)
        with open(file_path, 'w') as key_file:
            key_file.write(api_key)
        if platform.system() == 'Windows':
            pass
        else:
            os.chmod(file_path, 0o600)
        hide_file(file_path)
        print(f"Clé API sauvegardée et cachée à l'emplacement : {file_path}")
    except PermissionError as e:
        print(f"Erreur lors de l'enregistrement de la clé API : {str(e)}. Vérifiez les permissions du fichier.")
    except Exception as e:
        print(f"Erreur inattendue lors de l'enregistrement de la clé API : {str(e)}")

def load_api_key():
    file_path = get_api_key_filepath()
    if os.path.exists(file_path):
        print("Chargement de la clé API enregistrée.")
        with open(file_path, 'r') as key_file:
            return key_file.read()
    else:
        print("Aucune clé API enregistrée trouvée.")
    return ''