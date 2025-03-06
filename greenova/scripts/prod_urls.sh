#!/bin/sh

# Define constants
SCRIPT_DIR=$(dirname "$0")
PROJECT_DIR="$SCRIPT_DIR/../greenova"
URLS_FILE="urls.py"
BACKUP_FILE="${URLS_FILE}.bak.$(date +%Y%m%d%H%M%S)"

# Navigate to the project directory where urls.py is located
cd "$PROJECT_DIR" || {
  echo "Error: Could not navigate to project directory at $PROJECT_DIR"
  exit 1
}

# Check if the file exists
if [ ! -f "$URLS_FILE" ]; then
  echo "Error: URLs file not found at $PROJECT_DIR/$URLS_FILE"
  exit 1
fi

# Create a backup first
if ! cp "$URLS_FILE" "$BACKUP_FILE"; then
  echo "Error: Failed to create backup file"
  exit 1
fi

echo "Backup created at $PROJECT_DIR/$BACKUP_FILE"

# Create the production URLs content
if cat >"$URLS_FILE" <<'EOF'
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)

def home_router(request):
    """Redirect all traffic to admin login page"""
    return redirect('admin:index')

urlpatterns = [
    # Redirect root URL to admin
    path('', home_router, name='home'),

    # Admin URL - this is the main access point for users
    path('admin/', admin.site.urls),

    # Keep these for functionality but they won't be directly accessible
    path('authentication/', include('authentication.urls')),
]
EOF
then
  echo "Successfully updated URLs for production environment"
  # Ensure the file has proper permissions
  if ! chmod 644 "$URLS_FILE"; then
    echo "Warning: Failed to set permissions on $URLS_FILE"
  fi
else
  echo "Error: Failed to update URLs file"
  # Try to restore from backup
  if ! cp "$BACKUP_FILE" "$URLS_FILE"; then
    echo "Critical error: Failed to restore from backup"
    exit 2
  fi
  echo "Restored from backup"
  exit 1
fi

# Recommend restarting Django server
echo "Remember to restart your Django application to apply these changes"
