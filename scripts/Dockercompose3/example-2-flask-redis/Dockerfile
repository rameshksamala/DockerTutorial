FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy and install dependencies first (Docker layer caching optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Run the Flask app
CMD ["python", "app.py"]
