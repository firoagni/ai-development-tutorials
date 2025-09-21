FROM python:3.11-slim

WORKDIR /app

# Copy requirements.txt and server script
COPY requirements.txt .

RUN pip3 install -r requirements.txt

# Copy the server script
COPY 02_http-mcp-server-fastmcp.py .

# Expose the port the server runs on
EXPOSE 8000

# Command to start the server
CMD ["python3", "02_http-mcp-server-fastmcp.py"] 