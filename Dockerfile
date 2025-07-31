# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set work directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code into the container
COPY . .

# Expose the app on port 8000
EXPOSE 8000

# Default command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]