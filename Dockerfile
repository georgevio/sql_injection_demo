FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY docker-requirements.txt .
RUN pip install --no-cache-dir -r docker-requirements.txt

COPY . .

# Set environment variables
ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Create SQLite database in SQLite mode if no PostgreSQL URL is provided
# The actual initialization will happen at runtime to support both database types
RUN if [ -z "$DATABASE_URL" ]; then python init_db.py; fi

# Expose port 5000
EXPOSE 5000

# Add entrypoint script to check database and start app
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Run the entrypoint script
ENTRYPOINT ["docker-entrypoint.sh"]

# Default command if no command is provided
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-", "main:app"]