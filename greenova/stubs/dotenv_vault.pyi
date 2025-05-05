from typing import Any, Dict, Optional

def load_dotenv(
    dotenv_path: Optional[str] = None,
    stream: Optional[Any] = None,
    verbose: bool = False,
    override: bool = False,
    interpolate: bool = True,
) -> bool: ...
def find_dotenv(
    filename: str = ".env",
    raise_error_if_not_found: bool = False,
    usecwd: bool = False,
) -> str: ...
def get_key(key_name: str, default: Optional[str] = None) -> Optional[str]: ...
def set_key(
    dotenv_path: str,
    key_name: str,
    value: str,
    quote_mode: str = "always",
) -> bool: ...
def unset_key(dotenv_path: str, key_name: str) -> bool: ...
def dotenv_values(
    dotenv_path: Optional[str] = None,
    stream: Optional[Any] = None,
    verbose: bool = False,
    interpolate: bool = True,
) -> Dict[str, str]: ...
