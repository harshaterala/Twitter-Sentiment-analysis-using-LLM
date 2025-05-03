# Use a slightly larger base image with common dependencies
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt /app/

# Install system dependencies (add more if needed)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app/

# Expose the necessary port (if running a web app)
EXPOSE 8501

# Set the default command
CMD ["streamlit", "run", "app.py"]  