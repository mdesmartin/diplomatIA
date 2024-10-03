
from llama_index.core import SimpleDirectoryReader

path = "data/"
node_parser = SimpleDirectoryReader(input_dir=path, required_exts=['.pdf'])
documents = node_parser.load_data()
print(documents[0])