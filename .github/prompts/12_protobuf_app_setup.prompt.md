<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [GitHub Copilot Setup Checklist for Protobuf App](#github-copilot-setup-checklist-for-protobuf-app)
  - [Goal](#goal)
  - [Directory Structure](#directory-structure)
  - [Setup Checklist](#setup-checklist)
  - [Expectations](#expectations)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# GitHub Copilot Setup Checklist for Protobuf App

## Goal

Establish the `protobuf` app as the single source of truth for all `.proto` files in the Greenova project. Ensure all Protobuf definitions, server/client stub generation, and integration points follow project standards.

## Directory Structure

- `/workspaces/greenova/protobuf/`
  - `*.proto` (all Protobuf3 schema files for the project)
  - `README.rst` (overview and usage instructions)
  - `Makefile` or build scripts for stub generation
  - `py.typed` (if any Python modules are present)

## Setup Checklist

1. **Protobuf File Management**

   - Store all `.proto` files for the project in this app.
   - Organize proto files by domain or app if needed (e.g., `core.proto`, `obligations.proto`).
   - Document the purpose and structure of each proto file in `README.rst`.

2. **Stub Generation**

   - Add scripts or Makefile targets to:
     - Compile Python stubs (`*_pb2.py`) into each Django app that needs them.
     - Compile JS/TS stubs using `protobufjs` or `as-proto` into each app's static directory (e.g., `static/core/js/proto/`).
   - Ensure all generated stubs are up-to-date and committed if required.
   - Document the stub generation process in `README.rst`.

3. **Integration**

   - Instruct all other apps to import their stubs from the generated locations.
   - Update all static references (e.g., `wasm-loader.ts`, `index.ts`) to use the new proto locations in static assets.
   - Use symlinks or build scripts for developer convenience if needed.

4. **Linting & Validation**

   - Use `protolint` or similar tools to lint `.proto` files.
   - Ensure all proto files are well-documented and pass linting.

5. **Testing**

   - Add tests to validate that generated stubs are importable and match the proto definitions.
   - Use `stubtest` for Python stubs if any Python modules are present.

6. **Documentation**
   - Maintain `README.rst` with clear instructions for adding new proto files, generating stubs, and integrating with Django/JS/TS apps.

## Expectations

- All `.proto` files are managed centrally in this app.
- All server/client stubs are generated from here and integrated into the relevant apps.
- Linting, documentation, and testing are in place for all proto definitions and stubs.
- The app passes all pre-commit checks and project standards.
