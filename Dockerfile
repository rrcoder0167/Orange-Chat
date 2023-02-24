# Set the base image to Python 3.10
FROM python:3.10-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for the Flask app
EXPOSE 8080

# Install gunicorn
RUN pip install gunicorn

# Set the entrypoint to the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]

