# InDesign Translation Tool

This InDesign Translation Tool is a Python application designed to translate IDML files using the DeepL API. The tool allows users to select multiple IDML files, specify target languages, and use custom glossaries for translation. The translations are performed in a threaded manner to keep the application responsive.

## Features

- Translate IDML files into multiple languages using DeepL API.
- Support for custom glossaries to ensure accurate translation of specific terms.
- Real-time progress updates and the ability to stop the translation process.
- GUI-based file selection and settings configuration.

## Requirements

- Python 3.6 or higher.
- DeepL API Key.
- Required Python modules (automatically installed if missing):
  - deepl
  - tkinter
  - threading
  - datetime
  - os
  - xml.etree.ElementTree
  - zipfile
  - re

## Installation

1. Clone the repository or download the source code.
2. Ensure you have Python installed on your system.
3. Install the required Python modules. The script checks for required modules and installs them if they are missing.

## Usage

1. Run the script using Python:
   ```bash
   python main.py
2. Enter your DeepL API key.
3. Select the IDML files you want to translate.
4. Choose the target languages.
5. (Optional) Enter a glossary in the format word:translation;word:translation.
6 Click "Translate" to start the translation process.

## GUI Components

### Main Window
- File Path: Select the directory or files containing the IDML files to be translated.
- Target Languages: Choose the languages you want to translate the files into (English, German, Spanish).
- DeepL API Key: Enter your DeepL API key. You can toggle the visibility of the key.
- Glossary: Enter custom glossary entries to be used during translation.
- Translate Button: Starts the translation process.
- Stop Button: Stops the ongoing translation process.
- Progress Bar and Label: Shows the current progress of the translation process.

## Functions

### `check_and_install_modules(modules)`
Checks for required modules and installs any that are missing.

### `translate_stories(directory, target_langs, progress_bar, total_files, progress_label, root, translator, glossary_id)`
Translates the content of the IDML stories to the specified target languages.

### `create_idml_zip(source_file, target_lang, progress_bar, total_files, progress_label, root, translator, glossary_id)`
Creates a translated IDML file from the source file and compresses it into a ZIP archive.

### `on_translate()`
Handles the translation process, including user input validation and starting the translation thread.

### `on_stop()`
Stops the ongoing translation process and cleans up temporary files.

### `toggle_api_key_visibility()`
Toggles the visibility of the DeepL API key input.

### `browse_directory()`
Allows users to select a directory containing IDML files for translation.

### `is_valid_api_key(api_key)`
Validates the DeepL API key format.

## Error Handling
The application handles various errors such as invalid API keys, file extraction errors, XML parsing errors, and more. Users are notified through message boxes.

## Contribution
Contributions are welcome! Please fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.

## Acknowledgments
Thanks to DeepL for their powerful translation API.
The tkinter library for providing the GUI framework.
