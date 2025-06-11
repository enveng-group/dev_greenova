# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: 	AGPL-3.0-or-later

import logging

from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class ProjectSelectionMiddleware(MiddlewareMixin):
    """
    Middleware to manage selected_project_id in session and request.
    Ensures project selection is consistent for all views, including HTMX.
    """

    def process_request(self, request: HttpRequest):
        project_ids = request.GET.getlist("project_id")
        project_id = next((pid for pid in reversed(project_ids) if pid), None)
        if project_id:
            request.session["selected_project_id"] = project_id
            request.selected_project_id = project_id
            logger.debug("ProjectSelectionMiddleware: Set project_id %s", project_id)
        elif "selected_project_id" in request.session:
            request.selected_project_id = request.session["selected_project_id"]
        else:
            request.selected_project_id = None
