# Use a specific version of python image
FROM python:3.9-slim-buster as builder

# Set the working directory
WORKDIR /app

# Copy only the files needed for installing dependencies
COPY requirements.txt .

# Install dependencies and do not create a cache
RUN pip install --user --no-cache-dir -r requirements.txt

# Start a new stage from the same base image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Update the PATH environment variable to include /root/.local/bin
ENV PATH=/root/.local/bin:$PATH

# Copy only the files needed from the builder stage
COPY --from=builder /root/.local /root/.local

# Copy the rest of the files
COPY . .

# Run the application
CMD ["sh", "/app/run_app.sh"]
