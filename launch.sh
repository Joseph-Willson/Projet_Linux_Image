echo "******************* Initialisation de l'application *******************"
source ./venv/bin/activate
echo "******************* l'environnement virtuel est activé *******************"

echo "******************* Collecte des données *******************"
bash ./data_collector/data_collector.sh
echo "******************* Données collectées *******************"

echo "******************* Affichage de l'application *******************"
streamlit run ./Webapp/app.py




