# Use the official Python 3.11 image as the base image
FROM python:3.11

# Install Poetry
RUN pip install poetry

# Set the working directory in the container
WORKDIR /app

# Copy the poetry.lock and pyproject.toml files to the container
COPY poetry.lock pyproject.toml /app/

# Install the project dependencies
RUN poetry install --no-root

# Copy the rest of the application code to the container
COPY . /app

# Save the generated database files to a specific location
VOLUME /app/db

# Expose port 8000
EXPOSE 8000

# Set the entrypoint command to run the application
CMD ["poetry", "run", "python", "app.py"]
