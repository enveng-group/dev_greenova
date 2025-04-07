import logging
import os
import shutil
import subprocess  # nosec B404 - Required for protocol buffer compilation

from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Compile protocol buffer definition files to Python classes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force recompilation of existing files'
        )

    def handle(self, *args, **options):
        """Compile protobuf definitions to Python classes."""
        # Note: force option is defined but currently not used in the implementation
        # We're keeping the parameter for future use but ignoring the pylint warning
        # pylint: disable=unused-variable
        force = options.get('force', False)

        # Get the app directory (2 levels up from this file)
        base_path = os.path.abspath(__file__)
        dir_path = os.path.dirname
        current_dir = dir_path(dir_path(dir_path(base_path)))

        # Proto file sources
        proto_dirs = [
            os.path.join(current_dir, 'data'),
        ]

        # Output to the app directory
        output_dir = current_dir

        self._compile_proto_files(proto_dirs, output_dir)

    def _compile_proto_files(self, proto_dirs, output_dir):
        """Compile proto files from specified directories to output directory.

        Args:
            proto_dirs: List of directories containing .proto files
            output_dir: Directory where generated Python files will be saved
        """
        # pylint: disable=too-many-locals
        proto_files_found = False

        # Get absolute path to protoc executable
        protoc_path = shutil.which('protoc')
        if not protoc_path:
            error_msg = "protoc executable not found in PATH"
            self.stdout.write(self.style.ERROR(error_msg))
            self._show_installation_instructions()
            return

        for proto_dir in proto_dirs:
            if not os.path.exists(proto_dir):
                msg = f"Directory {proto_dir} doesn't exist, skipping"
                self.stdout.write(self.style.WARNING(msg))
                continue

            proto_files = [f for f in os.listdir(proto_dir) if f.endswith('.proto')]

            if not proto_files:
                msg = f"No .proto files found in {proto_dir}, skipping"
                self.stdout.write(self.style.WARNING(msg))
                continue

            proto_files_found = True

            for proto_file in proto_files:
                proto_path = os.path.join(proto_dir, proto_file)
                self.stdout.write(f"Compiling {proto_path} to {output_dir}")

                try:
                    # Run the protoc command
                    # nosec B603,B607 - Using verified absolute path with controlled inputs
                    subprocess.run([
                        protoc_path,
                        f'--python_out={output_dir}',
                        f'--proto_path={proto_dir}',
                        proto_path
                    ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    # Verify the generated file exists
                    base_name = os.path.splitext(proto_file)[0]
                    expected_output = os.path.join(output_dir, f"{base_name}_pb2.py")
                    if os.path.exists(expected_output):
                        success_msg = f"Generated file: {expected_output}"
                        self.stdout.write(self.style.SUCCESS(success_msg))
                    else:
                        error_msg = f"Expected output file {expected_output} not found!"
                        self.stdout.write(self.style.ERROR(error_msg))

                except subprocess.CalledProcessError as e:
                    error_msg = f"Failed to compile {proto_file}: {str(e)}"
                    self.stdout.write(self.style.ERROR(error_msg))
                    stderr = e.stderr.decode() if e.stderr else 'No output'
                    output_msg = f"Command output: {stderr}"
                    self.stdout.write(self.style.ERROR(output_msg))

        if not proto_files_found:
            warning_msg = "No protocol buffer files were found to compile!"
            self.stdout.write(self.style.WARNING(warning_msg))
            return

        success_msg = "Protocol buffer compilation completed successfully"
        self.stdout.write(self.style.SUCCESS(success_msg))

    def _check_protoc_available(self):
        """Check if protoc compiler is available.

        Returns:
            bool: True if protoc is available, False otherwise
        """
        try:
            # Get absolute path to protoc executable
            protoc_path = shutil.which('protoc')
            if not protoc_path:
                return False

            # nosec B603,B607 - Using verified absolute path with controlled inputs
            subprocess.run(
                [protoc_path, '--version'],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
            
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
