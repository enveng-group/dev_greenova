#!/usr/bin/env python3
"""build_frontend.py - Unified frontend build for Greenova.

Compiles AssemblyScript, SASS+Tailwind+PicoCSS, and bundles all vendor JS/CSS into dist/
Usage: python scripts/build_frontend.py
"""

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / "greenova" / "static"
DIST = STATIC / "dist"
GENERATED = STATIC / "as" / "generated"

PROTO_DIRS = [
    ROOT / "greenova" / "company" / "proto" / "company.proto",
    ROOT / "greenova" / "projects" / "proto" / "projects.proto",
    ROOT / "greenova" / "users" / "proto" / "users.proto",
    ROOT / "greenova" / "auditing" / "proto" / "auditing.proto",
    ROOT / "greenova" / "obligations" / "proto" / "obligations.proto",
    ROOT / "greenova" / "mechanisms" / "proto" / "mechanism.proto",
    ROOT / "greenova" / "feedback" / "proto" / "feedback.proto",
    ROOT / "greenova" / "chatbot" / "proto" / "chatbot.proto",
]


def run(cmd, cwd=None, check=True) -> None:
    subprocess.run(cmd, cwd=cwd, check=check)


def main() -> None:
    # 1. Compile AssemblyScript to WASM/JS
    run(
        [
            "npx",
            "asc",
            str(STATIC / "as" / "assembly" / "index.ts"),
            "--outFile",
            str(DIST / "optimized.wasm"),
            "--optimize",
            "--sourceMap",
            "--exportRuntime",
        ],
    )

    # 2. Generate JS Protobuf classes using protobufjs
    GENERATED.mkdir(parents=True, exist_ok=True)
    pbjs_out = GENERATED / "greenova_pb.js"
    pbts_out = GENERATED / "greenova_pb.d.ts"
    run(
        [
            "npx",
            "pbjs",
            "-t",
            "static-module",
            "-w",
            "commonjs",
            "-o",
            str(pbjs_out),
        ]
        + [str(p) for p in PROTO_DIRS],
    )
    run(["npx", "pbts", "-o", str(pbts_out), str(pbjs_out)])

    # 2b. Compile TypeScript glue code to JavaScript
    run(
        [
            "npx",
            "tsc",
            "-p",
            str(STATIC / "as" / "tsconfig.glue.json"),
        ],
    )

    # 3. Build frontend CSS (SASS + Tailwind + PicoCSS)
    run(["npm", "run", "build:frontend"])

    # 3b. Copy built CSS to dist/
    DIST.mkdir(parents=True, exist_ok=True)
    css_src = STATIC / "css" / "dist" / "styles.css"
    css_dst = DIST / "styles.css"
    if css_src.exists():
        css_dst.write_bytes(css_src.read_bytes())

    # 4. Bundle/copy all vendor JS and CSS
    vendors_src = STATIC / "js" / "vendors"
    vendors_dst = DIST / "vendors"
    vendors_dst.mkdir(parents=True, exist_ok=True)
    if vendors_src.exists():
        for item in vendors_src.iterdir():
            target = vendors_dst / item.name
            if item.is_dir():
                if target.exists():
                    import shutil

                    shutil.rmtree(target)
                shutil.copytree(item, target)
            else:
                import shutil

                shutil.copy2(item, target)
    pico_src = STATIC / "css" / "vendor" / "pico-classless.min.css"
    pico_dst = vendors_dst / "pico-classless.min.css"
    if pico_src.exists():
        import shutil

        shutil.copy2(pico_src, pico_dst)


if __name__ == "__main__":
    main()
