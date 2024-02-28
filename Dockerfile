FROM python:3.9.0-slim

WORKDIR /app
RUN pip install poetry
COPY . /app
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN python install_dep.py
CMD ["streamlit", "run", "--server.port=8000", "sentiment-analysis-text.py"]
