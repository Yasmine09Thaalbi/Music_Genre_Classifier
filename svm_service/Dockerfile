FROM python:3.9-slim

WORKDIR /app
COPY . .


RUN apt-get update && apt-get install -y 


RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "app.py"]
