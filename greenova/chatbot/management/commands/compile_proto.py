import logging
import os
import shutil
import subprocess  # nosec B404 - Required for protocol buffer compilation

from django.apps import apps
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
            help='Compile protobuf files for specific app (chatbot, feedback, etc.)'
        )

    def handle(self, *args, **options):
        """Compile protobuf definitions to Python classes."""
        app_name = options.get('app')

        # Default apps to process
        apps_to_process = ['chatbot', 'feedback']

        if app_name:
            if app_name not in apps_to_process:
                self.stdout.write(
                    self.style.ERROR(
                        f"Unknown app: {app_name}. Available apps: "
                        f"{', '.join(apps_to_process)}"
                    )
                )
                return
            apps_to_process = [app_name]

        for app_name in apps_to_process:
            self.stdout.write(self.style.NOTICE(f"Processing {app_name} app..."))
            app_config = apps.get_app_config(app_name)
            app_dir = app_config.path

            # Proto directories to check
            proto_dirs = [
                os.path.join(app_dir, 'proto'),
                os.path.join(app_dir, 'data'),
            ]

            # Output to the app directory
            output_dir = app_dir

            self._compile_proto_files(proto_dirs, output_dir)

    def _compile_proto_files(self, proto_dirs, output_dir):
        """Compile proto files from specified directories to output directory.

        Args:
            proto_dirs: List of directories containing .proto files
            output_dir: Directory where generated Python files will be saved
        """
        proto_files_found = False
        protoc_path = self._get_protoc_path()
        if not protoc_path:
            return

        for proto_dir in proto_dirs:
            proto_files = self._get_proto_files(proto_dir)
            if not proto_files:
                continue

            proto_files_found = True
            self._process_proto_files(proto_files, proto_dir, output_dir, protoc_path)

        if not proto_files_found:
            self.stdout.write(
                self.style.WARNING(
                    "No protocol buffer files were found to compile!"
                )
            )
            return

        self.stdout.write(
            self.style.SUCCESS(
                "Protocol buffer compilation "
                "completed successfully"
            )
        )

    def _get_protoc_path(self):
        """Get the absolute path to the protoc executable."""
        protoc_path = shutil.which('protoc')
        if not protoc_path:
            self.stdout.write(self.style.ERROR("protoc executable not found in PATH"))
            self._show_installation_instructions()
        return protoc_path

    def _get_proto_files(self, proto_dir):
        """Retrieve .proto files from a directory."""
        if not os.path.exists(proto_dir):
            self.stdout.write(
                self.style.WARNING(
                    f"Directory {proto_dir} doesn't exist, skipping"
                )
            )
            return []

        proto_files = [f for f in os.listdir(proto_dir) if f.endswith('.proto')]
        if not proto_files:
            self.stdout.write(
                self.style.WARNING(
                    f"No .proto files found in {proto_dir}, skipping"
                )
            )
        return proto_files

    def _process_proto_files(self, proto_files, proto_dir, output_dir, protoc_path):
        """Process and compile .proto files."""
        for proto_file in proto_files:
            proto_path = os.path.join(proto_dir, proto_file)
            self.stdout.write(f"Compiling {proto_path} to {output_dir}")

            try:
                # Ensure inputs are sanitized and trusted
                if not os.path.isfile(protoc_path):
                    raise ValueError(f"Invalid protoc path: {protoc_path}")
                if not os.path.isdir(output_dir):
                    raise ValueError(f"Invalid output directory: {output_dir}")
                if not os.path.isdir(proto_dir):
                    raise ValueError(f"Invalid proto directory: {proto_dir}")
                if not os.path.isfile(proto_path):
                    raise ValueError(f"Invalid proto file path: {proto_path}")

                subprocess.run([  # nosec B603 - Inputs are validated above
                    os.path.abspath(protoc_path),
                    f'--python_out={os.path.abspath(output_dir)}',
                    f'--proto_path={os.path.abspath(proto_dir)}',
                    os.path.abspath(proto_path)
                ],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    shell=False
                )

                self._verify_generated_file(proto_file, output_dir)

            except subprocess.CalledProcessError as e:
                self._handle_compilation_error(proto_file, e)

    def _verify_generated_file(self, proto_file, output_dir):
        """Verify if the expected output file was generated."""
        base_name = os.path.splitext(proto_file)[0]
        expected_output = os.path.join(output_dir, f"{base_name}_pb2.py")
        if os.path.exists(expected_output):
            self.stdout.write(self.style.SUCCESS(f"Generated file: {expected_output}"))
        else:
            self.stdout.write(
                self.style.ERROR(
                    f"Expected output file {expected_output} not found!"
                )
            )

    def _handle_compilation_error(self, proto_file, error):
        """Handle errors during proto file compilation."""
        self.stdout.write(
            self.style.ERROR(
                f"Failed to compile {proto_file}: {str(error)}"
            )
        )
        stderr = error.stderr.decode() if error.stderr else 'No output'
        self.stdout.write(self.style.ERROR(f"Command output: {stderr}"))

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
