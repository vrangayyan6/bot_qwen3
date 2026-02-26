# Use a lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend files
COPY backend /app/backend
COPY streamlit_app /app/streamlit_app

# Install backend dependencies
WORKDIR /app/backend
RUN pip install --no-cache-dir .

# Install Streamlit dependencies
WORKDIR /app/streamlit_app
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
