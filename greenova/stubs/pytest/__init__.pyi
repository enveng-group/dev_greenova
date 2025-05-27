from collections.abc import Callable
from typing import (
    Any,
    TypeVar,
)

# Type variables
_F = TypeVar("_F", bound=Callable[..., Any])
_T = TypeVar("_T")

# Core pytest functions and decorators
def fixture(
    scope: str = "function",
    params: list[Any] | None = None,
    autouse: bool = False,
    ids: list[str] | None = None,
    name: str | None = None,
) -> Callable[[_F], _F]: ...

class MarkDecorator:
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...

class MarkGenerator:
    @property
    def parametrize(self) -> MarkDecorator: ...
    @property
    def skip(self) -> MarkDecorator: ...
    @property
    def skipif(self) -> MarkDecorator: ...
    @property
    def xfail(self) -> MarkDecorator: ...
    @property
    def usefixtures(self) -> MarkDecorator: ...
    def __getattr__(self, name: str) -> MarkDecorator: ...

# Export the mark instance - make sure there's only one definition
mark: MarkGenerator

class RAISES:
    def __init__(
        self,
        expected_exception: type[BaseException] | tuple[type[BaseException], ...],
        match: str | None = None,
        *,
        message: str | None = None,
    ) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool: ...

class LineMatcher:
    def __init__(self) -> None: ...
    def fnmatch_lines(self, lines: list[str]) -> None: ...
    def re_match_lines(self, lines: list[str]) -> None: ...
    def str(self) -> str: ...  # Simple method definition

# Magic assert
def register_assert_rewrite(*names: str) -> None: ...
