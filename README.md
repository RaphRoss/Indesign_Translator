# InDesign Translation Tool

This application is designed to help users translate InDesign IDML files using the DeepL API. It provides a graphical user interface built with `tkinter`, allowing users to select files, configure translation settings, and start the translation process.

## Table of Contents
- [Project Overview](#project-overview)
- [Dependencies](#dependencies)
- [Setup](#setup)
- [Usage](#usage)
- [File Descriptions](#file-descriptions)
- [License](#license)

## Project Overview

The InDesign Translation Tool allows you to:
- Select IDML files for translation.
- Choose languages for translation (English, German, Spanish).
- Configure API key for DeepL and manage it securely.
- Translate text in IDML files using the DeepL API and create translated IDML files.

## Dependencies

This project requires the following Python packages:
- `tkinter` (for the GUI)
- `Pillow` (for image processing)
- `deepl` (for translation)
- `zipfile` (for handling IDML files)

Ensure these packages are installed by running the setup script or manually installing them.

## Setup

1. **Clone the repository:**

    ```bash
    git clone git@github.com:RaphRoss/Indesign_Translator.git
    cd <repository-directory>
    ```

2. **Install dependencies:**

    Just run the script to install the required Python packages:

3. **Prepare the environment:**

    Ensure you have a valid DeepL API key. The key will be used to authenticate translation requests.

4. **Run the application:**

    Execute the main script to start the application:

    ```bash
    python Main.py
    ```

## Usage

1. **Select Files:**
   - Click "Browse Directory" to select a folder containing IDML files for translation.
   - A dialog will allow you to choose which files to include.

2. **Configure Translation:**
   - Enter your DeepL API key and click "Save Key" to store it securely.
   - Enter any glossary terms if needed (format: `word:translation`).
   - Select the target languages for translation (English, German, Spanish).
   - Choose whether to notify users upon completion.

3. **Start Translation:**
   - Click "Translate" to begin the translation process.
   - Monitor progress through the progress bar and label.
   - Click "Stop" to halt the translation process if needed.

4. **Manage API Key:**
   - Click the eye icon to toggle the visibility of the API key field.

## File Descriptions

### `Main.py`

The main script for the application. It handles:
- GUI setup using `tkinter`.
- File selection and directory browsing.
- API key management.
- Translation process and progress reporting.

### `Translations.py`

Contains translation data and helper functions for loading translation texts:
- `translations` dictionary: Contains translations for different languages.
- `load_translation_text()` function: Loads long text messages from files.

### `Utils.py`

Utility functions for the application:
- `check_and_install_modules()`: Checks and installs required Python modules.
- `is_valid_api_key(api_key)`: Validates the format of the DeepL API key.
- `hide_file(filepath)`: Hides the API key file for security.
- `save_api_key(api_key)`: Saves and hides the API key.
- `load_api_key()`: Loads the saved API key.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
