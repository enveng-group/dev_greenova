# Compiling Protocol Buffers for Greenova

To compile your Protocol Buffer files into Python modules for use in the
Greenova project, follow these steps:

## Prerequisites

Ensure you have the following installed and configured:

1. **Python 3.9.21**: The version used in the Greenova project.
2. **Django 4.1.13**: Ensure your Django environment is set up.
3. **Protobuf Compiler**: Install the Protocol Buffer compiler (`protoc`).

   ```bash
   sudo apt-get install -y protobuf-compiler
   ```

4. **Protobuf Python Package**: Install the Python bindings for Protocol
   Buffers.

   ```bash
   pip install protobuf
   ```

## Compilation Steps

1. Open the Django shell:

   ```bash
   python manage.py shell
   ```

2. In the shell, run the following commands to compile your `.proto` files:

   ```python
   from chatbot.compile_proto import compile_proto
   compile_proto()
   ```

   This will generate Python modules from your `.proto` files, making them
   ready for import and use in your application.

## Notes

- Ensure your `.proto` files are correctly placed in the designated directory
  as specified in your `compile_proto` function.
- The generated Python modules will be located in the output directory defined
  in your `compile_proto` implementation.

## Troubleshooting

- If you encounter errors during compilation, verify the following:
  - The `protoc` compiler is installed and accessible in your system's PATH.
  - Your `.proto` files are free of syntax errors.
  - The output directory has the necessary write permissions.

For further assistance, refer to the
[Protocol Buffers documentation](https://protobuf.dev/).
