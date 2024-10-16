import os
from dotenv import load_dotenv
import streamlit as st
from rag_query_interface import load_query_engine

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
	raise ValueError("OPENAI_API_KEY is not set. Please check your .env file.")
else:
	print("API Key successfully loaded.")

st.set_page_config(page_title="diplomatIA", page_icon="🌎", layout="centered", initial_sidebar_state="auto")
st.title("diplomatIA 🌎")
st.info("Posez n’importe quelle question liée aux enjeux géopolitiques et obtenez des réponses pertinentes basées sur des articles du Monde diplomatique.", icon="💬")

index_save_path = "db"

query_engine = load_query_engine(index_save_path)

if "messages" not in st.session_state:
	st.session_state.messages = [{"role": "assistant", "content": "Comment puis-je vous aider aujourd’hui ? Posez n’importe quelle question."}]

if prompt := st.chat_input("Posez votre question"):
	st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:
	with st.chat_message(message["role"]):
		st.write(message["content"])

if st.session_state.messages[-1]["role"] == "user":
	with st.chat_message("assistant"):
		response = query_engine.query(st.session_state.messages[-1]["content"])
		generated_answer = response.response

		st.write(generated_answer)

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

		st.subheader("Sources")
		for title, meta in sources.items():
			source_line = f"""
			<p style="margin:0">
				<strong>{title}</strong>, {meta['date']}<br>
				{meta['author']}
			"""
			if meta['bio']:
				source_line += f" - <em>{meta['bio']}</em>"
			source_line += "</p>"
			st.markdown(source_line, unsafe_allow_html=True)

		st.session_state.messages.append({"role": "assistant", "content": generated_answer})

if st.button("Quitter"):
	st.write("Session terminée. Actualisez la page pour recommencer.")