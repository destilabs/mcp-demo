FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port the app will run on
EXPOSE 8000

# Command to run the application
# CMD ["uvicorn", "calculator-server:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "server.py"]

