# Use official Python image as base
FROM python:3.10-slim

# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1 \
#     PYTHONUNBUFFERED=1 \
#     GOOGLE_GENAI_USE_VERTEXAI=FALSE \
#     GOOGLE_API_KEY="AIzaSyBysUF7hKW6K4eXOGcHJ3g4TU"

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Start FastAPI server
CMD ["uvicorn", "src.main.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
