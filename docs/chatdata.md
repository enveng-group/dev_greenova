<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Install Protoc](#install-protoc)
- [Compile with Protoc](#compile-with-protoc)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Install Protoc

Install protoc from the github <https://github.com/protocolbuffers/protobuf>

# Compile with Protoc

protoc --proto_path=./greenova/chatbot/ --python_out=./greenova/chatbot/
./greenova/chatbot/chatdata.proto
