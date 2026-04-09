FROM python:3.11

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y curl

RUN curl -fsSL https://ollama.com/install.sh | sh

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ollama serve & uvicorn api.index:app --host 0.0.0.0 --port 8000
