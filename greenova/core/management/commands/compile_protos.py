# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Management command to compile Protocol Buffer definition files for the project.
"""

import logging
import os
import shutil
# nosec B404 - subprocess is necessary but used with all security precautions
import subprocess  # nosec B404
from shlex import quote
from subprocess import (PIPE, CalledProcessError, CompletedProcess,  # nosec B404
                        TimeoutExpired)

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Compile protocol buffer definition files for the project'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recompilation of existing files'
        )
        parser.add_argument(
            '--app',
            type=str,
            help='Compile protobuf files for specific app'
        )

    def handle(self, *args, **options):
        """Compile protobuf definitions to Python classes."""
        app_name = options.get('app')
        force = options.get('force', False)

        # Process all apps if no specific app is provided
        if app_name:
            try:
                app_config = apps.get_app_config(app_name)
                self.process_app(app_config, force)
            except LookupError:
                self.stdout.write(
                    self.style.ERROR(f"Unknown app: {app_name}")
                )
                return
        else:
            # Get all app configs and process each one
            app_configs = apps.get_app_configs()
            for app_config in app_configs:
                # Skip Django's built-in apps
                if not app_config.path.startswith(settings.BASE_DIR):
                    continue
                self.process_app(app_config, force)

        self.stdout.write(
            self.style.SUCCESS(
                "Protocol buffer compilation completed successfully"
            )
        )

    def process_app(self, app_config, force=False):
        """Process protocol buffer files for a single app."""
        app_dir = app_config.path
        app_name = app_config.name

        # Check if this app has proto directories
        proto_dirs = [
            os.path.join(app_dir, 'proto'),
            os.path.join(app_dir, 'data')
        ]

        proto_files_found = False
        for proto_dir in proto_dirs:
            if not os.path.exists(proto_dir):
                continue

            self.stdout.write(
                self.style.NOTICE(f"Processing {app_name} app...")
            )

            proto_files = self._get_proto_files(proto_dir)
            if not proto_files:
                continue

            proto_files_found = True
            protoc_path = self._get_protoc_path()
            if not protoc_path:
                return

            paths = {
                "proto_dir": proto_dir,
                "output_dir": app_dir,
                "protoc_path": protoc_path,
            }
            self._process_proto_files(proto_files, paths, force)

        if proto_files_found:
            self.stdout.write(
                self.style.SUCCESS(f"Finished processing {app_name} app")
            )

    def _get_protoc_path(self):
        """Get the absolute path to the protoc executable."""
        protoc_path = shutil.which('protoc')
        if not protoc_path:
            self.stdout.write(self.style.ERROR("protoc executable not found in PATH"))
            self._show_installation_instructions()
            return None
        return protoc_path

    def _get_proto_files(self, proto_dir):
        """Retrieve .proto files from a directory."""
        if not os.path.exists(proto_dir):
            return []

        proto_files = [f for f in os.listdir(proto_dir) if f.endswith('.proto')]
        if not proto_files:
            self.stdout.write(
                self.style.WARNING(
                    f"No .proto files found in {proto_dir}, skipping"
                )
            )
        return proto_files

    def _process_proto_files(self, proto_files, paths, force=False):
        """Process a list of proto files."""
        proto_dir = paths["proto_dir"]
        output_dir = paths["output_dir"]
        protoc_path = paths["protoc_path"]

        for proto_file in proto_files:
            self._compile_proto_file(
                proto_file=proto_file,
                paths={
                    "proto_dir": proto_dir,
                    "output_dir": output_dir,
                    "protoc_path": protoc_path,
                },
                force=force
            )

    def _compile_proto_file(self, proto_file, paths, force):
        """Compile a single proto file securely."""
        try:
            proto_path = os.path.join(paths["proto_dir"], proto_file)
            base_name = os.path.splitext(proto_file)[0]
            expected_output = os.path.join(
                paths["output_dir"], f"{base_name}_pb2.py"
            )

            # Skip if output file exists and force is not set
            if os.path.exists(expected_output) and not force:
                self.stdout.write(f"Skipping {proto_file} (already compiled)")
                return

            self.stdout.write(f"Compiling {proto_file} to {paths['output_dir']}")

            # Security validation for all paths
            self._validate_paths(paths, proto_path)

            # Use absolute paths for security
            safe_paths = {
                "proto_path": os.path.abspath(proto_path),
                "proto_dir": os.path.abspath(paths["proto_dir"]),
                "output_dir": os.path.abspath(paths["output_dir"]),
                "protoc_path": os.path.abspath(paths["protoc_path"])
            }

            self._run_protoc_command(safe_paths)
            self._verify_generated_file(proto_file, paths["output_dir"])

        except (subprocess.CalledProcessError, ValueError) as e:
            self._handle_compilation_error(proto_file, e)

    def _validate_paths(self, paths, proto_path):
        """Validate all paths for security and existence."""
        if not os.path.isfile(paths["protoc_path"]):
            raise ValueError(f"Invalid protoc path: {paths['protoc_path']}")
        if not os.path.isdir(paths["output_dir"]):
            raise ValueError(f"Invalid output directory: {paths['output_dir']}")
        if not os.path.isdir(paths["proto_dir"]):
            raise ValueError(f"Invalid proto directory: {paths['proto_dir']}")
        if not os.path.isfile(proto_path):
            raise ValueError(f"Invalid proto file: {proto_path}")

        # Ensure no path traversal is possible
        for _, path in paths.items():
            if '..' in path or not os.path.normpath(path) == path:
                raise ValueError(f"Potentially unsafe path detected: {path}")

        # Ensure proto file is within proto_dir
        if not os.path.dirname(os.path.abspath(proto_path)).startswith(
            os.path.abspath(paths["proto_dir"])
        ):
            raise ValueError(f"Proto file {proto_path} is outside of proto directory")

    def _run_protoc_command(self, paths):
        """Execute protoc command with proper arguments."""
        try:
            # Use shlex.quote on all user-influenced paths for extra security
            # even though we're using the subprocess list form already
            safe_output_dir = quote(paths["output_dir"])
            safe_proto_dir = quote(paths["proto_dir"])
            safe_proto_path = quote(paths["proto_path"])

            # Log command being executed for audit trail
            logger.info(
                "Executing protoc: %s --python_out=%s --proto_path=%s %s",
                paths["protoc_path"], safe_output_dir, safe_proto_dir, safe_proto_path
            )

            # Build command with arguments as a list for safety
            cmd = [
                paths["protoc_path"],
                f'--python_out={paths["output_dir"]}',
                f'--proto_path={paths["proto_dir"]}',
                paths["proto_path"]
            ]

            # Use a secure execution pattern with explicit parameters
            result = self._secure_command_exec(
                cmd=cmd,
                timeout=30
            )

            # Log successful execution
            logger.debug("protoc executed successfully")
            return result

        except TimeoutExpired as exc:
            logger.error("protoc execution timed out")
            raise ValueError("Protocol buffer compilation timed out") from exc

    def _secure_command_exec(self, cmd, timeout=30) -> CompletedProcess:
        """Execute a command securely with proper parameters and validation."""
        if not isinstance(cmd, list):
            raise ValueError("Command must be a list, not a string")

        # Verify no shell=True is used and capture all output
        # nosec B603 - We're explicitly using shell=False for security and validation
        return subprocess.run(
            cmd,
            check=True,
            stdout=PIPE,
            stderr=PIPE,
            shell=False,  # nosec B603
            timeout=timeout
        )

    def _handle_compilation_error(self, proto_file, error):
        """Handle errors during proto file compilation."""
        if isinstance(error, CalledProcessError):
            stderr = error.stderr.decode() if error.stderr else 'No output'
            self.stdout.write(
                self.style.ERROR(
                    f"Failed to compile {proto_file}: {stderr}"
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    f"Failed to compile {proto_file}: {str(error)}"
                )
            )

    def _show_installation_instructions(self):
        """Show instructions for installing the protoc compiler"""
        err_msg = (
            "protoc command not found. "
            "Please install Protocol Buffers compiler."
        )
        self.stdout.write(self.style.ERROR(err_msg))

        ubuntu_msg = "On Ubuntu: sudo apt-get install protobuf-compiler"
        self.stdout.write(self.style.WARNING(ubuntu_msg))

        mac_msg = "On macOS: brew install protobuf"
        self.stdout.write(self.style.WARNING(mac_msg))

        doc_url = (
            "See https://grpc.io/docs/protoc-installation/ "
            "for more details"
        )
        self.stdout.write(self.style.WARNING(doc_url))
