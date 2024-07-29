import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import threading
import datetime
import os
import re
import zipfile
from zipfile import ZipFile
from deepl import Translator
import xml.etree.ElementTree as ET  # Ajout de cette ligne

from translations import translations, load_translation_text
from utils import check_and_install_modules, is_valid_api_key, hide_file, load_api_key, save_api_key

# Initial setup
check_and_install_modules()
current_language = 'fr'
stop_translation = False
current_temp_dir = None
output_path = None

# Load long messages
long_messages = load_translation_text()

# Main functions
def translate_ui():
    lang = translations[current_language]
    root.title(lang['title'])
    dir_path_label.config(text=lang['dir_path'])
    browse_dir_button.config(text=lang['browse_dir'])
    langs_selected_label.config(text=lang['langs_selected'])
    notify_users_label.config(text=lang['notify_users'])
    notify_yes_button.config(text=lang['notify_yes'])
    notify_no_button.config(text=lang['notify_no'])
    api_key_label.config(text=lang['api_key'])
    save_key_button.config(text=lang['save_key'])
    glossary_label.config(text=lang['glossary'])
    translate_button.config(text=lang['translate'])
    stop_button.config(text=lang['stop'])
    progress_label.config(text=lang['progress'].format(percentage=0))
    english_checkbutton.config(text=lang['english'])
    german_checkbutton.config(text=lang['german'])
    spanish_checkbutton.config(text=lang['spanish'])

def show_message(title_key, message_key, **kwargs):
    title = translations[current_language][title_key]
    message = translations[current_language][message_key].format(**kwargs)
    messagebox.showinfo(title, message)

def show_warning(title_key, message_key, **kwargs):
    title = translations[current_language][title_key]
    message = translations[current_language][message_key].format(**kwargs)
    messagebox.showwarning(title, message)

def show_error(title_key, message_key, **kwargs):
    title = translations[current_language][title_key]
    message = translations[current_language][message_key].format(**kwargs)
    messagebox.showerror(title, message)

def on_fr_click():
    global current_language
    current_language = 'fr'
    translate_ui()

def on_en_click():
    global current_language
    current_language = 'en'
    translate_ui()

def disable_buttons():
    for widget in (translate_button, browse_dir_button, api_key_entry, file_path_entry, glossary_entry,
                   english_checkbutton, german_checkbutton, spanish_checkbutton, notify_yes_button,
                   notify_no_button, toggle_button, save_key_button, fr, en):
        widget.config(state=tk.DISABLED)

def enable_buttons():
    for widget in (translate_button, browse_dir_button, api_key_entry, file_path_entry, glossary_entry,
                   english_checkbutton, german_checkbutton, spanish_checkbutton, notify_yes_button,
                   notify_no_button, toggle_button, save_key_button, fr, en):
        widget.config(state=tk.NORMAL)

def toggle_api_key_visibility():
    if api_key_entry.cget('show') == '*':
        api_key_entry.config(show='')
        toggle_button.config(image=hide_image)
    else:
        api_key_entry.config(show='*')
        toggle_button.config(image=show_image)

def browse_directory():
    dir_path = filedialog.askdirectory(title=translations[current_language]['file_explorer_title'])
    if dir_path:
        idml_files = []
        for root, _, files in os.walk(dir_path):
            idml_files.extend([os.path.join(root, f) for f in files if f.endswith('.idml')])

        if idml_files:
            popup = tk.Toplevel()
            popup.title(translations[current_language]['popup_title'])
            popup.iconbitmap(icon_path)

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
            
            button_frame = ttk.Frame(popup)
            ttk.Button(button_frame, text=translations[current_language]['select_all'], command=select_all).pack(side='left', padx=5, pady=5)
            ttk.Button(button_frame, text=translations[current_language]['deselect_all'], command=deselect_all).pack(side='left', padx=5, pady=5)
            ttk.Button(button_frame, text=translations[current_language]['confirm'], command=confirm_selection).pack(side='left', padx=5, pady=5)
            button_frame.pack(side='bottom', pady=5)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

