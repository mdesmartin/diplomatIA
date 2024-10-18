# diplomatIA

![Licence](https://img.shields.io/badge/licence-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![Docker](https://img.shields.io/badge/docker-20.10%2B-blue.svg)

## Table des Matières

- [Présentation](#présentation)
- [Fonctionnalités](#fonctionnalités)
- [Architecture](#architecture)
- [Installation](#installation)
  - [Prérequis](#prérequis)
  - [Utilisation du Makefile](#utilisation-du-makefile)
- [Utilisation](#utilisation)
- [Structure du Projet](#structure-du-projet)
- [Technologies](#technologies)
- [Contribution](#contribution)
- [Licence](#licence)
- [Contact](#contact)

## Présentation

**diplomatIA** est un projet personnel visant à développer un agent diplomatique intelligent utilisant la Génération Augmentée par Récupération (RAG). Cet agent exploite une base de données vectorielle d'articles d'un journal specialisé en géopolitique pour fournir des réponses informées aux questions des utilisateurs, accompagnées de citations de sources.

## Fonctionnalités

- **Génération Augmentée par Récupération (RAG) :** Combine l'IA générative avec un système de récupération pour des réponses précises et contextuellement pertinentes.
- **Base de Données Vectorielle avec FAISS :** Indexe efficacement un large corpus d'articles diplomatiques pour une recherche rapide.
- **Pipeline de Données Automatisé :** Extraction, normalisation et indexation des articles EPUB pour des mises à jour fluides.
- **Interface Interactive avec Streamlit :** Interface conviviale permettant une interaction intuitive avec l'agent diplomatique.
- **Déploiement Dockerisé :** Assure la portabilité et la facilité de déploiement sur différents environnements.
- **Automatisation via Makefile :** Simplifie les tâches de construction, d'exécution et de maintenance grâce à des cibles prédéfinies.

## Architecture

diplomatIA/
├── Dockerfile
├── Makefile
├── README.md
├── data
│   ├── extracted_epubs
│   └── raw
│       ├── Le-Journal-Geopolitique-2019-01.epub
│       ├── …
│       └── Le-Journal-Geopolitique-2024-10.epub
├── requirements.txt
└── src
├── build_vector_store.py
├── chatbot_ui.py
├── extract_articles.py
└── rag_query_interface.py

## Installation

### Prérequis

- [Docker](https://www.docker.com/get-started) installé sur votre machine.
- [Make](https://www.gnu.org/software/make/) installé.
- [Git](https://git-scm.com/) installé.

### Utilisation du Makefile

Le projet inclut un `Makefile` pour automatiser les tâches courantes telles que la construction de l'image Docker, l'exécution du conteneur, la reconstruction de la base de données vectorielle et le nettoyage des ressources.

#### Cibles du Makefile

- `all` : Construit et exécute le conteneur Docker.
- `build` : Construit l'image Docker.
- `run` : Exécute le conteneur Docker, initialisant la base de données vectorielle si elle n'existe pas.
- `rebuild` : Reconstruit la base de données vectorielle et redémarre l'application.
- `clean` : Supprime l'image Docker.
- `fclean` : Supprime l'image Docker, le conteneur et le volume Docker associé.

#### Étapes d'installation

1. **Cloner le Dépôt**

   ```bash
   git clone https://github.com/mdesmartin/diplomatIA.git
   cd diplomatIA

2. **Configurer les Variables d’Environnement**

	Créez un fichier .env à la racine du projet et ajoutez votre clé API OpenAI :

		OPENAI_API_KEY=your_openai_api_key

3. **Placer les Fichiers EPUB**

	Assurez-vous que tous les fichiers EPUB du journal géopolitique sont placés dans le répertoire data/raw.

4.	**Construire et Exécuter avec le Makefile**

	•	Construire l’Image Docker
		
		make build


	•	Exécuter le Conteneur Docker

		make run

	Cette commande effectuera les actions suivantes :

	•	Monter le répertoire data et un volume Docker pour la base de données.

	•	Construire la base de données FAISS si elle n’existe pas.

	•	Lancer l’application Streamlit accessible à l’adresse http://localhost:8501.

	•	Reconstruire la Base de Données Vectorielle

		make rebuild

	Cette commande force la reconstruction de l’index FAISS et redémarre l’application Streamlit.

	•	Nettoyer les Ressources Docker

		make clean

	Supprime l’image Docker.

		make fclean

	Supprime l’image Docker, le conteneur et le volume Docker associé.

## Utilisation

1.	**Accéder à l’Application**

	Ouvrez votre navigateur web et naviguez vers http://localhost:8501.

2.	**Interagir avec l’Agent Diplomatique**

	•	Entrez vos questions liées aux enjeux géopolitiques.

	•	Recevez des réponses détaillées basées sur les articles du journal géopolitique.

	•	Consultez les sources citées pour chaque réponse.

3.	**Quitter l’Application**
Cliquez sur le bouton “Quitter” dans l’interface Streamlit pour terminer la session.

## Structure du Projet

•	**Dockerfile** : Définit l’image Docker pour l’application.

•	**Makefile** : Contient les commandes de construction et d’exécution pour simplifier l’utilisation.

•	**data/raw** : Contient les fichiers EPUB bruts du journal géopolitique.

•	**data/extracted_epubs** : Stocke le contenu extrait et traité des EPUB.

•	**src/build_vector_store.py** : Construit la base de données vectorielle FAISS à partir des articles extraits.

•	**src/extract_articles.py** : Extrait et prétraite les articles des fichiers EPUB.

•	**src/rag_query_interface.py** : Gère le moteur de requêtes RAG.

•	**src/chatbot_ui.py** : Implémente l’interface utilisateur basée sur Streamlit.

•	**requirements.txt** : Liste les dépendances Python nécessaires.

## Technologies

•	**Python 3.11** : Langage de programmation principal.

•	**FAISS** : Base de données vectorielle pour des recherches de similarité efficaces.

•	**LlamaIndex** : Gestion des embeddings et des interfaces de requêtes.

•	**Streamlit** : Création de l’interface web interactive.

•	**Docker** : Conteneurisation de l’application pour une portabilité accrue.

•	**BeautifulSoup** : Parsing et extraction des données des fichiers EPUB.

•	**OpenAI API** : Alimente les capacités d’IA générative.

## Contribution

Les contributions sont les bienvenues ! Veuillez suivre les étapes suivantes :

1.	Forker le Dépôt

2.	Créer une Branche de Fonctionnalité

		git checkout -b feature/votreFeature

3.	Committer vos Changements

		git commit -m "Ajout de votre fonctionnalité"

4.	Pousser la Branche

		git push origin feature/votreFeature

5.	Ouvrir une Pull Request

	Assurez-vous que votre code respecte les standards du projet et inclut des tests appropriés.

## Licence

Ce projet est sous licence MIT.

## Contact

**Auteur** : Mehdi DESMARTIN

**LinkedIn** : linkedin.com/in/mdesmartin

**GitHub** : github.com/mdesmartin