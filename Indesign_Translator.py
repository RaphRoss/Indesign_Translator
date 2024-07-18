import deepl
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import datetime
import os
import xml.etree.ElementTree as ET
import zipfile
from zipfile import ZipFile
import re

# Flag to control the translation thread
stop_translation = False
current_temp_dir = None  # Variable globale pour stocker le répertoire temporaire

def translate_stories(directory, target_langs, progress_bar, total_files, progress_label, root, translator, glossary_id=None):
    global stop_translation
    stories_path = os.path.join(directory, 'Stories')
    if not os.path.exists(stories_path):
        messagebox.showerror("Erreur", f"Le répertoire 'Stories' n'existe pas à l'emplacement {stories_path}.")
        return

    files = [f for f in os.listdir(stories_path) if f.endswith('.xml')]
    total_stories = len(files)
    translated_files = 0
    
    for filename in files:
        if stop_translation:
            break
        file_path = os.path.join(stories_path, filename)
        try:
            tree = ET.parse(file_path)
            xml_root = tree.getroot()
        except ET.ParseError as e:
            messagebox.showerror("Erreur de parsing XML", f"Erreur lors du parsing du fichier {file_path}: {str(e)}")
            continue
        
        for elem in xml_root.iter():
            if stop_translation:
                break
            if 'Content' in elem.tag and elem.text:
                original_text = elem.text
                for target_lang in target_langs:
                    translated_text = translator.translate_text(
                        original_text, 
                        target_lang=target_lang, 
                        preserve_formatting=True,
                        glossary=glossary_id
                    )
                    detected_language = translated_text.detected_source_lang
                    if detected_language == 'FR':
                        elem.text = translated_text.text
                        print(f"Texte traduit: {elem.text}")
                    else:
                        print(f"Le texte est déjà en {detected_language}, {original_text} ne sera pas traduit.")
        
        try:
            tree.write(file_path, encoding='UTF-8', xml_declaration=True)
        except IOError as e:
            messagebox.showerror("Erreur d'écriture", f"Erreur lors de l'écriture du fichier {file_path}: {str(e)}")

        translated_files += 1
        percentage = int(translated_files / total_files * 100)

        # Mettre à jour la barre de progression et l'étiquette de pourcentage
        progress_bar['value'] = percentage
        progress_label.config(text=f"Traduction : {percentage}%")
        root.update_idletasks()

    # Mettre à jour la barre de progression et l'étiquette de pourcentage à la fin de la traduction
    progress_bar['value'] = 100
    progress_label.config(text="Traduction : 100%")

def create_idml_zip(source_file, target_lang, progress_bar, total_files, progress_label, root, translator, glossary_id=None):
    global current_temp_dir
    temp_file = os.path.join(os.path.dirname(source_file), 'Temp')
    current_temp_dir = temp_file  # Stocker le chemin temporaire

    try:
        with ZipFile(source_file, 'r') as zip_ref:
            zip_ref.extractall(temp_file)
    except zipfile.BadZipFile as e:
        messagebox.showerror("Erreur d'extraction", f"Erreur lors de l'extraction du fichier {source_file}: {str(e)}")
        return
    
    translate_stories(temp_file, [target_lang], progress_bar, total_files, progress_label, root, translator, glossary_id)

    # Obtenir les informations de date et heure
    base_name = os.path.splitext(os.path.basename(source_file))[0]  # Nom du fichier sans extension
    now = datetime.datetime.now()  # Date et heure actuelles
    year = now.strftime("%Y")  # Année
    month = now.strftime("%B")  # Mois en toutes lettres
    day = now.strftime("%d")  # Jour
    time = now.strftime("%Hh%M")  # Heure et minute

    output_dir = os.path.join(os.path.dirname(source_file), "Traduction", year, month, day)
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{base_name}_{target_lang}_{time}.idml"
    output_path = os.path.join(output_dir, output_file)

    # Créer le chemin du dossier de sortie 
    with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_STORED) as zf:
        mimetype_path = os.path.join(temp_file, 'mimetype')
        zf.write(mimetype_path, arcname='mimetype')

    with zipfile.ZipFile(output_path, 'a', compression=zipfile.ZIP_DEFLATED) as zf:
        for root_dir, _, files in os.walk(temp_file):
            for file in files:
                if file != 'mimetype':
                    file_path = os.path.join(root_dir, file)
                    arcname = os.path.relpath(file_path, temp_file)
                    zf.write(file_path, arcname=arcname)
    
    return output_path

