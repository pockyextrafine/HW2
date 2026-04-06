# Use a lightweight python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    HF_HOME=/app/cache/huggingface

# Set working directory
WORKDIR /app

# Install system dependencies (curl for healthchecks if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements to leverage Docker cache
COPY requirements.txt .

# Install dependencies
# Using the CPU-only torch as specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create cache directory for Hugging Face
RUN mkdir -p /app/cache/huggingface && chmod -R 777 /app/cache/huggingface

# Copy the rest of the application
COPY app/ ./app/
COPY static/ ./static/

# Expose the API port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
