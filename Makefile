# Variables

# Nom de l'image Docker
IMAGE_NAME = diplorag_image

# Nom du conteneur Docker
CONTAINER_NAME = diplorag_container

# Nom du volume Docker pour la DB
DB_VOLUME = diplorag_db_volume

# Chemin vers le répertoire data sur l'hôte
DATA_PATH = $(shell pwd)/data

# Default target
.PHONY: all
all: build run

# Build Docker image
.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

# Run the chatbot, build the DB if it doesn't exist
.PHONY: run
run:
	docker run --rm --name $(CONTAINER_NAME) \
		-v $(DB_VOLUME):/app/db \
		-v "$(DATA_PATH)":/app/data \
		-p 8501:8501 \
		$(IMAGE_NAME) \
		/bin/bash -c "if [ ! -f '/app/db/faiss_index.bin' ]; then python src/build_vector_store.py; fi && streamlit run src/chatbot_ui.py"

# Rebuild the database
.PHONY: rebuild
rebuild:
	docker run --rm --name $(CONTAINER_NAME) \
		-v $(DB_VOLUME):/app/db \
		-v "$(DATA_PATH)":/app/data \
		-p 8501:8501 \
		$(IMAGE_NAME) \
		/bin/bash -c "python src/build_vector_store.py && streamlit run src/chatbot_ui.py"

# Clean up
.PHONY: clean
clean:
	docker rmi $(IMAGE_NAME)

# Force clean up
.PHONY: fclean
fclean: clean
	docker rm $(CONTAINER_NAME) || true
	docker volume rm $(DB_VOLUME) || true