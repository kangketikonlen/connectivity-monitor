# Base image
FROM python:3.10.9-slim-bullseye

# Set working directory
WORKDIR /app

# Copy project files to the working directory
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port where the app will run
EXPOSE 80

# Start the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
