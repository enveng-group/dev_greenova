#!/usr/bin/env python3
"""Script to regenerate all stubgen stubs and validate with stubtest.

This script recursively discovers all Python modules in the greenova directory,
generates type stub files (.pyi) using stubgen, and validates them using stubtest.
Follows the project's coding standards for type checking and stub generation.

Author: Adrian Gallo
Email: agallo@enveng-group.com.au
License: AGPL-3.0
"""

import logging
import os
import subprocess
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/stubgen_regeneration.log", encoding="utf-8"),
    ],
)
logger = logging.getLogger(__name__)


def find_python_modules(root_path: Path) -> list[str]:
    """Recursively find all Python modules in the greenova directory.

    Args:
        root_path: The root directory path to search for Python modules.

    Returns:
        A list of module names that can be imported.

    Raises:
        OSError: If the root path is not accessible.

    """
    modules: set[str] = set()

    logger.info("Discovering Python modules in %s", root_path)

    # Walk through all directories and files
    for py_file in root_path.rglob("*.py"):
        if py_file.name == "__init__.py":
            # Handle package directories
            relative_path = py_file.parent.relative_to(root_path)
            if relative_path != Path():
                module_name = str(relative_path).replace(os.sep, ".")
                modules.add(module_name)
        else:
            # Handle individual Python files
            relative_path = py_file.relative_to(root_path)
            module_path = relative_path.with_suffix("")
            module_name = str(module_path).replace(os.sep, ".")
            modules.add(module_name)

    # Filter out test modules and other non-importable modules
    filtered_modules = [
        module
        for module in modules
        if not any(part.startswith("test") for part in module.split("."))
        and not module.startswith("migrations.")
        and "migrations" not in module.split(".")
    ]

    logger.info("Found %d Python modules", len(filtered_modules))
    return sorted(filtered_modules)


def run_command(
    command: list[str], cwd: Path | None = None, setup_django: bool = False
) -> bool:
    """Run a shell command and log the output.

    Args:
        command: The command to run as a list of arguments.
        cwd: The working directory to run the command in.
        setup_django: Whether to set up Django environment variables.

    Returns:
        True if the command succeeded, False otherwise.

    """
    try:
        logger.info("Running command: %s", " ".join(command))

        # Set up environment for mypy tools to find the modules
        env = os.environ.copy()
        if cwd:
            env["PYTHONPATH"] = str(cwd / "greenova")

        # Set up Django environment if needed
        if setup_django:
            env["DJANGO_SETTINGS_MODULE"] = "greenova.settings"
            # Make sure the greenova directory is in the Python path
            greenova_path = (
                str(cwd / "greenova") if cwd else "/workspaces/greenova/greenova"
            )
            if "PYTHONPATH" in env:
                env["PYTHONPATH"] = f"{greenova_path}:{env['PYTHONPATH']}"
            else:
                env["PYTHONPATH"] = greenova_path

        # If this is a stubtest run, redirect output to logs/stubtest_results.log
        log_file = None
        if setup_django:
            logs_dir = Path.cwd() / "logs"
            logs_dir.mkdir(exist_ok=True)
            log_path = logs_dir / "stubtest_results.log"
            log_file = open(log_path, "a", encoding="utf-8")
        try:
            if setup_django:
                # For stubtest: redirect output to log file, do not use capture_output
                result = subprocess.run(
                    command,
                    cwd=cwd,
                    text=True,
                    check=False,
                    encoding="utf-8",
                    env=env,
                    stdout=log_file,
                    stderr=log_file,
                )
            else:
                # For stubgen and other commands: use capture_output, do not set
                # stdout/stderr
                result = subprocess.run(
                    command,
                    cwd=cwd,
                    capture_output=True,
                    text=True,
                    check=False,
                    encoding="utf-8",
                    env=env,
                )
        finally:
            if log_file:
                log_file.close()

        if not setup_django:
            if result.stdout:
                logger.info("STDOUT: %s", result.stdout.strip())
            if result.stderr:
                logger.warning("STDERR: %s", result.stderr.strip())

        if result.returncode == 0:
            logger.info("Command completed successfully")
            return True
        logger.error("Command failed with return code %d", result.returncode)
        return False

    except subprocess.SubprocessError as e:
        logger.exception("Failed to run command: %s", e)
        return False


def generate_stubs(modules: list[str], project_root: Path) -> dict[str, bool]:
    """Generate stub files for the given modules using stubgen.

    Args:
        modules: List of module names to generate stubs for.
        project_root: The project root directory.

    Returns:
        A dictionary mapping module names to success status.

    """
    results: dict[str, bool] = {}

    logger.info("Generating stubs for %d modules", len(modules))

    # Create stubs directory within the greenova project directory
    stubs_dir = project_root / "greenova" / "stubs"
    stubs_dir.mkdir(exist_ok=True)

    for module in modules:
        logger.info("Generating stub for module: %s", module)

        # Run stubgen for each module using global mypy installation
        # Set the working directory to the greenova project directory
        command = [
            "/usr/local/bin/stubgen",
            "--package",
            module,
            "--output",
            str(stubs_dir),
            "--include-private",
            "--export-less",
        ]

        # Run from the greenova directory so modules can be found
        greenova_dir = project_root / "greenova"
        success = run_command(command, cwd=greenova_dir)
        results[module] = success

        if success:
            logger.info("Successfully generated stub for %s", module)
        else:
            logger.error("Failed to generate stub for %s", module)

    return results


