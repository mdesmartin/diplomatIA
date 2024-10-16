# Dockerfile for the diploRAG project

# Base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ src/

# Copy the .env file if needed
COPY .env .env

# Expose the necessary port
EXPOSE 8501

# Command to run when the container starts
CMD ["streamlit", "run", "src/chatbot_ui.py"]