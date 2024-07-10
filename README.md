# Indesign Traduction

Ce projet est une application tkinter pour traduire des fichiers IDML en utilisant l'API DeepL. L'application permet de sélectionner des fichiers IDML, de choisir les langues de traduction, et d'afficher une barre de progression pendant le processus de traduction.

## Fonctionnalités
- Traduction automatique de fichiers IDML en utilisant l'API DeepL.
- Interface utilisateur simple et intuitive créée avec tkinter.
- Prise en charge de plusieurs langues de traduction : Anglais, Allemand, Espagnol.
- Affichage d'une barre de progression pour suivre l'avancement de la traduction.

## Prérequis
- Python 3.x
- Modules Python : requests, tkinter, zipfile, xml, deepl

## Installation
1. Clonez le repository sur votre machine locale :

       git clone https://github.com/votre-utilisateur/indesign-traduction.git

2. Accédez au répertoire du projet :

       cd indesign-traduction

3. Installez les dépendances requises :

       pip install requests deepl

## Configuration
1. Assurez-vous d'avoir un fichier d'icône au format .ico pour l'icône de la fenêtre. Placez ce fichier dans le répertoire du projet et modifiez le chemin de l'icône dans le script principal (icon_path).

2. Mettez à jour la clé d'authentification DeepL dans le script principal :

       auth_key = "votre_cle_deepl:fx"

## Utilisation
1. Exécutez le script principal pour lancer l'application tkinter :

       python indesign_traduction.py

2. Utilisez l'interface pour :
      - Parcourir et sélectionner des fichiers IDML.
      - Choisir les langues de traduction (Anglais, Allemand, Espagnol).
      - Lancer le processus de traduction en cliquant sur le bouton "Traduire".
      - Une fois la traduction terminée, un message d'information apparaîtra avec les chemins des fichiers traduits.

## Structure du projet
- Indesign_Translator.py : Script principal contenant l'interface tkinter et la logique de traduction.
- README.md : Ce fichier, contenant les instructions d'utilisation et les informations sur le projet.
