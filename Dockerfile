FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Upgrade pip permanently
RUN pip install --upgrade pip

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV MONGO_URI=mongodb://mongodb:27017/petcare

# Expose the port the app runs on
EXPOSE 5000

# Run the app using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]