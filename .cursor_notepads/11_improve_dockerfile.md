# Improving the Dockerfile

## Problem
The current Dockerfile needs improvements for production readiness, including:
- Multi-stage builds to reduce image size
- Running as non-root user
- Proper Uvicorn worker configuration
- Better security practices

## Solution Steps

1. **Implement Multi-stage Build**:
   - Create a builder stage for dependencies
   - Create a runtime stage for the application
   - Copy only necessary files

2. **Add Security Improvements**:
   - Create and use non-root user
   - Set proper file permissions
   - Use specific base image versions

3. **Optimize Uvicorn Configuration**:
   - Configure proper number of workers
   - Add health check
   - Set proper timeouts

## Implementation Details

### Updated Dockerfile:
```dockerfile
# Builder stage
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd -m -u 1000 appuser

# Set work directory
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages/ /usr/local/lib/python3.11/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application code
COPY --chown=appuser:appuser app ./app
COPY --chown=appuser:appuser prompt ./prompt

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Start FastAPI with Uvicorn
CMD ["uvicorn", "app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8080", \
     "--workers", "4", \
     "--timeout-keep-alive", "75", \
     "--log-level", "info"]
```

## Key Improvements

1. **Multi-stage Build**:
   - Reduces final image size by excluding build dependencies
   - Separates build environment from runtime environment

2. **Security**:
   - Creates and uses non-root user `appuser`
   - Sets proper file permissions
   - Uses specific Python version

3. **Performance**:
   - Configures 4 Uvicorn workers (adjust based on CPU cores)
   - Sets proper timeouts and keep-alive settings
   - Enables logging

4. **Monitoring**:
   - Adds health check endpoint
   - Configures proper logging level

## Testing

1. **Build the Image**:
```bash
docker build -t review-summarizer .
```

2. **Run the Container**:
```bash
docker run -d -p 8080:8080 --name review-summarizer review-summarizer
```

3. **Verify Health Check**:
```bash
curl http://localhost:8080/health
```

## Notes
- Adjust the number of workers based on your deployment environment
- Consider adding environment variable configuration
- The health check assumes the `/health` endpoint is available
- Consider adding Docker Compose for local development 