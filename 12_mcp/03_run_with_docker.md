
# MCP Server with Docker

Demonstrating how to containerize an MCP server using Docker.

## Prerequisites

Docker installed and running on your system

## Files

- `02_http-mcp-server-fastmcp.py`: The MCP server implementation
- `requirements.txt`: Python dependencies for the mcp server
- `Dockerfile`: Instructions for building the Docker image

## Running with Docker

### Step 1: Build the Docker image

```bash
docker build -t build-server-http:latest .
```

### Step 2: Run the Docker container

```bash
docker run -p 8000:8000 build-server-http:latest
```
This will start the MCP server inside a Docker container and expose it on port 8000.

Open your browser and navigate to `http://localhost:8000/mcp` and check if you are getting any response.

### Troubleshooting

If you encounter connection issues:

1. **Check if the server is running**: Make sure the Docker container is running with `docker ps`.

2. **Verify port mapping**: Ensure the port is correctly mapped with `docker ps` or by checking the output of the `docker run` command.

3. **Check server logs**: View the server logs with `docker logs <container_id>` to see if there are any errors.

4. **Host binding**: The server is configured to bind to `0.0.0.0` instead of `127.0.0.1` to make it accessible from outside the container. If you're still having issues, you might need to check your firewall settings.

5. **Network issues**: If you're running Docker on a remote machine, make sure the port is accessible from your client machine.