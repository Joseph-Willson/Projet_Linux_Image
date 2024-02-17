#!/bin/bash

# Installer les dépendances Python via pip
pip install -r requirements.txt

# Installation de Streamlit
pip install streamlit

# Installation des autres dépendances
pip install tensorflow matplotlib numpy

# Vous pouvez également exécuter d'autres commandes d'installation nécessaires à votre projet

# démarrage du service Docker
docker-compose up -d

# Assurez-vous que votre script est exécutable
chmod +x install.sh
