# Use the official Python 3.8 base image
FROM python:3.8

# Set the working directory
WORKDIR .

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install Python dependencies and PostgreSQL client
RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get update && \
    apt-get install -y postgresql-client

# Copy the rest of the application code
COPY . .

# Run the command to start your application
CMD ["python", "main.py"]