# Use an official Python runtime as the base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Set the working directory in the container
WORKDIR /backend

# Copy the requirements.txt file to the container
COPY ./requirements.txt /backend/requirements.txt

# Install the Python dependencies
RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

# Copy the FastAPI application code to the container
COPY ./app /backend/app

# Define the command to run the FastAPI application using uvicorn
CMD ["python3", "app/main.py"]
