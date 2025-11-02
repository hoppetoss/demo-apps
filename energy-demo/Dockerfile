# 🧩 1. Use an official lightweight Python base image
FROM python:3.11-slim

# 🧩 2. Set working directory inside the container
WORKDIR /app

# 🧩 3. Install system dependencies (optional, but good for builds)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# 🧩 4. Copy requirements first (for build cache efficiency)
COPY requirements.txt .

# 🧩 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 🧩 6. Copy application code
COPY . .

# 🧩 7. Expose FastAPI port
EXPOSE 8080

# 🧩 8. Start FastAPI app with Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]