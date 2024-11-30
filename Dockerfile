# Use the official Python image from AWS Public ECR
FROM public.ecr.aws/docker/library/python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY app/ /app/

# Install required Python packages
RUN pip install flask requests

# Expose the port for the application
EXPOSE 8080

# Run the Flask app
CMD ["python", "app.py"]