def on_save_key():
    api_key = api_key_entry.get()
    if is_valid_api_key(api_key):
        save_api_key(api_key)
        show_message('info', 'saving_api_key')
    else:
        show_warning('warning', 'invalid_api_key')

def on_stop():
    global stop_translation, current_temp_dir
    stop_translation = True
    if current_temp_dir and os.path.exists(current_temp_dir):
        try:
            os.rmdir(current_temp_dir)
            os.remove(output_path)
        except OSError as e:
            print(f"Erreur lors de la suppression du répertoire temporaire {current_temp_dir}: {str(e)}")

# Main application logic
def on_translate():
    global stop_translation
    stop_translation = False
    
    def run_translation():
        api_key = api_key_entry.get()
        if not is_valid_api_key(api_key):
            show_warning('warning', 'invalid_api_key')
            enable_buttons()
            return

        translator = Translator(api_key)

        files = file_path_entry.get().split(';')
        if not files or files == ['']:
            show_warning('warning', 'warning_no_files')
            enable_buttons()
            return

        try:
            translator.get_usage()
        except Exception as e:
            show_error('error', 'error_connection', error=str(e))
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
            show_warning('warning', 'warning_no_lang')
            enable_buttons()
            return

        glossary_text = glossary_entry.get()
        glossary_id = None
        if glossary_text:
            glossary_entries = [line.split(':') for line in glossary_text.split(';') if ':' in line]
            glossary = {key.strip(): value.strip() for key, value in glossary_entries}
            glossary_id = translator.create_glossary("Custom Glossary", "FR", "EN-US", glossary)

        total_files = 0
        for file in files:
            temp_stories_path = os.path.join(os.path.dirname(file), 'Temp', 'Stories')
            if os.path.exists(temp_stories_path):
                total_files += len([name for name in os.listdir(temp_stories_path) if name.endswith('.xml')])
            else:
                show_warning('warning', 'warning_no_stories_dir', file=file)
                continue

        if total_files == 0:
            show_warning('warning', 'warning_no_xml')
            enable_buttons()
            return

        total_steps = len(selected_languages) * total_files

        progress_bar['maximum'] = 100
        progress_bar.grid(row=9, columnspan=3, pady=20)
        progress_label.grid(row=8, columnspan=3, pady=5)
        stop_button.grid(row=11, columnspan=3, pady=5)

        translated_files = 0
        for file_path in files:
            if stop_translation:
                break
            temp_dir = os.path.join(os.path.dirname(file_path), 'Temp')

            try:
                with ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
            except zipfile.BadZipFile as e:
                show_error('error', 'error_extraction', file=file_path, error=str(e))
                continue
            except FileNotFoundError as e:
                show_error('error', 'file_not_found', file=file_path)
                continue
            except PermissionError as e:
                show_error('error', 'permission_error', file=file_path)
                continue

            for lang in selected_languages:
                if stop_translation:
                    break
                output_path, translated_files = create_idml_zip(file_path, lang, progress_bar, total_steps, progress_label, root, translator, glossary_id, translated_files)

        progress_bar.grid_forget()
        progress_label.grid_forget()
        stop_button.grid_forget()

        if translated_files and not stop_translation:
            output_dir = os.path.dirname(output_path)
            os.startfile(output_dir)

        enable_buttons()

    disable_buttons()
    translation_thread = threading.Thread(target=run_translation)
    translation_thread.start()

