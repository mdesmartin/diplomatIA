# chatbot_ui.py

import os
from dotenv import load_dotenv
import streamlit as st
from rag_query_interface import load_query_engine

load_dotenv()

# Vérifiez que la clé API est chargée
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY is not set. Please check your .env file.")
else:
    print("API Key successfully loaded.")

# Configuration de la page et du titre
st.set_page_config(page_title="diplomatIA", page_icon="🌎", layout="centered", initial_sidebar_state="auto")
st.title("diplomatIA 🌎")
st.info("Posez n’importe quelle question liée aux enjeux géopolitiques et obtenez des réponses pertinentes basées sur des articles du Monde diplomatique.", icon="📄")

# Chemin vers le dossier contenant l'index
index_save_path = "db"  # Assurez-vous que ce chemin est correct

# Charger le query engine
query_engine = load_query_engine(index_save_path)

# Initialisation de l'historique de chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Comment puis-je vous aider aujourd’hui ? Posez n’importe quelle question."}]

# Zone de saisie pour les questions de l'utilisateur
if prompt := st.chat_input("Posez votre question"):
    # Ajouter le message de l'utilisateur à l'historique
    st.session_state.messages.append({"role": "user", "content": prompt})

# Affichage de l'historique de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Traitement de la question de l'utilisateur et affichage de la réponse
if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        # Interroger le query engine et obtenir la réponse
        response = query_engine.query(st.session_state.messages[-1]["content"])
        generated_answer = response.response

        # Afficher la réponse générée
        st.write(generated_answer)

        # Collecter les métadonnées des sources
        sources = {}
        for node_with_score in response.source_nodes:
            node = node_with_score.node
            metadata = node.metadata
            title = metadata.get('title', 'Titre inconnu')
            if title not in sources:
                sources[title] = {
                    'author': metadata.get('author', 'Auteur inconnu'),
                    'date': metadata.get('date', 'Date inconnue'),
                    'bio': metadata.get('bio', ''),
                }

        # Afficher les sources dans le format spécifié sans interlignes
        st.subheader("Sources")
        for title, meta in sources.items():
            # Créer une chaîne HTML combinant le titre, la date, l'auteur et la bio
            source_line = f"""
            <p style="margin:0">
                <strong>{title}</strong>, {meta['date']}<br>
                {meta['author']}
            """
            if meta['bio']:
                source_line += f" - <em>{meta['bio']}</em>"
            source_line += "</p>"
            # Afficher la chaîne formatée
            st.markdown(source_line, unsafe_allow_html=True)

        # Ajouter la réponse de l'assistant à l'historique de chat
        st.session_state.messages.append({"role": "assistant", "content": generated_answer})

# Bouton de sortie
if st.button("Quitter"):
    st.write("Session terminée. Actualisez la page pour recommencer.")