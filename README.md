# Indesign Translator

This project is a tkinter application for translating IDML files using the DeepL API. The application lets you select IDML files, choose translation languages, and display a progress bar during the translation process.

## Features
- Automatic translation of IDML files using the DeepL API.
- Simple, intuitive user interface created with tkinter.
- Support for multiple translation languages: English, German, Spanish.
- Display of a progress bar to monitor translation progress.

## Prerequisites
- Python 3.x
- Python modules: requests, tkinter, zipfile, xml, deepl

## Installation
1. Clone the repository on your local machine:

       git clone https://github.com/votre-utilisateur/indesign-traduction.git

2. Go to the project directory :

       cd indesign-traduction

3. Install the required dependencies:

       pip install requests deepl

## Configuration
1. Make sure you have an icon file in .ico format for the window icon. Place this file in the project directory and modify the icon path in the main script (icon_path).

2. Update the authentication key DeepL in the main script:

       auth_key = "your_deepl_key:fx"

## Usage
1. Run the main script to launch the tkinter application:

       python Indesign_Translator.py

2. Use the interface to :
      - Browse and select IDML files.
      - Select translation languages (English, German, Spanish).
      - Start the translation process by clicking on the "Translate" button.
      - Once the translation is complete, an information message will appear with the paths to the translated files.

## Project structure
- Indesign_Translator.py: Main script containing the tkinter interface and translation logic.
- README.md: This file contains user instructions and project information.
