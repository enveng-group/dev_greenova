<<<<<<< HEAD
||||||| parent of 37e6b25 (Squashed commit of the following:)
=======
<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Protobuf Compiler (protoc)](#protobuf-compiler-protoc)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

>>>>>>> 37e6b25 (Squashed commit of the following:)
<!--
 Copyright 2025 Enveng Group.
 SPDX-License-Identifier: 	AGPL-3.0-or-later
-->

# Protobuf Compiler (protoc)

```fish
python -m grpc_tools.protoc \
  --proto_path=greenova \
  --python_out=greenova \
  --grpc_python_out=greenova \
  chatbot/proto/chatbot.proto \
  feedback/proto/feedback.proto \
  dashboard/proto/overdue_obligations.proto \
  mechanisms/proto/mechanism.proto
```
