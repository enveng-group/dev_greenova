<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Protobuf3 Client Integration for Greenova](#protobuf3-client-integration-for-greenova)
  - [Overview](#overview)
  - [Build Process (as of June 2025)](#build-process-as-of-june-2025)
    - [What the build does](#what-the-build-does)
  - [Usage Pattern](#usage-pattern)
    - [1. Generate JS Protobuf Classes](#1-generate-js-protobuf-classes)
    - [2. Import and Use in JS Glue Code](#2-import-and-use-in-js-glue-code)
    - [3. AssemblyScript Interop](#3-assemblyscript-interop)
    - [4. Endpoints](#4-endpoints)
  - [Example Endpoints](#example-endpoints)
  - [Notes](#notes)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Protobuf3 Client Integration for Greenova

This document describes how to use protobuf3 for client-server communication in the Greenova Django application, using JavaScript (protobufjs) and AssemblyScript glue code.

## Overview

- All major Django apps (feedback, obligations, mechanisms, etc.) expose endpoints for exporting/importing protobuf3 binary data.
- The client uses AssemblyScript for core logic and JS glue code for protobuf3 serialization/deserialization and HTTP requests.
- Protobuf message classes are generated for JavaScript using [protobufjs](https://github.com/protobufjs/protobuf.js) (`pbjs`/`pbts`).

## Build Process (as of June 2025)

- The unified frontend build is now managed by `scripts/build_frontend.py` (Python).
- The old `build_frontend.sh` is deprecated and should be removed.
- To build all frontend assets, run:

```sh
python3 scripts/build_frontend.py
```

- Or use the VS Code task: **Build Frontend** (runs the same script).

### What the build does

1. Compiles AssemblyScript to WASM/JS
2. Generates JS Protobuf classes using protobufjs (`pbjs`/`pbts`)
3. Builds frontend CSS (SASS + Tailwind + PicoCSS)
4. Bundles/copies all vendor JS and CSS

## Usage Pattern

### 1. Generate JS Protobuf Classes

- Compile `.proto` files using `pbjs`/`pbts` (protobufjs).
- Place generated files in `static/as/generated/`.
- This is automated in `scripts/build_frontend.py`:

```sh
python3 scripts/build_frontend.py
```

### 2. Import and Use in JS Glue Code

```js
const { BugReportProto } = require('./generated/greenova_pb');
const { sendProtobuf, fetchProtobuf } = require('./protobuf_integration.js');

// Upload a bug report
async function uploadBugReport(report) {
  const binary = BugReportProto.encode(report).finish();
  const status = await sendProtobuf('/feedback/import/', binary);
  // handle status
}

// Download a bug report
async function downloadBugReport(id) {
  const binary = await fetchProtobuf(`/feedback/export/${id}/`);
  const report = BugReportProto.decode(new Uint8Array(binary));
  // use report
}
```

### 3. AssemblyScript Interop

- Use the JS glue code to bridge between AssemblyScript and protobufjs for sending/fetching protobuf data.
- All protobuf parsing/serialization is handled in JavaScript.

### 4. Endpoints

- All import endpoints accept `application/octet-stream` POSTs with protobuf3 binary.
- All export endpoints return `application/octet-stream` with protobuf3 binary.

## Example Endpoints

- `/feedback/export/<id>/` and `/feedback/import/`
- `/obligations/export/<id>/` and `/obligations/import/`
- `/mechanisms/export/<id>/` and `/mechanisms/import/`

## Notes

- Always use `Uint8Array` or `ArrayBuffer` for binary data.
- Use CSRF tokens if required for POST requests.
- See `protobuf_integration.js` for integration patterns.
- TypeScript/ts-proto is no longer used; all protobuf integration is via JavaScript and protobufjs.
- The build process is now Python-based for cross-platform compatibility.
