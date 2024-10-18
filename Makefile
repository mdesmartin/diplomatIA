IMAGE_NAME = diplorag_image

CONTAINER_NAME = diplorag_container

DB_VOLUME = diplorag_db_volume

DATA_PATH = $(shell pwd)/data

.PHONY: all
all: build run

.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

.PHONY: run
run:
	docker run --rm --name $(CONTAINER_NAME) \
		-v $(DB_VOLUME):/app/db \
		-v "$(DATA_PATH)":/app/data \
		-p 8501:8501 \
		$(IMAGE_NAME) \
		/bin/bash -c "if [ ! -f '/app/db/faiss_index.bin' ]; then python src/build_vector_store.py; fi && streamlit run src/chatbot_ui.py"

.PHONY: rebuild
rebuild:
	docker run --rm --name $(CONTAINER_NAME) \
		-v $(DB_VOLUME):/app/db \
		-v "$(DATA_PATH)":/app/data \
		-p 8501:8501 \
		$(IMAGE_NAME) \
		/bin/bash -c "python src/build_vector_store.py && streamlit run src/chatbot_ui.py"

.PHONY: clean
clean:
	docker rmi $(IMAGE_NAME)

.PHONY: fclean
fclean: clean
	docker rm $(CONTAINER_NAME) || true
	docker volume rm $(DB_VOLUME) || true