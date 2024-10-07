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

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..'))) # Add the parent directory to the path sicnce we work with notebooks

EMBED_DIMENSION = 512

# Chunk settings are way different than langchain examples
# Beacuse for the chunk length langchain uses length of the string,
# while llamaindex uses length of the tokens
CHUNK_SIZE = 200
CHUNK_OVERLAP = 50

# Load environment variables from a .env file
load_dotenv()

# Set the OpenAI API key environment variable
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

import openai
import os

# Load API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set embeddig model on LlamaIndex global settings
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small", dimensions=EMBED_DIMENSION)


path = "data/"
node_parser = SimpleDirectoryReader(input_dir=path, required_exts=['.pdf'])
documents = node_parser.load_data()
print(documents[0])

# Create FaisVectorStore to store embeddings
faiss_index = faiss.IndexFlatL2(EMBED_DIMENSION)
vector_store = FaissVectorStore(faiss_index=faiss_index)

class TextCleaner(TransformComponent):
    """
    Transformation to be used within the ingestion pipeline.
    Cleans clutters from texts.
    """
    def __call__(self, nodes, **kwargs) -> List[BaseNode]:
        
        for node in nodes:
            node.text = node.text.replace('\t', ' ') # Replace tabs with spaces
            node.text = node.text.replace(' \n', ' ') # Replace paragraph seperator with spacaes
            
        return nodes
    
text_splitter = SentenceSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

print(text_splitter)

# Create a pipeline with defined document transformations and vectorstore
pipeline = IngestionPipeline(
    transformations=[
        TextCleaner(),
        text_splitter,
    ],
    vector_store=vector_store, 
)

# Run pipeline and get generated nodes from the process
nodes = pipeline.run(documents=documents)

vector_store_index = VectorStoreIndex(nodes)
retriever = vector_store_index.as_retriever(similarity_top_k=2)

def show_context(context):
    """
    Display the contents of the provided context list.

    Args:
        context (list): A list of context items to be displayed.

    Prints each context item in the list with a heading indicating its position.
    """
    for i, c in enumerate(context):
        print(f"Context {i+1}:")
        print(c.text)
        print("\n")
        
test_query = "Who are candidates to the US elections?"
context = retriever.retrieve(test_query)
show_context(context)


def ask_user_query(query_engine) -> None:
    """
    Prompt the user for a question, retrieve an answer from the query engine,
    and display the answer and the relevant documents.
    
    Args:
        query_engine: Query engine to process user questions and provide answers.
    """
    
    # Prompt user to enter a question
    user_question = input("Enter your question: ")
    
    # Generate an answer and retrieve documents for the user's question
    response = query_engine.query(user_question)
    context = [doc.text for doc in response.source_nodes]
    generated_answer = response.response

    # Display the generated answer
    print("\nAnswer:")
    print(generated_answer)

    # Display retrieved documents (context)
    print("\nRetrieved Documents:")
    for idx, doc in enumerate(context):
        print(f"Document {idx+1}: {doc}\n")


# Assuming query_engine is defined as before
query_engine = vector_store_index.as_query_engine(similarity_top_k=2)

# Run the program and get the answer for user input
ask_user_query(query_engine)