# query_interface.py

import pickle
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import VectorStoreIndex
import faiss

def load_query_engine(faiss_index_path: str, nodes_path: str):
    # Load FAISS index
    faiss_index = faiss.read_index(faiss_index_path)
    vector_store = FaissVectorStore(faiss_index=faiss_index)
    
    # Load nodes
    with open(nodes_path, 'rb') as f:
        nodes = pickle.load(f)

    # Create the VectorStoreIndex from the loaded FAISS index and nodes
    index = VectorStoreIndex(nodes)
    
    # Create and return a query engine from the index
    return index.as_query_engine(similarity_top_k=5)

def ask_user_query(query_engine) -> None:
    """
    Continuously prompt the user for questions, retrieve answers from the query engine,
    and display the answers and the relevant documents until the user decides to exit.
    
    Args:
        query_engine: Query engine to process user questions and provide answers.
    """
    while True:
        # Prompt user to enter a question
        user_question = input("Enter your question (or type 'exit' to quit): ")
        
        # Exit if user types 'exit'
        if user_question.lower() == 'exit':
            print("Exiting the query interface. Goodbye!")
            break
        
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

if __name__ == "__main__":
    faiss_index_path = "faiss_index.index"
    nodes_path = "nodes.pkl"

    # Load the query engine
    query_engine = load_query_engine(faiss_index_path, nodes_path)

    # Interact with the user
    ask_user_query(query_engine)