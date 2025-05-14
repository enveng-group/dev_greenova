"""Unit tests for base and layout templates in the Greenova project.

These tests verify template inheritance, semantic HTML structure, accessibility,
HTMX and Hyperscript integration, and context variable rendering.
"""

import logging

import pytest
from django.template.loader import render_to_string
from django.urls import reverse

# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

logger = logging.getLogger(__name__)


@pytest.mark.django_db
class TestBaseTemplates:
    """Test suite for base and layout templates."""

    def test_base_minimal_template_renders(self):
        """Test that base_minimal.html renders and contains required blocks."""
        html = render_to_string("base_minimal.html", {"request": None})
        assert "<!DOCTYPE html>" in html
        assert "<html" in html
        assert 'lang="' in html
        assert "<head" in html
        assert "<body" in html
        assert "{% block body %}" not in html  # Should be rendered, not raw tag

    def test_base_template_inherits_minimal(self):
        """Test that base.html extends base_minimal.html and renders blocks."""
        html = render_to_string("base.html", {"request": None})
        assert "greenova" in html
        assert "<main" in html or "<body" in html
        assert "htmx" in html or "hx-" in html
        assert "theme" in html

    def test_header_component_renders(self, client):
        """Test that _header.html renders with required navigation."""
        response = client.get(reverse("landing:index"))
        content = response.content.decode("utf-8")
        assert "<nav" in content
        assert "navbar" in content
        assert "Theme switcher" in content

    def test_footer_component_renders(self, client):
        """Test that _footer.html renders with required info and links."""
        response = client.get(reverse("landing:index"))
        content = response.content.decode("utf-8")
        assert "<footer" in content
        assert "Greenova" in content
        assert "System Status" in content
        assert "support@enveng-group.com.au" in content

    def test_breadcrumbs_component_renders(self, client):
        """Test that _breadcrumbs.html renders with semantic nav."""
        response = client.get(reverse("dashboard:home"))
        content = response.content.decode("utf-8")
        assert 'aria-label="Breadcrumb navigation"' in content
        assert "<ul" in content
        assert "Dashboard" in content

    def test_partial_base_layout_renders(self):
        """Test that _partial_base.html renders main block."""
        html = render_to_string("layouts/_partial_base.html", {"request": None})
        assert "<main" in html

    def test_template_blocks_and_includes(self):
        """Test that base.html includes header and footer components."""
        html = render_to_string("base.html", {"request": None})
        assert "_header.html" not in html  # Should be rendered, not included as text
        assert "_footer.html" not in html
        assert "<header" in html or "<nav" in html
        assert "<footer" in html

    def test_accessibility_skip_link_present(self, client):
        """Test that skip link for accessibility is present in base.html."""
        response = client.get(reverse("landing:index"))
        content = response.content.decode("utf-8")
        assert 'class="skip-link"' in content
        assert 'href="#main-content"' in content

    def test_csrf_token_in_forms(self, client):
        """Test that CSRF token is present in forms."""
        response = client.get(reverse("landing:index"))
        content = response.content.decode("utf-8")
        # Not all pages have forms, but if present, CSRF should be included
        if "<form" in content:
            assert "csrfmiddlewaretoken" in content

    def test_htmx_and_hyperscript_integration(self, client):
        """Test that HTMX and Hyperscript scripts are included."""
        response = client.get(reverse("landing:index"))
        content = response.content.decode("utf-8")
        assert "htmx.min" in content, "HTMX script not found in landing page HTML"
        assert "_hyperscript.min" in content, (
            "Hyperscript script not found in landing page HTML"
        )

    def test_semantic_html_structure(self, client):
        """Test that semantic HTML5 elements are present."""
        response = client.get(reverse("landing:index"))
        content = response.content.decode("utf-8")
        assert "<header" in content
        assert "<main" in content
        assert "<footer" in content

    def test_template_context_variables(self, client):
        """Test that context variables are rendered in the footer."""
        response = client.get(reverse("landing:index"))
        content = response.content.decode("utf-8")
        assert "System Status" in content
        assert "Version" in content
        assert "Last Updated" in content
