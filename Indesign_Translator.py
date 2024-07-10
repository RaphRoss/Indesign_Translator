import os
import requests
import xml.etree.ElementTree as ET
import zipfile
from zipfile import ZipFile
import deepl
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkinter import PhotoImage
import threading

def translate_stories(directory, target_langs, progress_bar, step, root):
    stories_path = os.path.join(directory, 'Stories')
    if not os.path.exists(stories_path):
        messagebox.showerror("Erreur", f"Le répertoire 'Stories' n'existe pas à l'emplacement {stories_path}.")
        return

    total_files = len([name for name in os.listdir(stories_path) if name.endswith('.xml')])
    current_file = 0
    
    for filename in os.listdir(stories_path):
        if filename.endswith('.xml'):
            file_path = os.path.join(stories_path, filename)
            tree = ET.parse(file_path)
            xml_root = tree.getroot()

            for elem in xml_root.iter():
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

            tree.write(file_path, encoding='UTF-8', xml_declaration=True)
            
            #Faire avancer la barre
            current_file += 1
            progress_bar.step(step)
            root.update_idletasks()

def create_idml_zip(source_file, target_lang, progress_bar, step, root):
    temp_file = os.path.join(os.path.dirname(source_file), 'Temp')

    with ZipFile(source_file, 'r') as zip_ref:
        zip_ref.extractall(temp_file)

    translate_stories(temp_file, [target_lang], progress_bar, step, root)

    base_name = os.path.splitext(os.path.basename(source_file))[0]
    output_file = f"{base_name}_{target_lang}.idml"
    output_path = os.path.join(os.path.dirname(source_file), output_file)

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
    def run_translation():
        files = file_path_entry.get().split(';')
        if not files:
            messagebox.showwarning("Avertissement", "Veuillez entrer le chemin des répertoires/fichiers.")
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
            return
        
        progress_bar['value'] = 0
        progress_bar.grid(row=4, columnspan=3, pady=20)
        
        translated_files = []
        for file_path in files:
            temp_dir = os.path.join(os.path.dirname(file_path), 'Temp')
            with ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Vérification de l'existence du répertoire 'Stories'
            stories_path = os.path.join(temp_dir, 'Stories')
            if not os.path.exists(stories_path):
                messagebox.showerror("Erreur", f"Le répertoire 'Stories' n'existe pas à l'emplacement {stories_path}.")
                return

            total_files = len([name for name in os.listdir(stories_path) if name.endswith('.xml')])
            total_steps = len(selected_languages) * total_files
            step = 100 / total_steps

            for lang in selected_languages:
                output_path = create_idml_zip(file_path, lang, progress_bar, step, root)
                translated_files.append(output_path)

        progress_bar.grid_forget()
        messagebox.showinfo("Information", f"Traduction terminée. Fichiers traduits:\n" + "\n".join(translated_files))

    translation_thread = threading.Thread(target=run_translation)
    translation_thread.start()

def browse_file():
    file_paths = filedialog.askopenfilenames(filetypes=[("IDML files", "*.idml")])
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, ';'.join(file_paths))

# Initialisation de la fenêtre principale
root = tk.Tk()
root.title("Indesign Traduction")

# Définir l'icône de la fenêtre et de la barre des tâches
icon_path = os.path.join(os.path.dirname(__file__),  "img/Logo.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# Clé d'authentification DeepL
auth_key = "8429c6af-1fe2-41ff-96fd-309c64a08e4d:fx"
translator = deepl.Translator(auth_key)

# Création et placement des widgets
tk.Label(root, text="Chemin des répertoires/fichiers :").grid(row=0, column=0, padx=10, pady=10, sticky='e')
file_path_entry = tk.Entry(root, width=50)
file_path_entry.grid(row=0, column=1, padx=10, pady=10)
browse_button = tk.Button(root, text="Parcourir", command=browse_file)
browse_button.grid(row=0, column=2, padx=10, pady=10)

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

progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
progress_bar.grid(row=4, columnspan=3, pady=20)
progress_bar.grid_forget()

# Exécution de la boucle principale
root.mainloop()
