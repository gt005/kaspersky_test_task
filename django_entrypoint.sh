#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python kaspersky_file_api/manage.py migrate

# Start Supervisor
echo "Starting Supervisor..."
exec supervisord -c supervisord.conf
