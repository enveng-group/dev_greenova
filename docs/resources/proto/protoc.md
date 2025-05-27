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
