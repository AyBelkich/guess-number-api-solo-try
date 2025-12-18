# 1. Base image: lightweight Python image
FROM python:3.11-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy requirements and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of the application code
COPY . .

# 5. Expose the port (for documentation / clarity)
EXPOSE 8000

# 6. Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
