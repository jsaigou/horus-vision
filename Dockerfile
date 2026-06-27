# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (gcc, curl if needed, but we keep it lean)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code and data assets
COPY app/ ./app/
COPY data/ ./data/

# Expose port (Cloud Run sets PORT env var automatically)
EXPOSE 8080

# Run the app dynamically using the PORT env var provided by Cloud Run
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
