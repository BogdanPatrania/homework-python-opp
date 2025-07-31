# Use official Python 3.11 image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy project metadata
COPY pyproject.toml ./

# Optional: copy setup.py if using both
COPY setup.py ./

# Install build backend and project dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install .

# Copy the rest of your application code
COPY . .

# Expose port for FastAPI
EXPOSE 8000

# Run FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
