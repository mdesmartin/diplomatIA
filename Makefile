# Variables
IMAGE_NAME = diplorag_image
CONTAINER_NAME = diplorag_container
DB_PATH_INDEX = /app/db/faiss_index.bin  # Chemin vers le fichier d'index FAISS

# Default target
.PHONY: all
all: build run

# Build Docker image and install requirements
.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

# Run the chatbot only if the DB files exist
.PHONY: run
run:
	docker run --rm --name $(CONTAINER_NAME) -v "$(shell pwd)":/app -p 8501:8501 $(IMAGE_NAME) /bin/bash -c "if [ ! -f '$(DB_PATH_INDEX)' ]; then python src/build_vector_store.py; fi && streamlit run src/chatbot_ui.py"

# Rebuild the database
.PHONY: rebuild
rebuild:
	docker run --rm --name $(CONTAINER_NAME) -v "$(shell pwd)":/app -p 8501:8501 $(IMAGE_NAME) /bin/bash -c "python src/build_vector_store.py && streamlit run src/chatbot_ui.py"

# Clean up
.PHONY: clean
clean:
	docker rmi $(IMAGE_NAME)

# Force clean up
.PHONY: fclean
fclean: clean
	docker rm $(CONTAINER_NAME) || true