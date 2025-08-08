# Projet d'API de Génération de Code avec Interface Web

Ce projet met à disposition une API de génération de code basée sur le modèle `Salesforce/codegen-350M-mono`, accompagnée d'une interface web interactive construite avec Streamlit. L'ensemble est entièrement conteneurisé avec Docker et intègre des fonctionnalités de surveillance ainsi qu'un pipeline d'intégration continue (CI) avec GitHub Actions.

## Fonctionnalités

* **Backend Robuste** : Une API construite avec **FastAPI** qui sert le modèle de génération de code.
* **Frontend Intuitif** : Une interface utilisateur développée avec **Streamlit** permettant de dialoguer avec l'API et de visualiser les métriques.
* **Surveillance Intégrée** :
    * Un endpoint `/metrics` pour collecter les temps de réponse, le nombre de requêtes et les erreurs.
    * Un endpoint `/health` pour vérifier l'état de santé de l'API.
    * Un tableau de bord sur l'interface Streamlit pour visualiser ces informations.
* **Conteneurisation** : L'ensemble de l'application (backend et frontend) est géré par **Docker** et **Docker Compose** pour un déploiement simple et reproductible.
* **Intégration Continue** : Un workflow **GitHub Actions** est configuré pour lancer automatiquement les tests unitaires et construire les images Docker à chaque push sur la branche `main`.

##  Installation et Lancement

### Prérequis

* Docker
* Docker Compose

### Étapes

1.  **Clonez le dépôt :**
    ```bash
    git clone https://github.com/M4nu974/OPCO-Module-5.git
    cd OPCO-Module-5
    ```

2.  **Vérifiez les dépendances :**
    Assurez-vous d'avoir deux fichiers `requirements.txt` distincts :
    * `backend/requirements.txt` pour les dépendances de FastAPI (torch, transformers, etc.).
    * `frontend/requirements.txt` pour les dépendances de Streamlit (streamlit, requests).

3.  **Lancez l'application avec Docker Compose :**
    Cette commande va construire les images Docker pour le backend et le frontend, puis démarrer les conteneurs.
    ```bash
    docker-compose up --build
    ```

4.  **Accédez à l'application :**
    * L'interface web Streamlit est accessible à l'adresse : **http://localhost:8501**
    * L'API FastAPI est accessible à l'adresse : **http://localhost:8001**

##  Tests

Pour lancer les tests unitaires du backend, assurez-vous d'avoir installé les dépendances locales, puis exécutez la commande suivante depuis la racine du projet :

```bash
# Installer les dépendances de test
pip install -r backend/requirements.txt
pip install pytest pytest-mock

# Lancer les tests (en ignorant les tests lents d'intégration)
pytest
```

## Endpoints de l'API

* `POST /api/v1/chat/completions` : Endpoint principal pour envoyer un prompt et recevoir une complétion de code.
* `GET /metrics` : Expose les métriques de performance de l'API au format JSON.
* `GET /health` : Endpoint de vérification de santé qui retourne `{"status": "ok"}` si l'API est fonctionnelle.
