#!/bin/bash

# Activer l'environnement virtuel
source ./venv/bin/activate

# Récupérer l'image avec curl et la placer dans un dossier source
curl -o image_content_1.jpeg "https://media.licdn.com/dms/image/D4E03AQH3np9QMfiZUw/profile-displayphoto-shrink_800_800/0/1697620991340?e=1713398400&v=beta&t=xZ8rIzhWsBeZTjDiRNAWzQrqycFATm--m7gxrcCG1hw"
curl -o image_content_2.jpg "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Cristiano_Ronaldo_playing_for_Al_Nassr_FC_against_Persepolis%2C_September_2023_%28cropped%29.jpg/375px-Cristiano_Ronaldo_playing_for_Al_Nassr_FC_against_Persepolis%2C_September_2023_%28cropped%29.jpg"
curl -o image_content_3.jpg "https://www.missnumerique.com/blog/wp-content/uploads/reussir-sa-photo-de-profil-michael-dam.jpg"

curl -o image_style_1.jpg "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg/390px-Van_Gogh_-_Starry_Night_-_Google_Art_Project.jpg"
curl -o image_style_2.jpg "https://cdn-cpjnb.nitrocdn.com/QUemDNPMnvyKLckhEQXFOXxbJNSKFcjW/assets/images/optimized/rev-1851576/www.blog-le-dessin.com/wp-content/uploads/2023/02/refletintime-tableau-abstrait-virginie-ayala-web-1536x1188.jpg"
curl -o image_style_3.jpeg "https://cc-prod.scene7.com/is/image/CCProdAuthor/Row%202%20-%201?$pjpeg$&jpegSize=100&wid=280"

# Créer le dossier source s'il n'existe pas
mkdir -p content_images
mkdir -p style_images

# Déplacer l'image téléchargée dans le dossier source
mv image_content_1.jpeg content_images/
mv image_content_2.jpg content_images/
mv image_content_3.jpg content_images/

mv image_style_1.jpg style_images/
mv image_style_2.jpg style_images/
mv image_style_3.jpeg style_images/


# Donner des permissions au dossier source
chmod +x ./data_collector/data_collector.sh
