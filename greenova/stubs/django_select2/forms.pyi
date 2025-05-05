from typing import Any, Dict, List, Optional, Type

from django.forms import (
    ModelChoiceField,
    ModelMultipleChoiceField,
    Select,
    SelectMultiple,
)

class Select2Widget(Select):
    def __init__(
        self, attrs: Optional[Dict[str, Any]] = None, choices: Any = None, **kwargs: Any
    ) -> None: ...

class Select2MultipleWidget(SelectMultiple):
    def __init__(
        self, attrs: Optional[Dict[str, Any]] = None, choices: Any = None, **kwargs: Any
    ) -> None: ...

class ModelSelect2Widget(Select2Widget):
    def __init__(
        self,
        model: Type[Any],
        search_fields: List[str],
        attrs: Optional[Dict[str, Any]] = None,
        choices: Any = None,
        **kwargs: Any,
    ) -> None: ...

class ModelSelect2MultipleWidget(Select2MultipleWidget):
    def __init__(
        self,
        model: Type[Any],
        search_fields: List[str],
        attrs: Optional[Dict[str, Any]] = None,
        choices: Any = None,
        **kwargs: Any,
    ) -> None: ...

class ModelSelect2Field(ModelChoiceField):
    def __init__(
        self,
        queryset: Any,
        search_fields: List[str],
        attrs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None: ...

class ModelSelect2MultipleField(ModelMultipleChoiceField):
    def __init__(
        self,
        queryset: Any,
        search_fields: List[str],
        attrs: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None: ...
