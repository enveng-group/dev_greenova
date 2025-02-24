import logging
from django.db import models
from typing import Optional, Type, Any, Dict

logger = logging.getLogger(__name__)

class RelationshipManager:
    """
    Manages model relationships to avoid circular dependencies.
    """

    @staticmethod
    def create_foreign_key(
            to: str,
            on_delete: Any = models.CASCADE,
            **kwargs: Any) -> models.ForeignKey:
        """
        Create a ForeignKey with string reference to avoid circular imports.

        Args:
            to: Model reference as 'app_label.ModelName'
            on_delete: On delete behavior
            **kwargs: Additional field options
        """
        return models.ForeignKey(to, on_delete=on_delete, **kwargs)

    @staticmethod
    def create_many_to_many(
            to: str,
            through: Optional[str] = None,
            **kwargs: Any) -> models.ManyToManyField:
        """
        Create a ManyToManyField with string references.

        Args:
            to: Model reference as 'app_label.ModelName'
            through: Through model reference as 'app_label.ModelName'
            **kwargs: Additional field options
        """
        if through:
            kwargs['through'] = through
        return models.ManyToManyField(to, **kwargs)

# Global instance
relationship_manager = RelationshipManager()
