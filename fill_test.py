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
import sys
from dotenv import load_dotenv

# Add the parent directory to the path for importing any other files if necessary
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..')))

# Dimension size for embeddings
EMBED_DIMENSION = 512

# Chunk settings for text splitting
CHUNK_SIZE = 200
CHUNK_OVERLAP = 50

# Load environment variables from a .env file
load_dotenv()

# Set the OpenAI API key environment variable
api_key = os.getenv('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = api_key

# Check if the OpenAI key is loaded correctly
print(f"OpenAI API Key Loaded: {api_key[:5]}...")  # Print first 5 characters of the key for privacy

import openai

# Load API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Verify OpenAI connection by performing a simple request (optional but useful for troubleshooting)
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt="This is a test to check OpenAI API connection.",
    max_tokens=5
)
print(f"Test OpenAI Response: {response.choices[0].text.strip()}")

# Set embedding model on LlamaIndex global settings
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small", dimensions=EMBED_DIMENSION)

# Directory containing the documents
path = "data/"

# Step 1: Load and print documents
node_parser = SimpleDirectoryReader(input_dir=path, required_exts=['.pdf'])
documents = node_parser.load_data()

# Print the first document loaded
print(f"Document Loaded: {documents[0]}")

# Step 2: Create FAISS Vector Store
faiss_index = faiss.IndexFlatL2(EMBED_DIMENSION)
vector_store = FaissVectorStore(faiss_index=faiss_index)

# Print a message after FAISS vector store creation
print(f"FAISS Vector Store created with embedding dimension {EMBED_DIMENSION}")

# Step 3: Create TextCleaner class to clean text and print the transformation
class TextCleaner(TransformComponent):
    """
    Transformation to be used within the ingestion pipeline.
    Cleans clutters from texts.
    """
    def __call__(self, nodes, **kwargs) -> List[BaseNode]:
        for node in nodes:
            # Clean text by replacing unwanted characters
            node.text = node.text.replace('\t', ' ') # Replace tabs with spaces
            node.text = node.text.replace(' \n', ' ') # Replace paragraph separator with spaces
        return nodes

# Step 4: Text splitting setup
text_splitter = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

# Print the text splitter settings to verify
print(f"TextSplitter created with CHUNK_SIZE: {CHUNK_SIZE} and CHUNK_OVERLAP: {CHUNK_OVERLAP}")

# Create the ingestion pipeline
pipeline = IngestionPipeline(
    transformations=[
        TextCleaner(),
        text_splitter,
    ],
    vector_store=vector_store, 
)

# Run the pipeline and get the nodes, print output
nodes = pipeline.run(documents=documents)

# Print nodes created (print only the first node for brevity)
if nodes:
    print(f"First node text: {nodes[0].text[:200]}...")  # Print first 200 characters of the first node text
else:
    print("No nodes created!")

# Step 5: Index the nodes into the vector store
vector_store_index = VectorStoreIndex(nodes)

# Step 6: Set up retriever to test retrieval
retriever = vector_store_index.as_retriever(similarity_top_k=2)

# Test the retrieval with a query
test_query = "What is the main cause of climate change?"

# Retrieve the context from the indexed nodes
context = retriever.retrieve(test_query)

# Print the retrieved context
for i, ctx in enumerate(context):
    print(f"Context {i+1}: {ctx.text[:200]}...")  # Print first 200 characters for brevity