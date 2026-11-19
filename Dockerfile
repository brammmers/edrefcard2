FROM python:3.13-slim

# Install ImageMagick for wand library and gosu for privilege dropping
RUN apt-get update -y \
    && apt-get install -y libmagickwand-dev gosu \
    && apt-get clean -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt constraints.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt -c constraints.txt

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy application code
COPY ./www/ /app/www/
COPY ./bindings/ /app/bindings/

# Copy entrypoint script and strip any Windows CR characters (CRLF -> LF)
# This is required because Docker Desktop on Windows can re-introduce \r during COPY
COPY docker-entrypoint.sh /usr/local/bin/
RUN sed -i 's/\r//' /usr/local/bin/docker-entrypoint.sh \
    && chmod +x /usr/local/bin/docker-entrypoint.sh

# Set work directory to where app.py is
WORKDIR /app/www

# Create configs and data directories
RUN mkdir -p /app/www/configs /app/www/data \
    && chown -R appuser:appuser /app/www/configs /app/www/data \
    && chmod 755 /app/www/configs /app/www/data

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8
# Admin credentials (override these in docker-compose or docker run)
ENV EDREFCARD_ADMIN_USER=admin
ENV EDREFCARD_ADMIN_PASS=changeme
ENV FLASK_SECRET_KEY=change-this-in-production
# Rate-limit counters shared by the gunicorn workers (see www/ratelimit_storage.py)
ENV RATELIMIT_STORAGE_URI=sqlite:////tmp/edrefcard-ratelimit.db

# Container starts as root, entrypoint will fix permissions and drop to appuser
# This is necessary because Docker volumes are mounted as root

# Expose port
EXPOSE 8000

# Use entrypoint to fix permissions then drop privileges
ENTRYPOINT ["docker-entrypoint.sh"]
# --max-requests recycles workers so memory bloated by card rendering is returned
# (a worker reached 1.4 GB on 2026-10-31). When the worker holding scheduler.lock
# is recycled, its replacement takes the lock back at import (see app.py).
# --no-control-socket: gunicorn 26 otherwise tries to create ~/.gunicorn, and appuser has no home.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "--max-requests", "1000", "--max-requests-jitter", "100", "--no-control-socket", "app:app"]