def translate_stories(directory, target_langs, progress_bar, total_files, progress_label, root, translator, glossary_id=None, translated_files=0):
    global stop_translation
    stories_path = os.path.join(directory, 'Stories')
    if not os.path.exists(stories_path):
        show_error('error', 'warning_no_stories_dir', file=stories_path)
        return translated_files

    files = [f for f in os.listdir(stories_path) if f.endswith('.xml')]
    
    for filename in files:
        if stop_translation:
            break
        file_path = os.path.join(stories_path, filename)
        try:
            tree = ET.parse(file_path)
            xml_root = tree.getroot()
        except ET.ParseError as e:
            show_error('error', 'error_parsing', file=file_path, error=str(e))
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
                        print(translations[current_language]['text_translated'].format(text=elem.text))
                    else:
                        print(translations[current_language]['file_already_translated'].format(language=detected_language, text=original_text))
        
        try:
            tree.write(file_path, encoding='UTF-8', xml_declaration=True)
        except IOError as e:
            show_error('error', 'error_writing', file=file_path, error=str(e))

        translated_files += 1
        percentage = int(translated_files / total_files * 100)

        progress_bar['value'] = percentage
        progress_label.config(text=translations[current_language]['progress'].format(percentage=percentage))
        root.update_idletasks()

    return translated_files

def create_idml_zip(source_file, target_lang, progress_bar, total_files, progress_label, root, translator, glossary_id=None, translated_files=0):
    global current_temp_dir
    temp_file = os.path.join(os.path.dirname(source_file), 'Temp')
    current_temp_dir = temp_file

    try:
        with ZipFile(source_file, 'r') as zip_ref:
            zip_ref.extractall(temp_file)
    except zipfile.BadZipFile as e:
        show_error('error', 'error_extraction', file=source_file, error=str(e))
        return translated_files
    
    translated_files = translate_stories(temp_file, [target_lang], progress_bar, total_files, progress_label, root, translator, glossary_id, translated_files)

    base_name = os.path.splitext(os.path.basename(source_file))[0]
    now = datetime.datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%B")
    day = now.strftime("%d")
    time = now.strftime("%Hh%Mm")
    seconds = now.strftime("%Ss")

    output_dir = os.path.join(os.path.dirname(source_file), "Traduction", year, month, day)
    os.makedirs(output_dir, exist_ok=True)
    output_file = f"{base_name}_{target_lang}_{time}{seconds}.idml"
    output_path = os.path.join(output_dir, output_file)

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
    
    return output_path, translated_files

