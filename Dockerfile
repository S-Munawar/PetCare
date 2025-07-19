# Use a specific version for deterministic builds
FROM python:3.9.18-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Copy only the requirements file to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root user for security
RUN addgroup --system nonroot && adduser --system --ingroup nonroot nonroot
USER nonroot

# Copy the rest of the application code
COPY . .

# Environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
# MONGO_URI should be provided at runtime, not hardcoded here

# Expose the port the app runs on
EXPOSE 5000

# Run the app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]