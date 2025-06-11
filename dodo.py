#!/usr/bin/env python3
"""Doit build automation for Greenova.

This file defines build tasks for the Greenova project using the Doit task runner.
Tasks include protobuf compilation, frontend builds, and asset management.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

import os
import subprocess
from pathlib import Path
from typing import Any

from beartype import beartype

# Project paths
WORKSPACE_ROOT = Path("/workspaces/greenova")
GREENOVA_ROOT = WORKSPACE_ROOT / "greenova"
PROTOBUF_DIR = GREENOVA_ROOT / "protobuf"
FRONTEND_TS_DIR = GREENOVA_ROOT / "core" / "static" / "core" / "ts"
FRONTEND_AS_DIR = GREENOVA_ROOT / "core" / "static" / "core" / "as"
FRONTEND_SCSS_DIR = GREENOVA_ROOT / "core" / "static" / "core" / "scss"
FRONTEND_JS_DIR = GREENOVA_ROOT / "core" / "static" / "core" / "js"
FRONTEND_CSS_DIR = GREENOVA_ROOT / "core" / "static" / "core" / "css"
FRONTEND_AS_PROTO_DIR = FRONTEND_AS_DIR / "assembly" / "as-proto"


@beartype
def get_proto_files() -> list[Path]:
    """Get all .proto files in the protobuf directory."""
    return list(PROTOBUF_DIR.glob("*.proto"))


@beartype
def get_ts_files() -> list[Path]:
    """Get all TypeScript files recursively."""
    return list(FRONTEND_TS_DIR.rglob("*.ts"))


@beartype
def get_scss_files() -> list[Path]:
    """Get all SCSS files recursively."""
    return list(FRONTEND_SCSS_DIR.rglob("*.scss"))


@beartype
def get_as_files() -> list[Path]:
    """Get all AssemblyScript files."""
    return list((FRONTEND_AS_DIR / "assembly").rglob("*.ts"))


# =============================================================================
# Protobuf Compilation Tasks
# =============================================================================


def task_compile_proto_python() -> dict[str, Any]:
    """Compile .proto files to Python *_pb2.py files."""
    proto_files = get_proto_files()

    def compile_proto() -> None:
        """Compile protobuf files."""
        os.chdir(GREENOVA_ROOT)
        for proto_file in proto_files:
            cmd = [
                "protoc",
                f"--python_out={PROTOBUF_DIR}",
                f"--pyi_out={PROTOBUF_DIR}",
                f"protobuf/{proto_file.name}",
            ]
            subprocess.run(cmd, check=True)

    return {
        "actions": [compile_proto],
        "file_dep": [str(f) for f in proto_files],
        "targets": [str(PROTOBUF_DIR / f"{f.stem}_pb2.py") for f in proto_files],
        "clean": True,
        "verbosity": 2,
    }


def task_compile_proto_as():
    """Copy .proto files to AssemblyScript directory for as-proto."""
    proto_files = get_proto_files()

    def copy_protos() -> None:
        """Copy proto files to AssemblyScript directory."""
        os.makedirs(FRONTEND_AS_DIR / "proto", exist_ok=True)
        for proto_file in proto_files:
            target = FRONTEND_AS_DIR / "proto" / proto_file.name
            with open(proto_file, encoding="utf-8") as src:
                with open(target, "w", encoding="utf-8") as dst:
                    dst.write(src.read())

    return {
        "actions": [copy_protos],
        "file_dep": [str(f) for f in proto_files],
        "targets": [str(FRONTEND_AS_DIR / "proto" / f.name) for f in proto_files],
        "clean": True,
        "verbosity": 2,
    }


def task_generate_proto_as() -> dict[str, Any]:
    """Generate AssemblyScript stubs from .proto files using as-proto-gen."""
    proto_files = get_proto_files()

    def generate_as_stubs() -> None:
        """Generate AssemblyScript protobuf stubs."""
        os.makedirs(FRONTEND_AS_DIR / "assembly" / "proto", exist_ok=True)
        os.chdir(GREENOVA_ROOT)

        for proto_file in proto_files:
            cmd = [
                "protoc",
                f"--plugin=protoc-gen-as={WORKSPACE_ROOT}/node_modules/.bin/as-proto-gen",
                f"--as_out={FRONTEND_AS_DIR}/assembly/proto",
                f"protobuf/{proto_file.name}",
            ]
            subprocess.run(cmd, check=True)

    target_files = [
        str(FRONTEND_AS_DIR / "assembly" / "proto" / f"{f.stem}.ts")
        for f in proto_files
    ]

    return {
        "actions": [generate_as_stubs],
        "file_dep": [str(f) for f in proto_files],
        "targets": target_files,
        "clean": True,
        "verbosity": 2,
    }


# =============================================================================
# AssemblyScript / WASM Compilation Tasks
# =============================================================================


def task_copy_as_proto_runtime():
    """Copy as-proto runtime files to AssemblyScript directory."""
    PACKAGE_JSON = WORKSPACE_ROOT / "package.json"
    PACKAGE_LOCK_JSON = WORKSPACE_ROOT / "package-lock.json"

    def copy_runtime() -> None:
        """Copy as-proto runtime files."""
        os.makedirs(FRONTEND_AS_PROTO_DIR, exist_ok=True)
        os.makedirs(FRONTEND_AS_PROTO_DIR / "internal", exist_ok=True)

        # Copy main as-proto files with proper globbing
        source_files = list(
            (WORKSPACE_ROOT / "node_modules" / "as-proto" / "assembly").glob("*.ts")
        )
        for src_file in source_files:
            dst_file = FRONTEND_AS_PROTO_DIR / src_file.name
            with open(src_file, encoding="utf-8") as src:
                with open(dst_file, "w", encoding="utf-8") as dst:
                    dst.write(src.read())

        # Copy internal files
        internal_files = list(
            (
                WORKSPACE_ROOT / "node_modules" / "as-proto" / "assembly" / "internal"
            ).glob("*.ts")
        )
        for src_file in internal_files:
            dst_file = FRONTEND_AS_PROTO_DIR / "internal" / src_file.name
            with open(src_file, encoding="utf-8") as src:
                with open(dst_file, "w", encoding="utf-8") as dst:
                    dst.write(src.read())

    return {
        "actions": [copy_runtime],
        "file_dep": [str(PACKAGE_JSON), str(PACKAGE_LOCK_JSON)],
        "targets": [str(FRONTEND_AS_PROTO_DIR / "Reader.ts")],
        "clean": True,
        "verbosity": 2,
    }


def task_compile_wasm_debug():
    """Compile AssemblyScript to WASM (debug mode)."""
    as_files = get_as_files()

    def compile_wasm_debug() -> None:
        """Compile AssemblyScript to debug WASM."""
        os.chdir(WORKSPACE_ROOT)
        cmd = [
            "npx",
            "asc",
            str(FRONTEND_AS_DIR / "assembly" / "index.ts"),
            "--config",
            str(FRONTEND_AS_DIR / "asconfig.json"),
            "--outFile",
            str(FRONTEND_AS_DIR / "build" / "debug.wasm"),
            "--debug",
            "--sourceMap",
        ]
        subprocess.run(cmd, check=True)

    return {
        "actions": [compile_wasm_debug],
        "file_dep": [str(f) for f in as_files]
        + [str(FRONTEND_AS_DIR / "asconfig.json")],
        "targets": [str(FRONTEND_AS_DIR / "build" / "debug.wasm")],
        "task_dep": ["copy_as_proto_runtime", "generate_proto_as"],
        "clean": True,
        "verbosity": 2,
    }


def task_compile_wasm_release():
    """Compile AssemblyScript to WASM (release mode)."""
    as_files = get_as_files()

    def compile_wasm_release() -> None:
        """Compile AssemblyScript to release WASM."""
        os.chdir(WORKSPACE_ROOT)
        cmd = [
            "npx",
            "asc",
            str(FRONTEND_AS_DIR / "assembly" / "index_simple.ts"),
            "--config",
            str(FRONTEND_AS_DIR / "asconfig.json"),
            "--outFile",
            str(FRONTEND_AS_DIR / "build" / "release.wasm"),
            "--optimize",
            "--sourceMap",
        ]
        subprocess.run(cmd, check=True)

    return {
        "actions": [compile_wasm_release],
        "file_dep": [str(f) for f in as_files]
        + [str(FRONTEND_AS_DIR / "asconfig.json")],
        "targets": [str(FRONTEND_AS_DIR / "build" / "release.wasm")],
        "task_dep": ["copy_as_proto_runtime", "compile_proto_as"],
        "clean": True,
        "verbosity": 2,
    }


# =============================================================================
# Frontend Build Tasks (Parcel)
# =============================================================================


def task_build_scss():
    """Compile SCSS to CSS using Sass and PostCSS."""
    scss_files = get_scss_files()

    def compile_scss() -> None:
        """Compile SCSS to CSS."""
        os.chdir(WORKSPACE_ROOT)
        # Compile main SCSS file
        cmd = [
            "sass",
            str(FRONTEND_SCSS_DIR / "main.scss")
            + ":"
            + str(FRONTEND_CSS_DIR / "main.css"),
            "--style=compressed",
            "--source-map",
        ]
        subprocess.run(cmd, check=True)

        # Run PostCSS
        cmd = [
            "postcss",
            str(FRONTEND_CSS_DIR / "main.css"),
            "-o",
            str(FRONTEND_CSS_DIR / "main.css"),
        ]
        subprocess.run(cmd, check=True)

    return {
        "actions": [compile_scss],
        "file_dep": [str(f) for f in scss_files] + [str(WORKSPACE_ROOT / ".postcssrc")],
        "targets": [str(FRONTEND_CSS_DIR / "main.css")],
        "clean": True,
        "verbosity": 2,
    }


def task_build_typescript():
    """Compile TypeScript to JavaScript using TypeScript compiler."""
    ts_files = get_ts_files()

    def compile_typescript() -> None:
        """Compile TypeScript to JavaScript."""
        os.chdir(FRONTEND_TS_DIR)
        cmd = ["tsc", "-p", str(FRONTEND_TS_DIR / "tsconfig.json")]
        subprocess.run(cmd, check=True)

    return {
        "actions": [compile_typescript],
        "file_dep": [str(f) for f in ts_files]
        + [str(FRONTEND_TS_DIR / "tsconfig.json")],
        "targets": [str(FRONTEND_JS_DIR / "wasm-loader.js")],
        "clean": True,
        "verbosity": 2,
    }


def task_build_parcel_dev():
    """Build frontend assets using Parcel (development mode)."""

    def run_parcel_dev() -> None:
        """Run Parcel in development mode."""
        os.chdir(WORKSPACE_ROOT)
        entry_html = FRONTEND_TS_DIR / "index.html"
        cmd = [
            "npx",
            "parcel",
            "build",
            str(entry_html),
            "--dist-dir",
            str(FRONTEND_JS_DIR / "dist"),
        ]
        subprocess.run(cmd, check=True)

    return {
        "actions": [run_parcel_dev],
        "file_dep": get_ts_files() + get_scss_files(),
        "targets": [str(FRONTEND_JS_DIR / "dist" / "index.html")],
        "task_dep": ["compile_proto_as"],
        "clean": True,
        "verbosity": 2,
    }


def task_build_parcel_prod():
    """Build frontend assets using Parcel (production mode)."""

    def run_parcel_prod() -> None:
        """Run Parcel in production mode."""
        os.chdir(WORKSPACE_ROOT)
        entry_html = FRONTEND_TS_DIR / "index.html"
        cmd = [
            "npx",
            "parcel",
            "build",
            str(entry_html),
            "--dist-dir",
            str(FRONTEND_JS_DIR / "dist-prod"),
        ]
        subprocess.run(cmd, check=True)

    return {
        "actions": [run_parcel_prod],
        "file_dep": get_ts_files() + get_scss_files(),
        "targets": [str(FRONTEND_JS_DIR / "dist-prod" / "index.html")],
        "task_dep": ["compile_proto_as"],
        "clean": True,
        "verbosity": 2,
    }


# =============================================================================
# Meta Tasks
# =============================================================================


def task_build_all_dev():
    """Build all assets for development."""
    return {
        "actions": None,
        "task_dep": [
            "compile_proto_python",
            "compile_proto_as",
            "generate_proto_as",
            "copy_as_proto_runtime",
            "compile_wasm_debug",
            "build_scss",
            "build_typescript",
            "build_parcel_dev",
        ],
        "verbosity": 2,
    }


def task_build_all_prod():
    """Build all assets for production."""
    return {
        "actions": None,
        "task_dep": [
            "compile_proto_python",
            "compile_proto_as",
            "generate_proto_as",
            "copy_as_proto_runtime",
            "compile_wasm_release",
            "build_scss",
            "build_typescript",
            "build_parcel_prod",
        ],
        "verbosity": 2,
    }


def task_clean_all():
    """Clean all build artifacts."""

    def clean_artifacts() -> None:
        """Remove all build artifacts."""
        import shutil

        # Clean protobuf generated files
        for pb_file in PROTOBUF_DIR.glob("*_pb2.py"):
            pb_file.unlink(missing_ok=True)
        for pyi_file in PROTOBUF_DIR.glob("*_pb2.pyi"):
            pyi_file.unlink(missing_ok=True)

        # Clean WASM build directory
        if (FRONTEND_AS_DIR / "build").exists():
            shutil.rmtree(FRONTEND_AS_DIR / "build")

        # Clean frontend build artifacts
        if (FRONTEND_JS_DIR / "dist").exists():
            shutil.rmtree(FRONTEND_JS_DIR / "dist")
        if (FRONTEND_JS_DIR / "dist-dev").exists():
            shutil.rmtree(FRONTEND_JS_DIR / "dist-dev")
        if (FRONTEND_JS_DIR / "dist-prod").exists():
            shutil.rmtree(FRONTEND_JS_DIR / "dist-prod")

        # Clean compiled CSS
        (FRONTEND_CSS_DIR / "main.css").unlink(missing_ok=True)
        (FRONTEND_CSS_DIR / "main.css.map").unlink(missing_ok=True)

        # Clean TypeScript compiled JS
        for js_file in FRONTEND_JS_DIR.glob("*.js"):
            if js_file.name != "obligation-list.js":  # Keep existing JS files
                js_file.unlink(missing_ok=True)

    return {
        "actions": [clean_artifacts],
        "verbosity": 2,
    }


# Doit configuration
DODOFILE_ENCODING = "utf-8"
