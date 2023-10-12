FROM python:3.9

# Install dependencies
RUN pip install psycopg2-binary python-dotenv
RUN pip install psycopg2-binary

# Copy files into the container
COPY ./your_python_script.py /app/your_python_script.py
COPY your_python_script.py .env ./

# Run your Python script
CMD ["python", "/app/your_python_script.py"]