"""Protocol Buffer compilation utilities for Greenova.

This module provides utilities to compile .proto files into Python modules
and manage protobuf data serialization.
"""

import subprocess
import sys
from pathlib import Path

from beartype import beartype


@beartype
def get_proto_dir() -> Path:
    """Get the directory containing .proto files.

    Returns:
        Path to the protobuf directory.

    """
    return Path(__file__).parent


@beartype
def get_proto_files() -> list[Path]:
    """Get list of all .proto files in the protobuf directory.

    Returns:
        List of paths to .proto files.

    """
    proto_dir = get_proto_dir()
    return list(proto_dir.glob("*.proto"))


@beartype
def compile_proto_file(proto_file: Path, output_dir: Path | None = None) -> bool:
    """Compile a single .proto file to Python.

    Args:
        proto_file: Path to the .proto file to compile.
        output_dir: Output directory for compiled files. Defaults to same directory.

    Returns:
        True if compilation successful, False otherwise.

    """
    if output_dir is None:
        output_dir = proto_file.parent

    try:
        # Use protoc to compile the .proto file
        cmd = [
            "protoc",
            f"--proto_path={proto_file.parent}",
            f"--python_out={output_dir}",
            str(proto_file),
        ]

        subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )

        return True

    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False


@beartype
def compile_all_protos() -> bool:
    """Compile all .proto files in the protobuf directory.

    Returns:
        True if all files compiled successfully, False otherwise.

    """
    proto_files = get_proto_files()

    if not proto_files:
        return True

    success_count = 0
    for proto_file in proto_files:
        if compile_proto_file(proto_file):
            success_count += 1

    total_files = len(proto_files)

    return success_count == total_files


@beartype
def check_protoc_available() -> bool:
    """Check if protoc compiler is available.

    Returns:
        True if protoc is available, False otherwise.

    """
    try:
        subprocess.run(
            ["protoc", "--version"],
            capture_output=True,
            check=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


if __name__ == "__main__":
    """Compile protobuf files when run as a script."""
    if not check_protoc_available():
        sys.exit(1)

    if compile_all_protos():
        sys.exit(0)
    else:
        sys.exit(1)
