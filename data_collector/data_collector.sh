#!/bin/bash

# Activer l'environnement virtuel
source ./venv/bin/activate

# Récupérer l'image avec curl et la placer dans un dossier source
curl -o image1.jpeg "https://media.licdn.com/dms/image/D4E03AQH3np9QMfiZUw/profile-displayphoto-shrink_800_800/0/1697620991340?e=1713398400&v=beta&t=xZ8rIzhWsBeZTjDiRNAWzQrqycFATm--m7gxrcCG1hw"

curl -o image2.jpg "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/390px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg"

# Créer le dossier source s'il n'existe pas
mkdir -p content_images
mkdir -p style_images

# Déplacer l'image téléchargée dans le dossier source
mv image1.jpeg content_images/
mv image2.jpg style_images/

# Donner des permissions au dossier source
chmod +x ./data_collector/data_collector.sh