# Main GUI setup
root = tk.Tk()
root.title(translations[current_language]['title'])
icon_path = os.path.join(os.path.dirname(__file__), "img/Logo.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

style = ttk.Style()
style.configure("TLabel", font=("Arial", 10), padding=5)
style.configure("TEntry", padding=5)
style.configure("TButton", font=("Arial", 10), padding=5)
style.configure("TCheckbutton", font=("Arial", 10), padding=5)
style.configure("TRadiobutton", font=("Arial", 10), padding=5)

main_frame = ttk.Frame(root, padding="10 10 10 10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

dir_path_label = ttk.Label(main_frame, text=translations[current_language]['dir_path'])
dir_path_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
file_path_entry = ttk.Entry(main_frame, width=50)
file_path_entry.grid(row=1, column=1, padx=10, pady=10)
browse_dir_button = ttk.Button(main_frame, text=translations[current_language]['browse_dir'], command=browse_directory)
browse_dir_button.grid(row=1, column=2, padx=10, pady=10)

langs_selected_label = ttk.Label(main_frame, text=translations[current_language]['langs_selected'])
langs_selected_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')

english_var = tk.BooleanVar()
german_var = tk.BooleanVar()
spanish_var = tk.BooleanVar()

english_checkbutton = ttk.Checkbutton(main_frame, text=translations[current_language]['english'], variable=english_var)
english_checkbutton.grid(row=2, column=1, sticky='w')
german_checkbutton = ttk.Checkbutton(main_frame, text=translations[current_language]['german'], variable=german_var)
german_checkbutton.grid(row=2, column=1)
spanish_checkbutton = ttk.Checkbutton(main_frame, text=translations[current_language]['spanish'], variable=spanish_var)
spanish_checkbutton.grid(row=2, column=1, sticky='e')

notify_users_label = ttk.Label(main_frame, text=translations[current_language]['notify_users'])
notify_users_label.grid(row=3, column=0, padx=10, pady=10, sticky='e')
notify_var = tk.StringVar()
notify_var.set("Oui")
notify_yes_button = ttk.Radiobutton(main_frame, text=translations[current_language]['notify_yes'], variable=notify_var, value="Oui")
notify_yes_button.grid(row=3, column=1, sticky='w')
notify_no_button = ttk.Radiobutton(main_frame, text=translations[current_language]['notify_no'], variable=notify_var, value="Non")
notify_no_button.grid(row=3, column=1, sticky='e')

show_image_path = os.path.join(os.path.dirname(__file__), "img/show.png")
hide_image_path = os.path.join(os.path.dirname(__file__), "img/hide.png")
show_image = ImageTk.PhotoImage(Image.open(show_image_path))
hide_image = ImageTk.PhotoImage(Image.open(hide_image_path))

entry_frame = ttk.Frame(main_frame)
entry_frame.grid(row=4, column=1, padx=10, pady=10, sticky='ew')

api_key_label = ttk.Label(main_frame, text=translations[current_language]['api_key'])
api_key_label.grid(row=4, column=0, padx=10, pady=10, sticky='e')
api_key_entry = ttk.Entry(entry_frame, width=40, show='*')
api_key_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
toggle_button = tk.Button(entry_frame, image=show_image, command=toggle_api_key_visibility, bd=0, highlightthickness=0, relief='flat')
toggle_button.pack(side=tk.RIGHT)
api_key_entry.insert(0, load_api_key())
main_frame.grid_columnconfigure(1, weight=1)

save_key_button = ttk.Button(main_frame, text=translations[current_language]['save_key'], command=on_save_key)
save_key_button.grid(row=4, column=2, padx=10, pady=10)

glossary_label = ttk.Label(main_frame, text=translations[current_language]['glossary'])
glossary_label.grid(row=5, column=0, padx=10, pady=10, sticky='e')
glossary_entry = ttk.Entry(main_frame, width=50)
glossary_entry.grid(row=5, column=1, padx=10, pady=10)

translate_button = ttk.Button(main_frame, text=translations[current_language]['translate'], command=on_translate)
translate_button.grid(row=6, columnspan=3, pady=20)

fr_image_path = os.path.join(os.path.dirname(__file__), "img/fr.png")
en_image_path = os.path.join(os.path.dirname(__file__), "img/USA.png")

fr_image = ImageTk.PhotoImage(Image.open(fr_image_path))
en_image = ImageTk.PhotoImage(Image.open(en_image_path))

small_size = (30, 20)
fr_image = ImageTk.PhotoImage(Image.open(fr_image_path).resize(small_size, Image.LANCZOS))
en_image = ImageTk.PhotoImage(Image.open(en_image_path).resize(small_size, Image.LANCZOS))

button_frame = ttk.Frame(main_frame)
button_frame.grid(row=0, column=0, padx=0, pady=0, sticky='nw')

fr = tk.Button(button_frame, image=fr_image, command=on_fr_click, bd=0, highlightthickness=0, relief='flat')
fr.pack(side=tk.LEFT, padx=(0, 1))
en = tk.Button(button_frame, image=en_image, command=on_en_click, bd=0, highlightthickness=0, relief='flat')
en.pack(side=tk.LEFT, padx=(1, 0))

progress_label = ttk.Label(main_frame, text=translations[current_language]['progress'].format(percentage=0))
progress_label.grid(row=8, columnspan=3, pady=5)
progress_label.grid_forget()

progress_bar = ttk.Progressbar(main_frame, orient='horizontal', length=300, mode='determinate')
progress_bar.grid(row=9, columnspan=3, pady=20)
progress_bar.grid_forget()

stop_button = ttk.Button(main_frame, text=translations[current_language]['stop'], command=on_stop)
stop_button.grid(row=11, columnspan=3, pady=5)
stop_button.grid_forget()

root.mainloop()