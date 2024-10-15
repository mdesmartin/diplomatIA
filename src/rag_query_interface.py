# rag_query_interface.py

import os
import faiss
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import Settings
from dotenv import load_dotenv

def load_query_engine(index_save_path: str):
    # Charger les variables d'environnement
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("OPENAI_API_KEY is not set. Please check your .env file.")
    else:
        print("API Key successfully loaded.")

    # Définir le modèle d'embedding dans les paramètres
    embed_model = OpenAIEmbedding()
    Settings.embed_model = embed_model

    # Chemin vers le fichier de l'index FAISS
    faiss_index_path = os.path.join(index_save_path, 'faiss_index.bin')

    # Charger l'index FAISS binaire
    faiss_index = faiss.read_index(faiss_index_path)
    print(f"FAISS index loaded from {faiss_index_path}")

    # Créer un FaissVectorStore avec l'index chargé
    vector_store = FaissVectorStore(faiss_index=faiss_index)

    # Créer un StorageContext avec le vector_store et le répertoire de persistance
    storage_context = StorageContext.from_defaults(persist_dir=index_save_path, vector_store=vector_store)

    # Charger l'index depuis le storage_context
    index = load_index_from_storage(storage_context)

    # Créer et retourner un query engine à partir de l'index
    return index.as_query_engine(similarity_top_k=5)

if __name__ == "__main__":
    index_save_path = "db"  # Chemin vers le répertoire contenant les fichiers d'index

    # Charger le query engine
    query_engine = load_query_engine(index_save_path)

    def ask_user_query(query_engine) -> None:
        """
        Pose des questions à l'utilisateur en continu, récupère les réponses du query engine,
        et affiche les réponses ainsi que les documents pertinents jusqu'à ce que l'utilisateur décide de quitter.
        """
        while True:
            # Demander à l'utilisateur d'entrer une question
            user_question = input("Entrez votre question (ou tapez 'exit' pour quitter) : ")
            
            # Quitter si l'utilisateur tape 'exit'
            if user_question.lower() == 'exit':
                print("Fermeture de l'interface de requête. Au revoir !")
                break
            
            # Générer une réponse et récupérer les documents pour la question de l'utilisateur
            response = query_engine.query(user_question)
            context = [node.node.text for node in response.source_nodes]
            generated_answer = response.response

            # Afficher la réponse générée
            print("\nRéponse :")
            print(generated_answer)

            # Afficher les documents récupérés (contexte)
            print("\nDocuments récupérés :")
            for idx, doc in enumerate(context):
                print(f"Document {idx+1}: {doc}\n")