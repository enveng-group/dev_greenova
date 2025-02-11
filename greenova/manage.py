#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import logging
import os
import signal
import sys
from dataclasses import dataclass
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, List, NoReturn, Optional

# Add the project root to Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))


class ManagementError(Exception):
    """Custom exception for management command errors."""

    pass


@dataclass(frozen=True)
class EnvironmentContext:
    """Environment configuration context."""

    project_root: Path
    environment: str
    debug: bool
    log_level: str
    settings_module: str
    allowed_hosts: List[str]
    time_zone: str
    version: str

    @classmethod
    def from_env(cls) -> "EnvironmentContext":
        """Create context from environment variables."""
        project_root = Path(__file__).resolve().parent
        return cls(
            project_root=project_root,
            environment=os.getenv("GREENOVA_ENVIRONMENT", "development"),
            debug=os.getenv("DJANGO_DEBUG", "True") == "True",
            log_level=os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            settings_module=os.getenv(
                "DJANGO_SETTINGS_MODULE", "greenova.settings"
            ),
            allowed_hosts=os.getenv(
                "DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1"
            ).split(","),
            time_zone=os.getenv("DJANGO_TIME_ZONE", "UTC"),
            version=os.getenv("GREENOVA_VERSION", "0.1.0"),
        )


@dataclass(frozen=True)
class SystemContext:
    """System runtime context."""

    start_time: datetime
    pid: int
    state_file: Path
    last_startup: Optional[float] = None

    @classmethod
    def create(cls, env_context: EnvironmentContext) -> "SystemContext":
        """Create system context."""
        state_file = env_context.project_root / ".system_state"
        last_startup = None
        if state_file.exists():
            try:
                last_startup = float(state_file.read_text().strip())
            except (ValueError, IOError):
                pass

        return cls(
            start_time=datetime.now(),
            pid=os.getpid(),
            state_file=state_file,
            last_startup=last_startup,
        )


def validate_environment() -> bool:
    """Validate required environment variables."""
    required_vars = [
        "DJANGO_SETTINGS_MODULE",
        "DJANGO_SECRET_KEY",
        "DJANGO_ALLOWED_HOSTS",
        "DJANGO_TIME_ZONE",
        "GREENOVA_ENVIRONMENT",
        "GREENOVA_VERSION",
    ]

    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ManagementError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )
    return True


def setup_logging(context: EnvironmentContext) -> None:
    """Configure logging system."""
    log_dir = context.project_root / "logs"
    log_dir.mkdir(exist_ok=True)

    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    handlers = [
        RotatingFileHandler(
            log_dir / "django-admin.log",
            maxBytes=1024 * 1024,  # 1MB
            backupCount=3,
        ),
        logging.StreamHandler(),
    ]

    logging.basicConfig(
        level=log_levels.get(context.log_level.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )


def signal_handler(signum: int, _: Any) -> NoReturn:
    """Handle system signals."""
    logging.info(f"Received signal {signum}")
    sys.exit(0)


def save_system_state(context: SystemContext) -> None:
    """Save system state to file."""
    try:
        context.state_file.write_text(str(context.start_time.timestamp()))
    except IOError as e:
        logging.error(f"Failed to save system state: {e}")


def initialize_system() -> Optional[SystemContext]:
    """Initialize system components."""
    try:
        env_context = EnvironmentContext.from_env()
        validate_environment()
        setup_logging(env_context)
        system_context = SystemContext.create(env_context)
        save_system_state(system_context)
        return system_context
    except Exception as e:
        logging.error(f"System initialization failed: {e}")
        return None


def main() -> int:
    """Main execution function."""
    try:
        # Initialize system
        system_context = initialize_system()
        if not system_context:
            return 1

        # Set up signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Execute Django management commands
        from django.core.management import execute_from_command_line

        execute_from_command_line(sys.argv)
        return 0

    except Exception as e:
        logging.error(f"Management command failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
