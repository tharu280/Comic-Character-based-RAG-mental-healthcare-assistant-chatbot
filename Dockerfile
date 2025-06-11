# Use Python 3.12.5 slim image
FROM python:3.12.5-slim

# Set working directory in container
WORKDIR /app

# Install build essentials (sometimes needed for native dependencies)
RUN apt-get update && apt-get install -y build-essential

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code, .env, and vdbs folder
COPY fast.py .
COPY .env .
COPY vdbs ./vdbs

# Expose port 8000
EXPOSE 8000

# Command to run the app with uvicorn
CMD ["uvicorn", "fast:app", "--host", "0.0.0.0", "--port", "8000"]
