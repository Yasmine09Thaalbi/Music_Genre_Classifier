FROM python:3.9-slim

WORKDIR /app
COPY . .


RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --timeout 1000 -r requirements.txt

EXPOSE 5002
CMD ["python", "app.py"]