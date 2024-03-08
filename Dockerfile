# Use Alpine Linux with Python 3 as base image
FROM python:3.9.18-alpine3.19

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy the current directory contents into the container at /app
COPY books/ /app/books
COPY main.py /app

# Expose port 8000
EXPOSE 5000

# Command to run the Flask application with Gunicorn
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "main:app"]
