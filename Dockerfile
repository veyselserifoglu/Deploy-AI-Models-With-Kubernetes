# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file first
COPY requirements.txt /app/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the model folder from outside the project
COPY deit-base-distilled-patch16-224 /app/deit-base-distilled-patch16-224

RUN pip install python-multipart

RUN pip install prometheus_client

RUN pip install starlette

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port for FastAPI (default FastAPI port is 8000)
EXPOSE 8000

# Set environment variable for development
ENV ENVIRONMENT=development

# Command to run FastAPI server
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]