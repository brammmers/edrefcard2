#!/bin/bash
# Entrypoint script that fixes permissions before starting the app

# Fix ownership of configs directory if running as root
if [ "$(id -u)" = "0" ]; then
    echo "Running as root, fixing permissions on /app/www/configs..."
    chown -R appuser:appuser /app/www/configs
    chown -R appuser:appuser /app/www/data 2>/dev/null || true
    echo "Permissions fixed, switching to appuser..."
    exec gosu appuser "$@"
else
    echo "Running as $(whoami), starting application..."
    exec "$@"
fi
