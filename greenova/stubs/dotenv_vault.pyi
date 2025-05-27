from typing import Any

def load_dotenv(
    dotenv_path: str | None = None,
    stream: Any | None = None,
    verbose: bool = False,
    override: bool = False,
    interpolate: bool = True,
) -> bool: ...
def find_dotenv(
    filename: str = ".env",
    raise_error_if_not_found: bool = False,
    usecwd: bool = False,
) -> str: ...
def get_key(key_name: str, default: str | None = None) -> str | None: ...
def set_key(
    dotenv_path: str,
    key_name: str,
    value: str,
    quote_mode: str = "always",
) -> bool: ...
def unset_key(dotenv_path: str, key_name: str) -> bool: ...
def dotenv_values(
    dotenv_path: str | None = None,
    stream: Any | None = None,
    verbose: bool = False,
    interpolate: bool = True,
) -> dict[str, str]: ...
