FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install flask sklearn numpy
EXPOSE 5001
CMD ["python", "app.py"]