"""Serializers for the landing app.

This module provides serialization/deserialization functionality for the landing app
using Protocol Buffers (Protobuf3). All API endpoints in the landing app use Protobuf3
for data exchange, including newsletter signup and landing page content.

Usage Notes:
- See landing_pb2 for Protobuf3 message definitions.
- Use LandingSerializer static methods to serialize/deserialize newsletter signup requests and responses.
- All API endpoints expect and return Protobuf3-encoded data.
- See docs/LANDING_APP.rst for integration and API usage details.
"""

import logging
from typing import Any

from beartype import beartype
from django.core.exceptions import ValidationError

from greenova.landing import landing_pb2

logger = logging.getLogger(__name__)


class LandingSerializer:
    """Serializer for landing page data using Protocol Buffers."""

    @staticmethod
    @beartype
    def serialize_newsletter_signup_request(email: str) -> bytes:
        """Serialize a newsletter signup request to Protobuf bytes.

        Args:
            email: The email address to serialize.

        Returns:
            Protobuf-encoded bytes for NewsletterSignupRequest.

        Raises:
            ValidationError: If the email is invalid.

        """
        from django.core.validators import validate_email

        validate_email(email)  # Will raise ValidationError if invalid
        msg = landing_pb2.NewsletterSignupRequest()
        msg.email = email
        return msg.SerializeToString()

    @staticmethod
    @beartype
    def deserialize_newsletter_signup_request(data: bytes) -> str:
        """Deserialize Protobuf bytes to email string.

        Args:
            data: Protobuf-encoded bytes.

        Returns:
            The email address from the deserialized message.

        """
        msg = landing_pb2.NewsletterSignupRequest()
        try:
            msg.ParseFromString(data)
        except Exception as exc:
            logger.exception("Failed to deserialize newsletter signup request: %s", exc)
            msg = "Invalid newsletter signup request data"
            raise ValidationError(msg) from exc
        return msg.email

    @staticmethod
    @beartype
    def serialize_newsletter_signup_response(success: bool, message: str) -> bytes:
        """Serialize a newsletter signup response to Protobuf bytes.

        Args:
            success: Whether the signup was successful.
            message: Response message.

        Returns:
            Protobuf-encoded bytes for NewsletterSignupResponse.

        """
        msg = landing_pb2.NewsletterSignupResponse()
        msg.success = success
        msg.message = message
        return msg.SerializeToString()

    @staticmethod
    @beartype
    def deserialize_newsletter_signup_response(data: bytes) -> dict[str, Any]:
        """Deserialize Protobuf bytes to a dictionary.

        Args:
            data: Protobuf-encoded bytes.

        Returns:
            Dictionary with 'success' and 'message' keys.

        """
        msg = landing_pb2.NewsletterSignupResponse()
        try:
            msg.ParseFromString(data)
        except Exception as exc:
            logger.exception(
                "Failed to deserialize newsletter signup response: %s",
                exc,
            )
            msg = "Invalid newsletter signup response data"
            raise ValidationError(msg) from exc
        return {"success": msg.success, "message": msg.message}

    @staticmethod
    @beartype
    def serialize_landing_page_content(
        hero_title: str,
        hero_subtitle: str,
        features: list[dict[str, str]],
        stats: dict[str, int],
        benefits: list[str],
        testimonials: list[dict[str, str]],
        cta_title: str,
        cta_subtitle: str,
    ) -> bytes:
        """Serialize landing page content to protobuf bytes.

        Args:
            hero_title: Title for the hero section.
            hero_subtitle: Subtitle for the hero section.
            features: List of feature dicts with 'title' and 'description'.
            stats: Dictionary of stat name to value.
            benefits: List of benefit strings.
            testimonials: List of testimonial dicts with 'name' and 'content'.
            cta_title: Call-to-action title.
            cta_subtitle: Call-to-action subtitle.

        Returns:
            Serialized protobuf bytes.

        """
        content = landing_pb2.LandingPageContent()
        content.hero_title = hero_title
        content.hero_subtitle = hero_subtitle
        for feat in features:
            f = landing_pb2.Feature()
            f.title = feat.get("title", "")
            f.description = feat.get("description", "")
            content.features.append(f)
        for name, value in stats.items():
            s = landing_pb2.Stat()
            s.name = name
            s.value = value
            content.stats.append(s)
        content.benefits.extend(benefits)
        for t in testimonials:
            test = landing_pb2.Testimonial()
            test.name = t.get("name", "")
            test.content = t.get("content", "")
            content.testimonials.append(test)
        content.cta_title = cta_title
        content.cta_subtitle = cta_subtitle
        serialized_data = content.SerializeToString()
        logger.debug("Serialized landing page content")
        return serialized_data

    @staticmethod
    @beartype
    def deserialize_landing_page_content(data: bytes) -> dict[str, Any]:
        """Deserialize landing page content from protobuf bytes.

        Args:
            data: Serialized protobuf bytes.

        Returns:
            Dictionary containing landing page content.

        Raises:
            ValidationError: If deserialization fails.

        """
        try:
            content = landing_pb2.LandingPageContent()
            content.ParseFromString(data)
            logger.debug("Deserialized landing page content")
            return {
                "hero_title": content.hero_title,
                "hero_subtitle": content.hero_subtitle,
                "features": [
                    {"title": f.title, "description": f.description}
                    for f in content.features
                ],
                "stats": {s.name: s.value for s in content.stats},
                "benefits": list(content.benefits),
                "testimonials": [
                    {"name": t.name, "content": getattr(t, "content", "")}
                    for t in content.testimonials
                ],
                "cta_title": content.cta_title,
                "cta_subtitle": content.cta_subtitle,
            }
        except Exception as e:
            logger.exception("Failed to deserialize landing page content: %s", e)
            msg = "Invalid landing page content data"
            raise ValidationError(msg) from e

    @staticmethod
    @beartype
    def parse_newsletter_signup_request(
        data: bytes,
    ) -> landing_pb2.NewsletterSignupRequest:
        """Parse a NewsletterSignupRequest from Protobuf bytes.

        Args:
            data: Protobuf-encoded request bytes.

        Returns:
            NewsletterSignupRequest message.

        """
        msg = landing_pb2.NewsletterSignupRequest()
        msg.ParseFromString(data)
        return msg

    @staticmethod
    @beartype
    def build_newsletter_signup_response(success: bool, message: str) -> bytes:
        """Build a NewsletterSignupResponse and serialize to Protobuf bytes.

        Args:
            success: Whether signup was successful.
            message: Response message.

        Returns:
            Protobuf-encoded NewsletterSignupResponse bytes.

        """
        resp = landing_pb2.NewsletterSignupResponse(success=success, message=message)
        return resp.SerializeToString()

    @staticmethod
    @beartype
    def build_landing_page_content() -> bytes:
        """Build and serialize landing page content (features, stats, testimonials, etc.).

        Returns:
            Protobuf-encoded LandingPageContent bytes.

        """
        content = landing_pb2.LandingPageContent(
            hero_title="Environmental Management Made Simple",
            hero_subtitle="Greenova empowers professionals to achieve compliance excellence.",
            features=[
                landing_pb2.Feature(
                    title="Obligation Tracking",
                    description="Track all your environmental obligations in one place.",
                ),
                landing_pb2.Feature(
                    title="Automated Reminders",
                    description="Never miss a deadline with automated compliance reminders.",
                ),
                landing_pb2.Feature(
                    title="Real-Time Dashboards",
                    description="Visualize compliance status and key metrics instantly.",
                ),
            ],
            stats=[
                landing_pb2.Stat(name="Obligations Managed", value=1200),
                landing_pb2.Stat(name="Projects Supported", value=85),
                landing_pb2.Stat(name="Compliance Rate", value=99),
                landing_pb2.Stat(name="Active Users", value=350),
            ],
            benefits=[
                "Reduce compliance risk and manual effort.",
                "Centralize all regulatory requirements.",
                "Boost team accountability and transparency.",
            ],
            testimonials=[
                landing_pb2.Testimonial(
                    name="Alex, Environmental Manager",
                    content="Greenova has transformed our compliance process—simple, reliable, and effective!",
                ),
                landing_pb2.Testimonial(
                    name="Morgan, Consultant",
                    content="The dashboards and reminders keep my clients on track. Highly recommended.",
                ),
            ],
            cta_title="Ready to Transform Your Environmental Compliance?",
            cta_subtitle="Join thousands of professionals who trust Greenova.",
        )
        return content.SerializeToString()
