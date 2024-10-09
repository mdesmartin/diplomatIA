import logging
from tqdm import tqdm
from typing import List
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.schema import BaseNode, TransformComponent
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core.text_splitter import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
import faiss
import os
import pickle
from dotenv import load_dotenv

# Constants
EMBED_DIMENSION = 512
CHUNK_SIZE = 200
CHUNK_OVERLAP = 50

# Load environment variables from a .env file
load_dotenv()

# Set the OpenAI API key environment variable
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

# Set embedding model on LlamaIndex global settings
Settings.embed_model = OpenAIEmbedding(model="text-embedding-ada-002")

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define the text cleaner class
class TextCleaner(TransformComponent):
    """
    Transformation to be used within the ingestion pipeline.
    Cleans clutters from texts.
    """
    def __call__(self, nodes, **kwargs) -> List[BaseNode]:
        for node in nodes:
            node.text = node.text.replace('\t', ' ')  # Replace tabs with spaces
            node.text = node.text.replace(' \n', ' ')  # Replace paragraph separator with spaces
        return nodes

# Function to build or update the database
def build_database(data_dir: str, faiss_index_path: str, nodes_path: str):
    # Load documents from the specified directory
    logging.info(f"Loading documents from {data_dir}...")
    node_parser = SimpleDirectoryReader(input_dir=data_dir, required_exts=['.pdf'])
    documents = node_parser.load_data()

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
    data_dir = "data/"
    faiss_index_path = "faiss_index.index"
    nodes_path = "nodes.pkl"
    
    # Build or update the database
    build_database(data_dir, faiss_index_path, nodes_path)