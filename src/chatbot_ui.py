import streamlit as st
from rag_query_interface import load_query_engine

# Set up page configuration and title
st.set_page_config(page_title="Diplomatic RAG Chatbot", page_icon="🌎", layout="centered", initial_sidebar_state="auto")
st.title("Diplomatic RAG Chatbot 💬🌎")
st.info("Posez n’importe quelle question liée aux enjeux géopolitiques et obtenez des réponses pertinentes basées sur des articles du Monde diplomatique.", icon="📄")

# Define paths for FAISS index and nodes
faiss_index_path = "../db/faiss_index.index"  # Chemin mis à jour vers l'index FAISS
nodes_path = "../db/nodes.pkl"  # Chemin mis à jour vers les nœuds

# Load the query engine
query_engine = load_query_engine(faiss_index_path, nodes_path)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Comment puis-je vous aider aujourd’hui ? Posez n’importe quelle question."}]

# User input area for questions
if prompt := st.chat_input("Posez votre question"):
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Process the user's question and display the answer
if st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant"):
        # Query the engine and get the answer
        response = query_engine.query(st.session_state.messages[-1]["content"])
        generated_answer = response.response
        context = [doc.text for doc in response.source_nodes]

        # Display the generated answer
        st.write(generated_answer)

        # Display retrieved documents
        st.subheader("Sources: (Retrieved Documents)")
        for idx, doc in enumerate(context):
            st.write(f"Document {idx + 1}: {doc}")

        # Append the assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": generated_answer})

# Exit button
if st.button("Quitter"):
    st.write("Session terminée. Actualisez la page pour recommencer.")