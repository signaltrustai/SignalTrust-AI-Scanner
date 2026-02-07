FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY supervisor.py .
COPY auto_gpt.cfg .

# Create workspace directory
RUN mkdir -p /app/workspace

# Run the supervisor
CMD ["python", "supervisor.py"]