def validate_stubs(modules: list[str], project_root: Path) -> dict[str, bool]:
    """Validate generated stub files using stubtest.

    Args:
        modules: List of module names to validate stubs for.
        project_root: The project root directory.

    Returns:
        A dictionary mapping module names to validation status.

    """
    results: dict[str, bool] = {}

    logger.info("Validating stubs for %d modules", len(modules))

    # Use stubs directory within the greenova project directory
    stubs_dir = project_root / "greenova" / "stubs"

    for module in modules:
        logger.info("Validating stub for module: %s", module)

        # Check if stub file exists
        module_stub_path = stubs_dir / f"{module.replace('.', os.sep)}.pyi"
        package_stub_path = stubs_dir / module.replace(".", os.sep) / "__init__.pyi"

        if not (module_stub_path.exists() or package_stub_path.exists()):
            logger.warning("No stub file found for module: %s", module)
            results[module] = False
            continue

        # Run stubtest for the module using our Django-aware wrapper
        # This ensures Django is properly initialized before importing modules
        django_wrapper = project_root / "scripts" / "django_stubtest_wrapper.py"
        command = [
            "/workspaces/greenova/.venv/bin/python",
            str(django_wrapper),
            module,
            "--mypy-config-file",
            str(project_root / "mypy.ini"),
        ]

        # Run from the greenova directory so modules and stubs can be found
        greenova_dir = project_root / "greenova"
        success = run_command(command, cwd=greenova_dir, setup_django=True)
        results[module] = success

        if success:
            logger.info("Successfully validated stub for %s", module)
        else:
            logger.error("Stub validation failed for %s", module)

    return results


def create_py_typed_marker(project_root: Path) -> bool:
    """Create py.typed marker file to indicate type information is available.

    Args:
        project_root: The project root directory.

    Returns:
        True if the marker was created successfully, False otherwise.

    """
    py_typed_path = project_root / "greenova" / "py.typed"

    try:
        py_typed_path.write_text("", encoding="utf-8")
        logger.info("Created py.typed marker file at %s", py_typed_path)
        return True
    except OSError as e:
        logger.exception("Failed to create py.typed marker: %s", e)
        return False


def print_summary(
    stub_results: dict[str, bool], validation_results: dict[str, bool]
) -> None:
    """Print a summary of the stub generation and validation results.

    Args:
        stub_results: Results from stub generation.
        validation_results: Results from stub validation.

    """
    total_modules = len(stub_results)
    successful_stubs = sum(stub_results.values())
    successful_validations = sum(validation_results.values())

    logger.info("=" * 60)
    logger.info("STUB GENERATION AND VALIDATION SUMMARY")
    logger.info("=" * 60)
    logger.info("Total modules processed: %d", total_modules)
    logger.info("Successful stub generations: %d/%d", successful_stubs, total_modules)
    logger.info("Successful validations: %d/%d", successful_validations, total_modules)

    # List failed modules
    failed_stubs = [module for module, success in stub_results.items() if not success]
    failed_validations = [
        module for module, success in validation_results.items() if not success
    ]

    if failed_stubs:
        logger.warning("Failed stub generations:")
        for module in failed_stubs:
            logger.warning("  - %s", module)

    if failed_validations:
        logger.warning("Failed validations:")
        for module in failed_validations:
            logger.warning("  - %s", module)

    if not failed_stubs and not failed_validations:
        logger.info("All operations completed successfully!")

    logger.info("=" * 60)


def main() -> int:
    """Main function to coordinate stub generation and validation.

    Returns:
        Exit code: 0 for success, 1 for failure.

    """
    logger.info("Starting stub generation and validation process")

    # Get project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    greenova_dir = project_root / "greenova"

    if not greenova_dir.exists():
        logger.error("Greenova directory not found at %s", greenova_dir)
        return 1

    # Add project root to Python path
    sys.path.insert(0, str(project_root))

    try:
        # Discover Python modules
        modules = find_python_modules(greenova_dir)

        if not modules:
            logger.warning("No Python modules found in %s", greenova_dir)
            return 1

        # Generate stubs
        logger.info("Phase 1: Generating stub files")
        stub_results = generate_stubs(modules, project_root)

        # Validate stubs
        logger.info("Phase 2: Validating stub files")
        validation_results = validate_stubs(modules, project_root)

        # Create py.typed marker
        logger.info("Phase 3: Creating py.typed marker")
        create_py_typed_marker(project_root)

        # Print summary
        print_summary(stub_results, validation_results)

        # Determine exit code
        all_stubs_successful = all(stub_results.values())
        all_validations_successful = all(validation_results.values())

        if all_stubs_successful and all_validations_successful:
            logger.info("All operations completed successfully")
            return 0
        logger.error("Some operations failed")
        return 1

    except Exception as e:
        logger.exception("Unexpected error occurred: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