def on_translate():
    global stop_translation
    stop_translation = False
    
    def run_translation():
        api_key = api_key_entry.get()
        if not is_valid_api_key(api_key):
            messagebox.showwarning("Avertissement", "Veuillez saisir une clé API valide.")
            enable_buttons()
            return

        translator = deepl.Translator(api_key)
        
        files = file_path_entry.get().split(';')
        if not files or files == ['']:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner au moins un fichier à traduire.")
            enable_buttons()
            return
        
        # Vérifier la validité de la clé API en effectuant une requête de test
        try:
            translator.get_usage()
        except deepl.exceptions.AuthorizationException:
            messagebox.showerror("Erreur d'autorisation", "La clé API est invalide ou n'a pas les permissions nécessaires.")
            enable_buttons()
            return
        except Exception as e:
            messagebox.showerror("Erreur de connexion", f"Une erreur s'est produite lors de la vérification de la clé API : {str(e)}")
            enable_buttons()
            return

        files = file_path_entry.get().split(';')
        if not files or files == ['']:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner au moins un fichier à traduire.")
            enable_buttons()
            return

        selected_languages = []
        if english_var.get():
            selected_languages.append("EN-US")
        if german_var.get():
            selected_languages.append("DE")
        if spanish_var.get():
            selected_languages.append("ES")
        
        if not selected_languages:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner au moins une langue.")
            enable_buttons()
            return
        
        glossary_text = glossary_entry.get()
        glossary_id = None
        if glossary_text:
            glossary_entries = [line.split(':') for line in glossary_text.split(';') if ':' in line]
            glossary = {key.strip(): value.strip() for key, value in glossary_entries}
            glossary_id = translator.create_glossary("Custom Glossary", "FR", "EN-US", glossary)

        total_files = sum([len([name for name in os.listdir(os.path.join(os.path.dirname(file), 'Temp', 'Stories')) if name.endswith('.xml')]) for file in files])
        total_steps = len(selected_languages) * total_files
        step = 100 / total_steps

        progress_bar['value'] = 0
        progress_bar.grid(row=9, columnspan=3, pady=20)
        progress_label.grid(row=8, columnspan=3, pady=5)
        stop_button.grid(row=11, columnspan=3, pady=5)
        
        translated_files = []
        for file_path in files:
            if stop_translation:
                break
            temp_dir = os.path.join(os.path.dirname(file_path), 'Temp')

            try:
                with ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            except zipfile.BadZipFile as e:
                messagebox.showerror("Erreur d'extraction", f"Erreur lors de l'extraction du fichier {file_path}: {str(e)}")
                continue
            except FileNotFoundError as e:
                messagebox.showerror("Fichier introuvable", f"Le fichier spécifié {file_path} est introuvable.")
                continue
            except PermissionError as e:
                messagebox.showerror("Permission refusée", f"Vous n'avez pas les droits nécessaires pour accéder au fichier {file_path}.")
                continue

            for lang in selected_languages:
                if stop_translation:
                    break
                output_path = create_idml_zip(file_path, lang, progress_bar, total_steps, progress_label, root, translator, glossary_id)
                translated_files.append(output_path)

        progress_bar.grid_forget()
        progress_label.grid_forget()
        stop_button.grid_forget()
        
        # Ouvrir l'explorateur de fichiers à l'emplacement des fichiers traduits
        if translated_files and not stop_translation:
            output_dir = os.path.dirname(translated_files[0])
            os.startfile(output_dir)

        enable_buttons()

    disable_buttons()
    translation_thread = threading.Thread(target=run_translation)
    translation_thread.start()

def on_stop():
    global stop_translation, current_temp_dir
    stop_translation = True
    if current_temp_dir and os.path.exists(current_temp_dir):
        try:
            os.rmdir(current_temp_dir)
        except OSError as e:
            print(f"Erreur lors de la suppression du répertoire temporaire {current_temp_dir}: {str(e)}")

def disable_buttons():
    translate_button.config(state=tk.DISABLED)
    browse_dir_button.config(state=tk.DISABLED)
    api_key_entry.config(state=tk.DISABLED)
    file_path_entry.config(state=tk.DISABLED)
    glossary_entry.config(state=tk.DISABLED)
    english_checkbutton.config(state=tk.DISABLED)
    german_checkbutton.config(state=tk.DISABLED)
    spanish_checkbutton.config(state=tk.DISABLED)

def enable_buttons():
    translate_button.config(state=tk.NORMAL)
    browse_dir_button.config(state=tk.NORMAL)
    api_key_entry.config(state=tk.NORMAL)
    file_path_entry.config(state=tk.NORMAL)
    glossary_entry.config(state=tk.NORMAL)
    english_checkbutton.config(state=tk.NORMAL)
    german_checkbutton.config(state=tk.NORMAL)
    spanish_checkbutton.config(state=tk.NORMAL)

