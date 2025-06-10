# InDesign Translation Tool

This application is designed to help users translate InDesign IDML files using the DeepL API. It provides a graphical user interface built with `tkinter`, allowing users to select files, configure translation settings, and start the translation process.

## Table of Contents
- [Project Overview](#project-overview)
- [Dependencies](#dependencies)
- [Setup](#setup)
- [Usage](#usage)
- [Glossary Feature](#glossary-feature)
- [File Descriptions](#file-descriptions)
- [License](#license)

## Project Overview

The InDesign Translation Tool allows you to:
- Select IDML files for translation.
- Choose languages for translation (English, German, Spanish, French).
- Configure API key for DeepL and manage it securely.
- Translate text in IDML files using the DeepL API and create translated IDML files.
- Optionally, use a custom glossary for translation consistency.

## Dependencies

This project requires the following Python packages:
- `tkinter` (for the GUI)
- `Pillow` (for image processing)
- `deepl` (for translation)
- `zipfile` (for handling IDML files)
- `pandas` (for processing Excel files used for glossaries)

Ensure these packages are installed by running the setup script or manually installing them.

## Setup

1. **Clone the repository:**

    ```bash
    git clone git@github.com:RaphRoss/Indesign_Translator.git
    cd <repository-directory>
    ```

2. **Install dependencies:**

    Run the script to install the required Python packages:

    ```bash
    python main.py
    ```

3. **Prepare the environment:**

    Ensure you have a valid DeepL API key. The key will be used to authenticate translation requests.

4. **Run the application:**

    Execute the main script to start the application:

    ```bash
    python main.py
    ```

## Usage

1. **Select Files:**
   - Click "Browse Directory" to select a folder containing IDML files for translation.
   - A dialog will allow you to choose which files to include.

2. **Configure Translation:**
   - Enter your DeepL API key and click "Save Key" to store it securely.
   - Optionally, load a glossary (explained in detail below in the [Glossary Feature](#glossary-feature) section).
   - Select the target languages for translation (English, German, Spanish, French).
   - Choose whether to notify users upon completion.

3. **Start Translation:**
   - Click "Translate" to begin the translation process.
   - Monitor progress through the progress bar and label.
   - Click "Stop" to halt the translation process if needed.

4. **Manage API Key:**
   - Click the eye icon to toggle the visibility of the API key field.

## Glossary Feature

The glossary feature allows you to use a custom list of terms to ensure consistency across translations. This is particularly useful for industry-specific terminology or brand-specific language.

### Glossary Format

The glossary must be an Excel file with two columns:
- **Source**: The original word or phrase to be translated.
- **Target**: The translated word or phrase that should replace the original.

Here’s an example of what your Excel glossary file should look like:

| Source       | Target      |
|--------------|-------------|
| marketing    | marketing   |
| manager      | responsable |
| team leader  | chef d'équipe |
| report       | rapport     |

### How to Use the Glossary

1. **Prepare your glossary file**:
   - Create an Excel file (`.xlsx` or `.xls`) with two columns: "Source" (for original terms) and "Target" (for translated terms).
   - Make sure that the "Source" and "Target" columns are well-structured, with no missing values.

2. **Load the glossary in the tool**:
   - Once your glossary file is ready, click the "Browse Glossary" button in the application.
   - Select your glossary file from the file explorer.
   - After selection, the glossary file name will appear in the glossary preview box.

3. **Use the glossary during translation**:
   - If you have selected a glossary, the tool will automatically use it during the translation process.
   - The terms defined in the glossary will be prioritized during translation.
   - If no glossary is selected, the translation will proceed as normal without any glossary-based modifications.

4. **Glossary loading success**:
   - The tool will verify that the glossary is correctly formatted and load it.
   - If the glossary is successfully loaded, a message will confirm its readiness.
   - If there are issues (e.g., missing columns or rows), an error message will alert you.

5. **Optional**:
   - The glossary is optional. If you don't load a glossary, the translation will still proceed with the default DeepL settings.

### Glossary Troubleshooting

- **Invalid Glossary File**: Ensure that your Excel file contains both "Source" and "Target" columns, with no empty values.
- **File Format**: Only `.xlsx` or `.xls` files are supported for the glossary feature.
- **Glossary Not Being Applied**: If the translation doesn't seem to be using the glossary, double-check that the terms are correctly spelled and match the source text exactly (e.g., "Marketing" vs "marketing").

## File Descriptions

### `Main.py`

The main script for the application. It handles:
- GUI setup using `tkinter`.
- File selection and directory browsing.
- API key management.
- Glossary loading.
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

## To Do
- Send Outlook email with "notify user"

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
