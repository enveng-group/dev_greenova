# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Centralized Protocol Buffer utilities for the Greenova project.

This module provides common functionality for Protocol Buffer operations
across all apps in the Greenova project.
"""

import importlib
import logging
import os
from typing import Dict, List, Optional, Type

from django.apps import apps
from django.conf import settings
from google.protobuf import message as proto_message
from google.protobuf import symbol_database as _symbol_database

logger = logging.getLogger(__name__)

# Get the global symbol database
_sym_db = _symbol_database.Default()

# Cache for loaded message types
_message_type_cache: Dict[str, Type[proto_message.Message]] = {}


def get_proto_message_type(full_name: str) -> Optional[Type[proto_message.Message]]:
    """
    Get a Protocol Buffer message type by its fully qualified name.

    This function checks the cache first, then falls back to the symbol database.
    If the message type isn't found, it attempts to load appropriate modules
    that might contain the message definition.

    Args:
        full_name: Fully qualified name of the message (e.g., 'feedback.BugReportProto')

    Returns:
        The message class if found, otherwise None
    """
    # Check cache first
    if full_name in _message_type_cache:
        return _message_type_cache[full_name]

    # Try to get from symbol database
    try:
        message_type = _sym_db.GetSymbol(full_name)
        _message_type_cache[full_name] = message_type
        return message_type
    except KeyError:
        # Message type not found, attempt to import relevant modules
        namespace = full_name.split('.')[0]

        # Try to find and import the relevant *_pb2.py files
        for app_config in apps.get_app_configs():
            if app_config.name == namespace or namespace in app_config.name:
                app_path = app_config.path
                pb2_files = _find_pb2_files(app_path)

                for pb2_file in pb2_files:
                    module_name = _get_module_name(pb2_file)
                    try:
                        importlib.import_module(module_name)
                    except ImportError as e:
                        logger.warning("Failed to import %s: %s", module_name, e)

        # Try again after importing modules
        try:
            message_type = _sym_db.GetSymbol(full_name)
            _message_type_cache[full_name] = message_type
            return message_type
        except KeyError:
            logger.error("Could not find Protocol Buffer message type: %s", full_name)
            return None


def _find_pb2_files(directory: str) -> List[str]:
    """Find all *_pb2.py files in a directory and its subdirectories."""
    pb2_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('_pb2.py'):
                # Get the absolute path to the file
                file_path = os.path.join(root, file)
                pb2_files.append(file_path)
    return pb2_files


def _get_module_name(file_path: str) -> str:
    """
    Convert a file path to a module name.

    Args:
        file_path: The path to the file

    Returns:
        The module name for import
    """
    base_dir = os.path.dirname(settings.BASE_DIR)
    relative_path = os.path.relpath(file_path, base_dir)
    # Remove the .py extension
    module_path = os.path.splitext(relative_path)[0]
    # Replace directory separators with dots
    module_name = module_path.replace(os.path.sep, '.')
    return module_name
