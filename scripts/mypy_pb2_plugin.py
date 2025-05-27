"""MyPy plugin to handle protobuf-generated files."""

from mypy.nodes import MypyFile
from mypy.plugin import Plugin


class ProtobufPlugin(Plugin):
    """Plugin to handle protobuf-generated files."""

    def get_additional_deps(self, file: MypyFile) -> list[tuple[int, str, int]]:
        """Skip checking dependencies for protobuf files."""
        if file.path and file.path.endswith("_pb2.py"):
            return []
        return super().get_additional_deps(file)


def plugin(version: str) -> type[Plugin]:
    """Return the plugin type."""
    return ProtobufPlugin
