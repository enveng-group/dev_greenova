#!/usr/bin/env python
import os
import subprocess
import logging

logger = logging.getLogger(__name__)

def compile_proto():
    """Compile protobuf definitions to Python classes."""
    proto_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'protos')
    output_dir = os.path.dirname(os.path.abspath(__file__))

    proto_files = [f for f in os.listdir(proto_dir) if f.endswith('.proto')]

    for proto_file in proto_files:
        proto_path = os.path.join(proto_dir, proto_file)
        try:
            subprocess.run([
                'protoc',
                f'--python_out={output_dir}',
                f'--proto_path={proto_dir}',
                proto_path
            ], check=True)
            logger.info(f"Successfully compiled {proto_file}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to compile {proto_file}: {str(e)}")

if __name__ == "__main__":
    compile_proto()
