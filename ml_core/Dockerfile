FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# We copy the rest of the code, but we also mount it in docker-compose for dev
COPY . .

CMD ["python", "main.py"]
