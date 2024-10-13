# Dockerfile for the diploRAG project

# Base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Copy .env file
COPY .env .env

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Command to run when the container starts
CMD ["streamlit", "run", "src/chatbot_ui.py"]