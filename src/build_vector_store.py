import os
import logging
import faiss
from llama_index.core import VectorStoreIndex, Document, StorageContext, Settings
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore
from dotenv import load_dotenv
from extract_articles import extract_all_articles
from tqdm import tqdm

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def build_vector_store(articles, index_save_path):
	os.makedirs(index_save_path, exist_ok=True)

	embed_model = OpenAIEmbedding()
	Settings.embed_model = embed_model

	text_splitter = TokenTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)

	logging.info("Processing articles and generating embeddings...")
	documents = []
	for article in tqdm(articles, desc="Processing Articles", unit="article"):
		text = article['text']
		title = article['title']
		author = article['author']
		date = article['date']
		bio = article['bio']

		chunks = text_splitter.split_text(text)

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

	dimension = 1536

	faiss_index = faiss.IndexFlatL2(dimension)

	vector_store = FaissVectorStore(faiss_index=faiss_index)

	storage_context = StorageContext.from_defaults(vector_store=vector_store)

	index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)

	faiss_index_path = os.path.join(index_save_path, 'faiss_index.bin')
	faiss.write_index(faiss_index, faiss_index_path)
	logging.info(f"FAISS index saved to {faiss_index_path}")

	index.storage_context.persist(persist_dir=index_save_path)
	logging.info("Database build/update completed successfully.")

if __name__ == "__main__":
	data_dir = 'data/raw'
	index_save_path = 'db'

	articles = extract_all_articles(data_dir)

	build_vector_store(articles, index_save_path)