from typing import (
    Any,
    Callable,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

# Type variables
_F = TypeVar("_F", bound=Callable[..., Any])
_T = TypeVar("_T")

# Core pytest functions and decorators
def fixture(
    scope: str = "function",
    params: Optional[List[Any]] = None,
    autouse: bool = False,
    ids: Optional[List[str]] = None,
    name: Optional[str] = None,
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

class raises:
    def __init__(
        self,
        expected_exception: Union[Type[BaseException], Tuple[Type[BaseException], ...]],
        match: Optional[str] = None,
        *,
        message: Optional[str] = None,
    ) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool: ...

class LineMatcher:
    def __init__(self) -> None: ...
    def fnmatch_lines(self, lines: List[str]) -> None: ...
    def re_match_lines(self, lines: List[str]) -> None: ...
    def str(self) -> str: ...  # Simple method definition

# Magic assert
def register_assert_rewrite(*names: str) -> None: ...
