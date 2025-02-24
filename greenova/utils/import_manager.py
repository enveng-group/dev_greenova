import logging
from django.apps import apps
from django.db.models import Model
from typing import Type, Optional, Any

logger = logging.getLogger(__name__)

class ImportManager:
    """
    Manages model imports and relationships to avoid circular dependencies.
    """

    @staticmethod
    def get_model(app_label: str, model_name: str) -> Optional[Type[Model]]:
        """
        Get a model class by its app label and model name.

        Args:
            app_label: The Django app label
            model_name: The model class name

        Returns:
            The model class or None if not found
        """
        try:
            return apps.get_model(app_label, model_name)
        except LookupError as e:
            logger.error(f"Error getting model {app_label}.{model_name}: {str(e)}")
            return None

    @staticmethod
    def lazy_related_model(app_label: str, model_name: str) -> str:
        """
        Returns a string reference to a model for lazy evaluation.

        Args:
            app_label: The Django app label
            model_name: The model class name

        Returns:
            String in format 'app_label.ModelName'
        """
        return f"{app_label}.{model_name}"

    @classmethod
    def get_or_none(cls, model_class: Type[Model], **kwargs: Any) -> Optional[Model]:
        """
        Safely get a model instance or return None.

        Args:
            model_class: The model class to query
            **kwargs: Lookup parameters

        Returns:
            Model instance or None if not found
        """
        try:
            return model_class.objects.get(**kwargs)
        except model_class.DoesNotExist:
            return None
        except Exception as e:
            logger.error(f"Error getting {model_class.__name__}: {str(e)}")
            return None

    @staticmethod
    def is_model_ready(app_label: str, model_name: str) -> bool:
        """
        Check if a model is ready to be imported.

        Args:
            app_label: The Django app label
            model_name: The model class name

        Returns:
            bool: True if model is ready
        """
        try:
            apps.get_registered_model(app_label, model_name)
            return True
        except LookupError:
            return False

# Global instance
manager = ImportManager()
