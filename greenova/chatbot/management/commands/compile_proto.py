from django.core.management.base import BaseCommand
import os
import subprocess
import logging

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
        force = options.get('force', False)

        # Get the app directory (2 levels up from this file)
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Proto file sources
        proto_dirs = [
            os.path.join(current_dir, 'data'),
        ]

        # Output to the app directory
        output_dir = current_dir

        proto_files_found = False

        for proto_dir in proto_dirs:
            if not os.path.exists(proto_dir):
                self.stdout.write(self.style.WARNING(f"Directory {proto_dir} doesn't exist, skipping"))
                continue

            proto_files = [f for f in os.listdir(proto_dir) if f.endswith('.proto')]

            if not proto_files:
                self.stdout.write(self.style.WARNING(f"No .proto files found in {proto_dir}, skipping"))
                continue

            proto_files_found = True

            for proto_file in proto_files:
                proto_path = os.path.join(proto_dir, proto_file)
                self.stdout.write(f"Compiling {proto_path} to {output_dir}")

                try:
                    # Ensure the protoc command is available
                    try:
                        subprocess.run(['protoc', '--version'],
                                       check=True,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
                    except (subprocess.SubprocessError, FileNotFoundError):
                        self.stdout.write(self.style.ERROR("protoc command not found. Please install Protocol Buffers compiler."))
                        self.stdout.write(self.style.WARNING("On Ubuntu: sudo apt-get install protobuf-compiler"))
                        self.stdout.write(self.style.WARNING("On macOS: brew install protobuf"))
                        self.stdout.write(self.style.WARNING("See https://grpc.io/docs/protoc-installation/ for more details"))
                        return

                    # Run the protoc command
                    result = subprocess.run([
                        'protoc',
                        f'--python_out={output_dir}',
                        f'--proto_path={proto_dir}',
                        proto_path
                    ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                    # Verify the generated file exists
                    expected_output = os.path.join(output_dir, f"{os.path.splitext(proto_file)[0]}_pb2.py")
                    if os.path.exists(expected_output):
                        self.stdout.write(self.style.SUCCESS(f"Generated file: {expected_output}"))
                    else:
                        self.stdout.write(self.style.ERROR(f"Expected output file {expected_output} not found!"))

                except subprocess.CalledProcessError as e:
                    self.stdout.write(self.style.ERROR(f"Failed to compile {proto_file}: {str(e)}"))
                    self.stdout.write(self.style.ERROR(f"Command output: {e.stderr.decode() if e.stderr else 'No output'}"))

        if not proto_files_found:
            self.stdout.write(self.style.WARNING("No protocol buffer files were found to compile!"))
            return

        self.stdout.write(self.style.SUCCESS("Protocol buffer compilation completed successfully"))
