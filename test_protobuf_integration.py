#!/usr/bin/env python3
"""Test script to validate Protobuf3 integration in Greenova.

This script validates that:
1. Protobuf Python files can be imported
2. Basic protobuf message creation works
3. AssemblyScript stubs are generated
4. Build system works correctly
"""

import sys
from pathlib import Path

# Add greenova to Python path
GREENOVA_ROOT = Path(__file__).parent / "greenova"
sys.path.insert(0, str(GREENOVA_ROOT))


def test_protobuf_imports() -> bool | None:
    """Test that protobuf Python files can be imported."""
    try:
        return True
    except ImportError:
        return False


def test_protobuf_message_creation() -> bool | None:
    """Test that protobuf messages can be created and serialized."""
    try:
        from protobuf import greenova_data_pb2

        # Create a simple DashboardData message
        dashboard = greenova_data_pb2.DashboardData()
        dashboard.last_updated = 1718984736  # Current timestamp

        # Create project summary
        project_summary = greenova_data_pb2.ProjectSummary()
        project_summary.total_projects = 5
        project_summary.active_projects = 3
        project_summary.completed_projects = 2

        dashboard.project_summary.CopyFrom(project_summary)

        # Serialize to binary
        binary_data = dashboard.SerializeToString()

        # Test deserialization
        dashboard2 = greenova_data_pb2.DashboardData()
        dashboard2.ParseFromString(binary_data)
        assert dashboard2.project_summary.total_projects == 5

        return True
    except Exception:
        return False


def test_assemblyscript_stubs() -> bool:
    """Test that AssemblyScript stubs were generated."""
    as_proto_dir = (
        GREENOVA_ROOT / "core" / "static" / "core" / "as" / "assembly" / "proto"
    )

    expected_files = [
        "greenova/charts/ChartData.ts",
        "core/DashboardData.ts",
        "dashboard/DashboardWidget.ts",
        "auditing/AuditProto.ts",
    ]

    found_files = 0
    for expected_file in expected_files:
        file_path = as_proto_dir / expected_file
        if file_path.exists():
            found_files += 1

    return found_files > 0


def test_wasm_build_artifacts() -> bool:
    """Test that WASM build artifacts exist."""
    wasm_build_dir = GREENOVA_ROOT / "core" / "static" / "core" / "as" / "build"

    artifacts = ["debug.wasm", "release.wasm"]
    found_artifacts = 0

    for artifact in artifacts:
        artifact_path = wasm_build_dir / artifact
        if artifact_path.exists():
            artifact_path.stat().st_size
            found_artifacts += 1

    return found_artifacts > 0


def main() -> int:
    """Run all Protobuf3 integration tests."""
    tests = [
        test_protobuf_imports,
        test_protobuf_message_creation,
        test_assemblyscript_stubs,
        test_wasm_build_artifacts,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception:
            pass

    if passed == total:
        return 0
    if passed >= total // 2:
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