def browse_directory():
    dir_path = filedialog.askdirectory()
    if dir_path:
        idml_files = []
        for root, _, files in os.walk(dir_path):
            idml_files.extend([os.path.join(root, f) for f in files if f.endswith('.idml')])

        if idml_files:
            popup = tk.Toplevel()
            popup.title("Sélection des fichiers")
            popup.iconbitmap(icon_path)  # Appliquer l'icône de la fenêtre principale

            canvas = tk.Canvas(popup)
            scrollbar = ttk.Scrollbar(popup, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)

            file_vars = {}
            for file in idml_files:
                var = tk.BooleanVar()
                file_vars[file] = var
                ttk.Checkbutton(scrollable_frame, text=os.path.relpath(file, dir_path), variable=var).pack(anchor='w')

            def select_all():
                for var in file_vars.values():
                    var.set(True)
            
            def deselect_all():
                for var in file_vars.values():
                    var.set(False)
            
            def confirm_selection():
                selected_files = [file for file, var in file_vars.items() if var.get()]
                file_path_entry.delete(0, tk.END)
                file_path_entry.insert(0, ';'.join(selected_files))
                popup.destroy()
            
            # Frame pour les boutons de sélection
            button_frame = ttk.Frame(popup)
            ttk.Button(button_frame, text="Tout sélectionner", command=select_all).pack(side='left', padx=5, pady=5)
            ttk.Button(button_frame, text="Tout désélectionner", command=deselect_all).pack(side='left', padx=5, pady=5)
            ttk.Button(button_frame, text="Confirmer", command=confirm_selection).pack(side='left', padx=5, pady=5)
            button_frame.pack(side='bottom', pady=5)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

# Vérifier si la clé API DeepL est valide
def is_valid_api_key(api_key):
    pattern = r'^[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}:fx$'
    return bool(re.match(pattern, api_key))

# Initialisation de la fenêtre principale
root = tk.Tk()
root.title("Indesign Traduction")

# Définir l'icône de la fenêtre et de la barre des tâches
icon_path = os.path.join(os.path.dirname(__file__), "img/Logo.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# Style
style = ttk.Style()
style.configure("TLabel", font=("Arial", 10), padding=5)
style.configure("TEntry", padding=5)
style.configure("TButton", font=("Arial", 10), padding=5)
style.configure("TCheckbutton", font=("Arial", 10), padding=5)
style.configure("TRadiobutton", font=("Arial", 10), padding=5)

# Frame principale
main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Création et placement des widgets
ttk.Label(main_frame, text="Chemin des répertoires/fichiers :").grid(row=0, column=0, padx=10, pady=10, sticky='e')
file_path_entry = ttk.Entry(main_frame, width=50)
file_path_entry.grid(row=0, column=1, padx=10, pady=10)
browse_dir_button = ttk.Button(main_frame, text="Parcourir Dossier", command=browse_directory)
browse_dir_button.grid(row=0, column=2, padx=10, pady=10)

ttk.Label(main_frame, text="Langue(s) sélectionnée(s) :").grid(row=1, column=0, padx=10, pady=10, sticky='e')

english_var = tk.BooleanVar()
german_var = tk.BooleanVar()
spanish_var = tk.BooleanVar()

english_checkbutton = ttk.Checkbutton(main_frame, text="Anglais", variable=english_var)
english_checkbutton.grid(row=1, column=1, sticky='w')
german_checkbutton = ttk.Checkbutton(main_frame, text="Allemand", variable=german_var)
german_checkbutton.grid(row=1, column=1)
spanish_checkbutton = ttk.Checkbutton(main_frame, text="Espagnol", variable=spanish_var)
spanish_checkbutton.grid(row=1, column=1, sticky='e')

ttk.Label(main_frame, text="Prévenir les utilisateurs :").grid(row=2, column=0, padx=10, pady=10, sticky='e')

notify_var = tk.StringVar()
notify_var.set("Oui")
ttk.Radiobutton(main_frame, text="Oui", variable=notify_var, value="Oui").grid(row=2, column=1, sticky='w')
ttk.Radiobutton(main_frame, text="Non", variable=notify_var, value="Non").grid(row=2, column=1, sticky='e')

ttk.Label(main_frame, text="Clé API DeepL :").grid(row=3, column=0, padx=10, pady=10, sticky='e')
api_key_entry = ttk.Entry(main_frame, width=50)
api_key_entry.grid(row=3, column=1, padx=10, pady=10)
api_key_entry.insert(0, "ex:XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX:fx")

# Ajouter un champ pour le glossaire
ttk.Label(main_frame, text="Glossaire (mot:traduction) :").grid(row=4, column=0, padx=10, pady=10, sticky='e')
glossary_entry = ttk.Entry(main_frame, width=50)
glossary_entry.grid(row=4, column=1, padx=10, pady=10)

translate_button = ttk.Button(main_frame, text="Traduire", command=on_translate)
translate_button.grid(row=5, columnspan=3, pady=20)

# Pourcentage de progression
progress_label = ttk.Label(main_frame, text="Traduction : 0%")
progress_label.grid(row=8, columnspan=3, pady=5)
progress_label.grid_forget()

# Barre de progression
progress_bar = ttk.Progressbar(main_frame, orient='horizontal', length=300, mode='determinate')
progress_bar.grid(row=9, columnspan=3, pady=20)
progress_bar.grid_forget()

# Bouton d'arrêt
stop_button = ttk.Button(main_frame, text="Arrêter", command=on_stop)
stop_button.grid(row=11, columnspan=3, pady=5)
stop_button.grid_forget()

# Exécution de la boucle principale
root.mainloop()
