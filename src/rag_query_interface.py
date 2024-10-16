import os
import faiss
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core import Settings
from dotenv import load_dotenv

def load_query_engine(index_save_path: str):
	load_dotenv()
	api_key = os.getenv("OPENAI_API_KEY")
	if api_key is None:
		raise ValueError("OPENAI_API_KEY is not set. Please check your .env file.")
	else:
		print("API Key successfully loaded.")

	embed_model = OpenAIEmbedding()
	Settings.embed_model = embed_model

	faiss_index_path = os.path.join(index_save_path, 'faiss_index.bin')

	faiss_index = faiss.read_index(faiss_index_path)
	print(f"FAISS index loaded from {faiss_index_path}")

	vector_store = FaissVectorStore(faiss_index=faiss_index)

	storage_context = StorageContext.from_defaults(persist_dir=index_save_path, vector_store=vector_store)

	index = load_index_from_storage(storage_context)

	return index.as_query_engine(similarity_top_k=5)

if __name__ == "__main__":
	index_save_path = "db"

	query_engine = load_query_engine(index_save_path)

	def ask_user_query(query_engine) -> None:
		while True:
			user_question = input("Entrez votre question (ou tapez 'exit' pour quitter) : ")
			
			if user_question.lower() == 'exit':
				print("Fermeture de l'interface de requête. Au revoir !")
				break
			
			response = query_engine.query(user_question)
			context = [node.node.text for node in response.source_nodes]
			generated_answer = response.response

			print("\nRéponse :")
			print(generated_answer)

			print("\nDocuments récupérés :")
			for idx, doc in enumerate(context):
				print(f"Document {idx+1}: {doc}\n")