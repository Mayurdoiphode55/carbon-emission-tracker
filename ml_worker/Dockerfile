FROM python:3.10-slim

WORKDIR /app

# --- add curl for health/debug ---
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app, including the new pipeline folder
COPY . .

# (Optional but explicit) Ensure pipeline is copied inside /app
# This line is redundant if "COPY . ." already includes it,
# but you can keep it for clarity.
COPY ./pipeline /app/pipeline

# Environment + Port
ENV PYTHONUNBUFFERED=1
EXPOSE 9000

# Start the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]
