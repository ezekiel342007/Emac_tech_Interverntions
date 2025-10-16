#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status.
set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

# 2. Run migrations
python manage.py migrate

# 3. Collect static files
python manage.py collectstatic --no-input

# 4. Create superuser (Non-interactive)
# This uses the environment variables set in the Render dashboard.
if [ "$CREATE_SUPERUSER_FLAG" = "True" ]; then
    echo "Creating superuser..."
    # python manage.py createsuperuser --no-input
fi
