# diplomatIA

![Licence](https://img.shields.io/badge/licence-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)
![Docker](https://img.shields.io/badge/docker-20.10%2B-blue.svg)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
	- [Prerequisites](#prerequisites)
	- [Using the Makefile](#using-the-makefile)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Contribution](#contribution)
- [License](#license)
- [Contact](#contact)

## Overview

**diplomatIA** is a personal project aimed at developing an intelligent diplomatic agent using Retrieval-Augmented Generation (RAG). This agent leverages a vector database of articles from a specialized geopolitical journal to provide informed responses to user questions, accompanied by source citations.

## Features

- **Retrieval-Augmented Generation (RAG):** Combines generative AI with a retrieval system for accurate and contextually relevant responses.
- **Vector Database with FAISS:** Efficiently indexes a large corpus of diplomatic articles for quick searching.
- **Automated Data Pipeline:** Extraction, normalization, and indexing of EPUB articles for seamless updates.
- **Interactive Interface with Streamlit:** User-friendly interface allowing intuitive interaction with the diplomatic agent.
- **Dockerized Deployment:** Ensures portability and ease of deployment across different environments.
- **Automation via Makefile:** Simplifies build, execution, and maintenance tasks with predefined targets.

## Architecture

	diplomatIA/
	├── Dockerfile
	├── Makefile
	├── README.md
	├── data
	│   ├── extracted_epubs
	│   └── raw
	│       ├── Le-Journal-Geopolitique-2019-01.epub
	│       ├── …
	│       └── Le-Journal-Geopolitique-2024-10.epub
	├── requirements.txt
	└── src
		├── build_vector_store.py
		├── chatbot_ui.py
		├── extract_articles.py
		└── rag_query_interface.py

## Installation

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed.
- [Make](https://www.gnu.org/software/make/) installed.
- [Git](https://git-scm.com/) installed.

### Using the Makefile

The project includes a `Makefile` to automate common tasks such as building the Docker image, running the container, rebuilding the vector database, and cleaning up resources.

### Makefile Targets

- `all`: Builds and runs the Docker container.
- `build`: Builds the Docker image.
- `run`: Runs the Docker container, initializing the vector database if it does not exist.
- `rebuild`: Rebuilds the vector database and restarts the application.
- `clean`: Removes the Docker image.
- `fclean`: Removes the Docker image, container, and associated Docker volume.

#### Installation Steps

**1. Clone the Repository**

	git clone https://github.com/mdesmartin/diplomatIA.git
	cd diplomatIA

**2. Configure Environment Variables**

Create a .env file at the root of the project and add your OpenAI API key:

	OPENAI_API_KEY=your_openai_api_key

**3. Place the EPUB Files**

Ensure that all EPUB files from the geopolitical journal are placed in the data/raw directory.

**4. Build and Run with the Makefile**

• Build the Docker Image

	make build

• Run the Docker Container

	make run

This command will perform the following actions:
• Mount the data directory and a Docker volume for the database.

• Build the FAISS database if it does not exist.

• Launch the Streamlit application accessible at http://localhost:8501.

• Rebuild the Vector Database

	make rebuild

This command forces the reconstruction of the FAISS index and restarts the Streamlit application.

• Clean Docker Resources

	make clean

Removes the Docker image.

	make fclean

Removes the Docker image, container, and associated Docker volume.

## Usage

**1. Access the Application**

Open your web browser and navigate to http://localhost:8501.

**2. Interact with the Diplomatic Agent**

• Enter your questions related to geopolitical issues.
	
• Receive detailed responses based on articles from the geopolitical journal.
	
• View cited sources for each response.

**3. Exit the Application**

Click the “Quit” button in the Streamlit interface to end the session.

## Project Structure

•	**Dockerfile:** Defines the Docker image for the application.

•	**Makefile:** Contains build and execution commands to simplify usage.

•	**data/raw:** Contains raw EPUB files from the geopolitical journal.

•	**data/extracted_epubs:** Stores the extracted and processed content from EPUBs.

•	**src/build_vector_store.py:** Builds the FAISS vector database from extracted articles.

•	**src/extract_articles.py:** Extracts and preprocesses articles from EPUB files.

•	**src/rag_query_interface.py:** Manages the RAG query engine.

•	**src/chatbot_ui.py:** Implements the Streamlit-based user interface.

•	**requirements.txt:** Lists the necessary Python dependencies.

## Technologies

•	**Python 3.11:** Main programming language.

•	**FAISS:** Vector database for efficient similarity searches.

•	**LlamaIndex:** Manages embeddings and query interfaces.

•	**Streamlit:** Creates the interactive web interface.

•	**Docker:** Containerizes the application for enhanced portability.

•	**BeautifulSoup:** Parses and extracts data from EPUB files.

•	**OpenAI API:** Powers the generative AI capabilities.

## Contribution

Contributions are welcome! Please follow these steps:

1. Fork the Repository

2. Create a Feature Branch

		git checkout -b feature/yourFeature


3.	Commit Your Changes

		git commit -m "Add your feature"

4.	Push the Branch

		git push origin feature/yourFeature

5.	Open a Pull Request
	
	Ensure that your code adheres to project standards and includes appropriate tests.

## License

This project is licensed under the MIT License.

## Contact

**Author:** Mehdi DESMARTIN

**LinkedIn:** linkedin.com/in/mdesmartin

**GitHub:** github.com/mdesmartin