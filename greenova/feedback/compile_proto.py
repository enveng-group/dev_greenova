# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Script to compile Protocol Buffer definitions for the feedback app.

This script compiles .proto files in the proto directory into Python modules
that can be used for serialization and deserialization.
"""

import logging
import os
import re
import shutil
import subprocess  # nosec B404 - Required for protocol buffer compilation
from typing import List, Optional

logger = logging.getLogger(__name__)


def is_safe_filename(filename: str) -> bool:
    """
    Validates that a filename is safe to use with subprocess.

    Args:
        filename: The filename to validate

    Returns:
        bool: True if the filename is safe, False otherwise
    """
    # Only allow alphanumeric characters, underscore, hyphen, and .proto extension
    return bool(re.match(r'^[a-zA-Z0-9_-]+\.proto$', filename))


def sanitize_path(path: str) -> str:
    """
    Sanitize a path to prevent command injection.

    Args:
        path: The path to sanitize

    Returns:
        str: The sanitized path
    """
    # Remove any shell-specific characters and normalize path
    sanitized = os.path.normpath(path)
    # Ensure the path contains only safe characters
    if not re.match(r'^[a-zA-Z0-9_/.-]+$', sanitized):
        raise ValueError(f"Path contains unsafe characters: {path}")
    return sanitized


def compile_proto() -> None:
    """
    Compiles protocol buffer files (.proto) into Python modules.

    This function looks for .proto files in the proto directory within the feedback app
    and compiles them using the protoc compiler.
    """
    try:
        base_dir, proto_dir = setup_directories()
        proto_files = find_proto_files(proto_dir)
        if not proto_files:
            return

        protoc_path = validate_protoc_executable()
        if not protoc_path:
            return

        compile_proto_files(proto_files, base_dir, proto_dir, protoc_path)
        logger.info("Protocol buffer compilation complete")

    except Exception as e:
        logger.error("Error compiling protocol buffers: %s", str(e))
        raise


def setup_directories() -> tuple:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    proto_dir = os.path.join(base_dir, 'proto')

    if not os.path.exists(proto_dir):
        os.makedirs(proto_dir)
        logger.info("Created proto directory at %s", proto_dir)
        logger.warning(
            "No .proto files found. Please add your proto files to the proto directory."
        )
    return base_dir, proto_dir


def find_proto_files(proto_dir: str) -> List[str]:
    proto_files = [
        f for f in os.listdir(proto_dir)
        if f.endswith('.proto')
    ]
    if not proto_files:
        logger.warning("No .proto files found in proto directory.")
    return proto_files


def validate_protoc_executable() -> Optional[str]:
    protoc_path = shutil.which('protoc')
    if not protoc_path:
        logger.error("protoc executable not found in PATH")
        return None

    if not os.path.isfile(protoc_path):
        logger.error("protoc path is not a file: %s", protoc_path)
        return None

    if not os.access(protoc_path, os.X_OK):
        logger.error("protoc is not executable: %s", protoc_path)
        return None

    return protoc_path


def compile_proto_files(
    proto_files: List[str],
    base_dir: str,
    proto_dir: str,
    protoc_path: str
) -> None:
    for proto_file in proto_files:
        if not is_safe_filename(proto_file):
            logger.error(
                (
                    "Invalid proto file name: %s "
                    "(must be alphanumeric with .proto extension)"
                ),
                proto_file
            )
            continue

        proto_path = os.path.join(proto_dir, proto_file)
        if not validate_proto_file(proto_path, proto_dir):
            continue

        try:
            run_protoc(proto_file, proto_path, base_dir, proto_dir, protoc_path)
        except ValueError as ve:
            logger.error("Security error while sanitizing paths: %s", str(ve))


def validate_proto_file(proto_path: str, proto_dir: str) -> bool:
    real_proto_path = os.path.realpath(proto_path)
    real_proto_dir = os.path.realpath(proto_dir)
    if not real_proto_path.startswith(real_proto_dir):
        logger.error(
            "Security error: File path traversal detected for %s",
            proto_path
        )
        return False

    if not os.path.isfile(proto_path):
        logger.error(
            "Proto file does not exist or is not a file: %s",
            proto_path
        )
        return False

    return True


def run_protoc(
    proto_file: str,
    proto_path: str,
    base_dir: str,
    proto_dir: str,
    protoc_path: str
) -> None:
    safe_proto_path = sanitize_path(proto_path)
    safe_proto_dir = sanitize_path(proto_dir)
    safe_base_dir = sanitize_path(base_dir)
    safe_protoc_path = sanitize_path(protoc_path)

    logger.info("Compiling %s...", proto_file)

    result = subprocess.run(  # nosec B603
        [
            safe_protoc_path,
            f'--proto_path={safe_proto_dir}',
            f'--python_out={safe_base_dir}',
            safe_proto_path
        ],
        capture_output=True,
        text=True,
        check=False,
        shell=False
    )

    if result.returncode == 0:
        logger.info("Successfully compiled %s", proto_file)
    else:
        logger.error("Failed to compile %s: %s", proto_file, result.stderr)


if __name__ == "__main__":
    # Set up logging when run directly
    logging.basicConfig(level=logging.INFO)
    compile_proto()
