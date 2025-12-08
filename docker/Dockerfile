# ===== BASE BUILD STAGE =====
FROM python:3.13-slim AS builder

WORKDIR /app

# Python optimizations
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies for building packages
RUN apt-get update && \
    apt-get install -y build-essential graphviz libgraphviz-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ===== PRODUCTION STAGE =====
FROM python:3.13-slim

# Install runtime libraries for Graphviz
RUN apt-get update && \
    apt-get install -y graphviz libgraphviz-dev && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user and project folder
RUN useradd -m -r appuser && mkdir /app
WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy project files
COPY bcs/ .

# Make entrypoint executable
RUN chmod +x entrypoint.prod.sh

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Start application
CMD ["./entrypoint.prod.sh"]
