from collections.abc import Callable
from typing import Any

class Environment:
    def __init__(
        self,
        block_start_string: str = "{%",
        block_end_string: str = "%}",
        variable_start_string: str = "{{",
        variable_end_string: str = "}}",
        comment_start_string: str = "{#",
        comment_end_string: str = "#}",
        line_statement_prefix: str | None = None,
        line_comment_prefix: str | None = None,
        trim_blocks: bool = False,
        lstrip_blocks: bool = False,
        newline_sequence: str = "\n",
        keep_trailing_newline: bool = False,
        extensions: list[str] | None = None,
        optimized: bool = True,
        undefined: type[Any] | None = None,
        finalize: Callable | None = None,
        autoescape: bool | Callable[[str | None], bool] = False,
        loader: Any = None,
        cache_size: int = 400,
        auto_reload: bool = True,
        bytecode_cache: Any | None = None,
        enable_async: bool = False,
    ) -> None: ...
    def get_template(
        self,
        name: str,
        parent: str | None = None,
        globals: dict[str, Any] | None = None,
    ) -> Template: ...
    def select_template(
        self,
        names: list[str],
        parent: str | None = None,
        globals: dict[str, Any] | None = None,
    ) -> Template: ...
    def from_string(
        self,
        source: str,
        globals: dict[str, Any] | None = None,
        template_class: type[Template] | None = None,
    ) -> Template: ...

class Template:
    def render(self, *args: Any, **kwargs: Any) -> str: ...
    def stream(self, *args: Any, **kwargs: Any) -> Any: ...
    def generate(self, *args: Any, **kwargs: Any) -> Any: ...

class FileSystemLoader:
    def __init__(
        self,
        searchpath: str | list[str],
        encoding: str = "utf-8",
        followlinks: bool = False,
    ) -> None: ...

class PackageLoader:
    def __init__(
        self,
        package_name: str,
        package_path: str = "templates",
        encoding: str = "utf-8",
    ) -> None: ...

class ChoiceLoader:
    def __init__(self, loaders: list[Any]) -> None: ...

class PrefixLoader:
    def __init__(self, loaders: dict[str, Any], delimiter: str = "/") -> None: ...

def select_autoescape(
    enabled_extensions: list[str] | None = None,
    disabled_extensions: list[str] | None = None,
    default_for_string: bool = True,
    default: bool = False,
) -> Callable[[str | None], bool]: ...
