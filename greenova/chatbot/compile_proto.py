import os
import subprocess
import logging

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
            logger.info(f"Created proto directory at {proto_dir}")
            logger.warning("No .proto files found. Please add your proto files to the proto directory.")
            return

        # Find all .proto files
        proto_files = [f for f in os.listdir(proto_dir) if f.endswith('.proto')]

        if not proto_files:
            logger.warning("No .proto files found in proto directory.")
            return

        # Compile each .proto file
        for proto_file in proto_files:
            proto_path = os.path.join(proto_dir, proto_file)
            logger.info(f"Compiling {proto_file}...")

            # Run protoc compiler
            result = subprocess.run(
                [
                    'protoc',
                    f'--proto_path={proto_dir}',
                    f'--python_out={base_dir}',
                    proto_path
                ],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                logger.info(f"Successfully compiled {proto_file}")
            else:
                logger.error(f"Failed to compile {proto_file}: {result.stderr}")

        logger.info("Protocol buffer compilation complete")

    except Exception as e:
        logger.error(f"Error compiling protocol buffers: {str(e)}")
        raise

if __name__ == "__main__":
    # Set up logging when run directly
    logging.basicConfig(level=logging.INFO)
    compile_proto()
