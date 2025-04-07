# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: 	AGPL-3.0-or-later

import logging
import re

from django.http import HttpResponse

logger = logging.getLogger(__name__)

class ProtobufErrorMiddleware:
    """Middleware to catch protobuf-related KeyErrors and show helpful messages."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        """Process exceptions and catch protobuf-related KeyErrors."""
        if isinstance(exception, KeyError) and "Couldn't find message" in str(exception):
            # Extract the message type from the error
            message_type_match = re.search(r"Couldn't find message ([a-zA-Z0-9_.]+)", str(exception))
            if message_type_match:
                message_type = message_type_match.group(1)
                app_name = message_type.split('.')[0]

                error_message = f"""
                <h1>Protocol Buffer Error</h1>
                <p>Protocol buffer module for <code>{message_type}</code> not found.</p>
                <p>Please run: <code>python manage.py compile_proto --app {app_name}</code></p>
                <p>Or for all apps: <code>python manage.py compile_proto</code></p>
                """
                return HttpResponse(error_message, content_type='text/html', status=500)
        return None
