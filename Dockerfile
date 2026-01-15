# Use an official Python runtime as a parent image
FROM python:3.14.2-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory to /app
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy the project configuration
COPY pyproject.toml .

# Install dependencies
# We use --no-dev to exclude development dependencies (like pytest)
# We use --no-install-project because we configured package=false in pyproject.toml
RUN uv sync --no-install-project --no-dev

# Create the directory structure for the package
RUN mkdir -p packages/server_python

# Copy the current directory contents into the container at /app/packages/server_python
COPY . packages/server_python/

# Set PYTHONPATH so python can find the 'packages' module
ENV PYTHONPATH=/app

# Make sure we use the virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# Expose port (9001 is the default game port)
EXPOSE 9001

# Run the server using uvicorn
CMD ["uvicorn", "packages.server_python.main:app", "--host", "0.0.0.0", "--port", "9001"]
