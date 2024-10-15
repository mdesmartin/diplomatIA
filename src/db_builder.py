# db_builder.py

import os
import logging
from tqdm import tqdm
from typing import List
from llama_index.core import VectorStoreIndex
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.schema import TextNode, TransformComponent
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core.text_splitter import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
import faiss
import pickle
from dotenv import load_dotenv
import pdfplumber
import re

# Constants
EMBED_DIMENSION = 512
CHUNK_SIZE = 600
CHUNK_OVERLAP = 200

# Load environment variables from a .env file
load_dotenv()

# Set the OpenAI API key environment variable
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

# Set embedding model on LlamaIndex global settings
Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Function to extract text from a PDF using pdfplumber
def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            full_text += text if text else ""
    return full_text

# Custom class to clean and normalize text
class TextCleaner(TransformComponent):
    """
    Transformation to be used within the ingestion pipeline.
    Cleans clutters from texts and ensures proper spacing.
    """
    def __call__(self, nodes, **kwargs) -> List[TextNode]:
        for node in nodes:
            print("Texte avant nettoyage:", node.text[:500])  # Avant nettoyage
            # Replace multiple spaces with a single space
            node.text = re.sub(r'\s+', ' ', node.text)
            # Add space between words that were joined (e.g., between a lowercase and an uppercase)
            node.text = re.sub(r'(\w)([A-Z])', r'\1 \2', node.text)
            print("Texte après nettoyage:", node.text[:500])  # Après nettoyage
        return nodes

# Function to build or update the database
def build_database(data_dir: str, faiss_index_path: str, nodes_path: str):
    # Ensure the output directory exists
    output_dir = os.path.dirname(faiss_index_path)
    os.makedirs(output_dir, exist_ok=True)

    # Load PDF files and extract text
    logging.info(f"Loading documents from {data_dir}...")
    documents = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".pdf"):
            file_path = os.path.join(data_dir, filename)
            logging.info(f"Extracting text from {file_path}...")
            extracted_text = extract_text_from_pdf(file_path)
            documents.append(TextNode(text=extracted_text))
            print("Texte extrait du PDF:", extracted_text[:1000])  # Afficher les 1000 premiers caractères

    logging.info(f"Loaded {len(documents)} documents.")

    # Initialize FAISS vector store
    if os.path.exists(faiss_index_path):
        logging.info(f"Loading existing FAISS index from {faiss_index_path}...")
        faiss_index = faiss.read_index(faiss_index_path)
    else:
        logging.info("Creating new FAISS index...")
        faiss_index = faiss.IndexFlatL2(EMBED_DIMENSION)

    vector_store = FaissVectorStore(faiss_index=faiss_index)
    
    # Define the ingestion pipeline
    text_splitter = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    pipeline = IngestionPipeline(
        transformations=[TextCleaner(), text_splitter],
        vector_store=vector_store
    )

    # Run the pipeline to generate nodes from documents with a progress bar
    logging.info("Processing documents and generating embeddings...")
    nodes = []
    for document in tqdm(documents, desc="Processing Documents", unit="doc"):
        document_nodes = pipeline.run(documents=[document])
        nodes.extend(document_nodes)
        print("Texte à indexer dans FAISS:", document_nodes[0].text[:500])  # Afficher les premiers chunks traités

    logging.info("Finished processing documents.")

    # Save FAISS index after updating
    logging.info(f"Saving FAISS index to {faiss_index_path}...")
    faiss.write_index(faiss_index, faiss_index_path)

    # Save the nodes to a file (for later retrieval)
    logging.info(f"Saving nodes to {nodes_path}...")
    with open(nodes_path, 'wb') as f:
        pickle.dump(nodes, f)

    logging.info("Database build/update completed successfully.")

    # Return the VectorStoreIndex for later use
    return VectorStoreIndex(nodes)

if __name__ == "__main__":
    data_dir = "/app/data/"
    faiss_index_path = "/app/db/faiss_index.index"
    nodes_path = "/app/db/nodes.pkl"
    
    # Build or update the database
    build_database(data_dir, faiss_index_path, nodes_path)