# Use a specific version of python image
FROM python:3.9-slim-buster

# Set the working directory
WORKDIR /app

# Copy only the files needed for installing dependencies
COPY requirements.txt .

# Install dependencies and do not create a cache
RUN pip install --user --no-cache-dir -r requirements.txt

# Update the PATH environment variable to include /root/.local/bin
ENV PATH=/root/.local/bin:$PATH

# Copy the rest of the files
COPY . .

# Run the application
CMD ["sh", "/app/run_app.sh"]
