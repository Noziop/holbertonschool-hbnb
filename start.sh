#!/bin/bash

# Chemin absolu du projet
PROJECT_PATH="/home/fassihbe/Git/holbertonschool-hbnb"

# Fonction pour arrêter tous les processus
cleanup() {
    echo "Arrêt des serveurs..."
    pkill -f "flask run"
    pkill -f "http-server"
    exit 0
}

# Gestion du CTRL+C
trap cleanup SIGINT

# Démarrer l'API (Part 3)
echo "Démarrage de l'API..."
cd "${PROJECT_PATH}/part3" || exit
poetry run flask run &

# Attendre que l'API démarre
sleep 2

# Démarrer le frontend (Part 4)
echo "Démarrage du frontend..."
cd "${PROJECT_PATH}/part4" || exit
http-server -p 8080 &

echo "Serveurs démarrés !"
echo "API: http://localhost:5000"
echo "Frontend: http://localhost:8080"
echo "Appuyez sur CTRL+C pour arrêter les serveurs."

# Attendre
wait