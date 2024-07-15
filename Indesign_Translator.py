import os
import xml.etree.ElementTree as ET
import zipfile
from zipfile import ZipFile
import deepl
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import datetime

# Flag to control the translation thread
stop_translation = False

def translate_stories(directory, target_langs, progress_bar, step, progress_label, root):
    global stop_translation
    stories_path = os.path.join(directory, 'Stories')
    if not os.path.exists(stories_path):
        messagebox.showerror("Erreur", f"Le répertoire 'Stories' n'existe pas à l'emplacement {stories_path}.")
        return

    for filename in os.listdir(stories_path):
        if stop_translation:
            break
        if filename.endswith('.xml'):
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
                        translated_text = translator.translate_text(original_text, target_lang=target_lang, preserve_formatting=True)
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

            # Mettre à jour la barre de progression et l'étiquette
            progress_bar.step(step)
            percentage = int(progress_bar['value'])
            progress_label.config(text=f"Traduction : {percentage}%")
            root.update_idletasks()

def create_idml_zip(source_file, target_lang, progress_bar, step, progress_label, root):
    temp_file = os.path.join(os.path.dirname(source_file), 'Temp')

    try:
        with ZipFile(source_file, 'r') as zip_ref:
            zip_ref.extractall(temp_file)
    except zipfile.BadZipFile as e:
        messagebox.showerror("Erreur d'extraction", f"Erreur lors de l'extraction du fichier {source_file}: {str(e)}")
        return
    
    translate_stories(temp_file, [target_lang], progress_bar, step, progress_label, root)

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
        
        progress_bar['value'] = 0
        progress_bar.grid(row=8, columnspan=3, pady=20)
        progress_label.grid(row=6, columnspan=3, pady=5)
        stop_button.grid(row=9, columnspan=3, pady=5)
        
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
                output_path = create_idml_zip(file_path, lang, progress_bar, progress_label, root)
                translated_files.append(output_path)

        progress_bar.grid_forget()
        progress_label.grid_forget()
        stop_button.grid_forget()
        
        # Ouvrir l'explorateur de fichiers à l'emplacement des fichiers traduits
        if translated_files:
            output_dir = os.path.dirname(translated_files[0])
            os.startfile(output_dir)

        enable_buttons()

    disable_buttons()
    translation_thread = threading.Thread(target=run_translation)
    translation_thread.start()

def on_stop():
    global stop_translation
    stop_translation = True

def disable_buttons():
    translate_button.config(state=tk.DISABLED)
    browse_file_button.config(state=tk.DISABLED)
    browse_dir_button.config(state=tk.DISABLED)

def enable_buttons():
    translate_button.config(state=tk.NORMAL)
    browse_file_button.config(state=tk.NORMAL)
    browse_dir_button.config(state=tk.NORMAL)

def browse_file():
    file_paths = filedialog.askopenfilenames(filetypes=[("IDML files", "*.idml")])
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, ';'.join(file_paths))

def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        file_paths = []
        for root_dir, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.idml'):
                    file_paths.append(os.path.join(root_dir, file))
        
        if file_paths:
            # Créer une popup pour sélectionner les fichiers à traduire
            popup = tk.Toplevel(root)
            popup.title("Sélection des fichiers")
            
            # Canvas et Scrollbar
            canvas = tk.Canvas(popup)
            scrollbar = tk.Scrollbar(popup, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # Bindings pour la molette de la souris
            def _on_mouse_wheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")

            canvas.bind_all("<MouseWheel>", _on_mouse_wheel)

            file_vars = {}
            for file in file_paths:
                var = tk.BooleanVar(value=True)
                file_vars[file] = var
                tk.Checkbutton(scrollable_frame, text=file, variable=var).pack(anchor='w')

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
            button_frame = tk.Frame(popup)
            tk.Button(button_frame, text="Tout sélectionner", command=select_all).pack(side='top', padx=5, pady=5)
            tk.Button(button_frame, text="Tout désélectionner", command=deselect_all).pack(side='top', padx=5, pady=5)
            button_frame.pack(side='left', padx=5, pady=5)

            tk.Button(popup, text="Confirmer", command=confirm_selection).pack(side='right', padx=5, pady=5)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

# Initialisation de la fenêtre principale
root = tk.Tk()
root.title("Indesign Traduction")

# Définir l'icône de la fenêtre et de la barre des tâches
icon_path = os.path.join(os.path.dirname(__file__), "img/Logo.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# Clé d'authentification DeepL
auth_key = "981ae196-3312-4335-b7ad-b330d699b110:fx"
translator = deepl.Translator(auth_key)

# Création et placement des widgets
tk.Label(root, text="Chemin des répertoires/fichiers :").grid(row=0, column=0, padx=10, pady=10, sticky='e')
file_path_entry = tk.Entry(root, width=50)
file_path_entry.grid(row=0, column=1, padx=10, pady=10)
browse_file_button = tk.Button(root, text="Parcourir Fichiers", command=browse_file)
browse_file_button.grid(row=0, column=2, padx=10, pady=10)
browse_dir_button = tk.Button(root, text="Parcourir Dossier", command=browse_directory)
browse_dir_button.grid(row=1, column=2, padx=10, pady=10)

tk.Label(root, text="Langue(s) sélectionnée(s) :").grid(row=1, column=0, padx=10, pady=10, sticky='e')

english_var = tk.BooleanVar()
german_var = tk.BooleanVar()
spanish_var = tk.BooleanVar()

tk.Checkbutton(root, text="Anglais", variable=english_var).grid(row=1, column=1, sticky='w')
tk.Checkbutton(root, text="Allemand", variable=german_var).grid(row=1, column=1)
tk.Checkbutton(root, text="Espagnol", variable=spanish_var).grid(row=1, column=1, sticky='e')

tk.Label(root, text="Prévenir les utilisateurs :").grid(row=2, column=0, padx=10, pady=10, sticky='e')

notify_var = tk.StringVar()
notify_var.set("Oui")
tk.Radiobutton(root, text="Oui", variable=notify_var, value="Oui").grid(row=2, column=1, sticky='w')
tk.Radiobutton(root, text="Non", variable=notify_var, value="Non").grid(row=2, column=1, sticky='e')

translate_button = tk.Button(root, text="Traduire", command=on_translate)
translate_button.grid(row=3, columnspan=3, pady=20)

# Pourcentage de progression
progress_label = tk.Label(root, text="Traduction : 0%")
progress_label.grid(row=4, columnspan=3, pady=5)
progress_label.grid_forget()

# Barre de progression
progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
progress_bar.grid(row=6, columnspan=3, pady=20)
progress_bar.grid_forget()

# Bouton d'arrêt
stop_button = tk.Button(root, text="Arrêter", command=on_stop)
stop_button.grid(row=9, columnspan=3, pady=5)
stop_button.grid_forget()

# Exécution de la boucle principale
root.mainloop()
