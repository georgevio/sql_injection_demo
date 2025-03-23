#!/bin/bash
set -e

# Initialize the database depending on the environment
if [ -z "$DATABASE_URL" ]; then
    echo "No DATABASE_URL found, using SQLite database"
    # SQLite mode - ensure database is initialized
    if [ ! -f "sql_injection_demo.db" ]; then
        echo "Initializing SQLite database..."
        python init_db.py
    fi
else
    echo "DATABASE_URL found, using PostgreSQL database"
    
    # Extract host and port from DATABASE_URL
    if [[ $DATABASE_URL =~ postgresql://[^:]*:[^@]*@([^:]*):([0-9]*)/[a-zA-Z0-9_]* ]]; then
        DB_HOST="${BASH_REMATCH[1]}"
        DB_PORT="${BASH_REMATCH[2]}"
        
        echo "Waiting for PostgreSQL to be ready at $DB_HOST:$DB_PORT..."
        
        # Wait for PostgreSQL to be ready with timeout
        RETRY_COUNT=0
        MAX_RETRIES=30
        until pg_isready -h $DB_HOST -p $DB_PORT -U postgres || [ $RETRY_COUNT -eq $MAX_RETRIES ]; do
            echo "PostgreSQL is unavailable - sleeping (attempt $RETRY_COUNT of $MAX_RETRIES)"
            RETRY_COUNT=$((RETRY_COUNT+1))
            sleep 1
        done
        
        if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
            echo "ERROR: Failed to connect to PostgreSQL after $MAX_RETRIES attempts"
            echo "Check your database connection settings or try the SQLite version:"
            echo "docker-compose -f docker-compose.sqlite.yml up --build"
            exit 1
        fi
        
        echo "PostgreSQL is up - initializing database"
        python init_db.py
    else
        echo "Warning: DATABASE_URL format not recognized, continuing anyway"
        # Try to initialize anyway
        python init_db.py
    fi
fi

# Execute the command provided to the entrypoint
exec "$@"