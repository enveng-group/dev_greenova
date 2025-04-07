import logging
import os
import shutil
import subprocess  # nosec B404 - Required for protocol buffer compilation

logger = logging.getLogger(__name__)

def compile_proto():
    """
    Compiles protocol buffer files (.proto) into Python modules.

    This function looks for .proto files in the proto directory within the chatbot app
    and compiles them using the protoc compiler.
    """
    try:
        # Get the directory where this script is located
        base_dir = os.path.dirname(os.path.abspath(__file__))
        proto_dir = os.path.join(base_dir, 'proto')

        # Check if proto directory exists
        if not os.path.exists(proto_dir):
            os.makedirs(proto_dir)
            logger.info("Created proto directory at %s", proto_dir)
            msg = "No .proto files found. Please add your proto files"
            msg += " to the proto directory."
            logger.warning(msg)
            return

        # Find all .proto files
        proto_files = [f for f in os.listdir(proto_dir) if f.endswith('.proto')]

        if not proto_files:
            logger.warning("No .proto files found in proto directory.")
            return

        # Get absolute path to protoc executable
        protoc_path = shutil.which('protoc')
        if not protoc_path:
            logger.error("protoc executable not found in PATH")
            return

        # Compile each .proto file
        for proto_file in proto_files:
            proto_path = os.path.join(proto_dir, proto_file)
            logger.info("Compiling %s...", proto_file)

            # Run protoc compiler
            # nosec B603,B607 - Using a verified executable path controlling inputs
            result = subprocess.run(
                [
                    protoc_path,
                    f'--proto_path={proto_dir}',
                    f'--python_out={base_dir}',
                    proto_path
                ],
                capture_output=True,
                text=True,
                check=False
            )

            if result.returncode == 0:
                logger.info("Successfully compiled %s", proto_file)
            else:
                logger.error("Failed to compile %s: %s", proto_file, result.stderr)

        logger.info("Protocol buffer compilation complete")

    except Exception as e:
        logger.error("Error compiling protocol buffers: %s", str(e))
        raise

if __name__ == "__main__":
    # Set up logging when run directly
    logging.basicConfig(level=logging.INFO)
    compile_proto()
