# build_vector_store.py

import os
import logging
import faiss  # Import FAISS
from llama_index.core import VectorStoreIndex, Document, StorageContext, Settings
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore
from dotenv import load_dotenv
from extract_articles import extract_all_articles  # Import depuis le premier script
from tqdm import tqdm

# Charger les variables d'environnement depuis un fichier .env
load_dotenv()

# Définir la clé API OpenAI
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

# Constantes
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Configuration du logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def build_vector_store(articles, index_save_path):
    # S'assurer que le répertoire de sortie existe
    os.makedirs(index_save_path, exist_ok=True)

    # Initialiser le modèle d'embedding et le définir dans les paramètres
    embed_model = OpenAIEmbedding()
    Settings.embed_model = embed_model

    # Initialiser le découpeur de texte
    text_splitter = TokenTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

    # Traiter les articles et construire l'index
    logging.info("Processing articles and generating embeddings...")
    documents = []
    for article in tqdm(articles, desc="Processing Articles", unit="article"):
        text = article['text']
        title = article['title']
        author = article['author']
        date = article['date']
        bio = article['bio']

        # Découper le texte en chunks
        chunks = text_splitter.split_text(text)

        # Créer des documents avec des métadonnées
        for chunk in chunks:
            doc = Document(
                text=chunk,
                metadata={
                    'title': title,
                    'author': author,
                    'date': date,
                    'bio': bio
                }
            )
            documents.append(doc)

    # Manuellement définir la dimension des embeddings
    dimension = 1536  # Pour le modèle text-embedding-ada-002

    # Créer un index FAISS avec distance L2
    faiss_index = faiss.IndexFlatL2(dimension)  # Index utilisant la distance L2

    # Créer un FaissVectorStore avec l'index FAISS
    vector_store = FaissVectorStore(faiss_index=faiss_index)

    # Créer un StorageContext avec le vector_store
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    # Créer l'index en utilisant les documents et le storage_context
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

    # Sauvegarder l'index FAISS binaire
    faiss_index_path = os.path.join(index_save_path, 'faiss_index.bin')
    faiss.write_index(faiss_index, faiss_index_path)
    logging.info(f"FAISS index saved to {faiss_index_path}")

    # Sauvegarder l'index complet (documents, métadonnées, etc.)
    index.storage_context.persist(persist_dir=index_save_path)
    logging.info("Database build/update completed successfully.")

if __name__ == "__main__":
    data_dir = 'data/raw'
    index_save_path = 'db'

    # Extraire les articles directement
    articles = extract_all_articles(data_dir)

    # Construire le vector store
    build_vector_store(articles, index_save_path)