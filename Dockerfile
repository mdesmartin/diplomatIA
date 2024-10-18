FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

COPY .env .env

EXPOSE 8501

CMD ["streamlit", "run", "src/chatbot_ui.py"]