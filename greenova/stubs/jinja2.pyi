from typing import Any, Callable, Dict, List, Optional, Type, Union

class Environment:
    def __init__(
        self,
        block_start_string: str = "{%",
        block_end_string: str = "%}",
        variable_start_string: str = "{{",
        variable_end_string: str = "}}",
        comment_start_string: str = "{#",
        comment_end_string: str = "#}",
        line_statement_prefix: Optional[str] = None,
        line_comment_prefix: Optional[str] = None,
        trim_blocks: bool = False,
        lstrip_blocks: bool = False,
        newline_sequence: str = "\n",
        keep_trailing_newline: bool = False,
        extensions: Optional[List[str]] = None,
        optimized: bool = True,
        undefined: Optional[Type[Any]] = None,
        finalize: Optional[Callable] = None,
        autoescape: Union[bool, Callable[[Optional[str]], bool]] = False,
        loader: Any = None,
        cache_size: int = 400,
        auto_reload: bool = True,
        bytecode_cache: Optional[Any] = None,
        enable_async: bool = False,
    ) -> None: ...
    def get_template(
        self,
        name: str,
        parent: Optional[str] = None,
        globals: Optional[Dict[str, Any]] = None,
    ) -> "Template": ...
    def select_template(
        self,
        names: List[str],
        parent: Optional[str] = None,
        globals: Optional[Dict[str, Any]] = None,
    ) -> "Template": ...
    def from_string(
        self,
        source: str,
        globals: Optional[Dict[str, Any]] = None,
        template_class: Optional[Type["Template"]] = None,
    ) -> "Template": ...

class Template:
    def render(self, *args: Any, **kwargs: Any) -> str: ...
    def stream(self, *args: Any, **kwargs: Any) -> Any: ...
    def generate(self, *args: Any, **kwargs: Any) -> Any: ...

class FileSystemLoader:
    def __init__(
        self,
        searchpath: Union[str, List[str]],
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
    def __init__(self, loaders: List[Any]) -> None: ...

class PrefixLoader:
    def __init__(self, loaders: Dict[str, Any], delimiter: str = "/") -> None: ...

def select_autoescape(
    enabled_extensions: Optional[List[str]] = None,
    disabled_extensions: Optional[List[str]] = None,
    default_for_string: bool = True,
    default: bool = False,
) -> Callable[[Optional[str]], bool]: ...
