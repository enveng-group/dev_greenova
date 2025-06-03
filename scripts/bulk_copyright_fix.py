#!/usr/bin/env python3
"""Script to bulk add copyright notices to all files flagged by ruff CPY001."""


# Copyright notice template
COPYRIGHT_NOTICE = '''"""
Copyright (C) 2025 Adrian Gallo

This file is part of Greenova.

Greenova is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Greenova is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Greenova. If not, see <https://www.gnu.org/licenses/>.

Author: Adrian Gallo <agallo@enveng-group.com.au>
"""

'''


def extract_file_paths(ruff_log_content: str) -> list[str]:
    """Extract file paths from ruff log content."""
    file_paths = []
    for line in ruff_log_content.strip().split("\n"):
        if "CPY001 Missing copyright notice at top of file" in line:
            # Extract the file path (everything before the first colon)
            file_path = line.split(":")[0]
            file_paths.append(file_path)
    return file_paths


def add_copyright_to_file(file_path: str) -> bool | None:
    """Add copyright notice to the beginning of a file."""
    full_path = f"/workspaces/greenova/{file_path}"

    try:
        # Read current content
        with open(full_path, encoding="utf-8") as f:
            content = f.read()

        # Add copyright notice at the beginning
        new_content = COPYRIGHT_NOTICE + content

        # Write back to file
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(new_content)

        return True

    except Exception:
        return False


def main() -> None:
    """Main function to process all files."""
    # Read ruff log
    ruff_log_path = "/workspaces/greenova/ruff.log"

    try:
        with open(ruff_log_path, encoding="utf-8") as f:
            ruff_content = f.read()
    except Exception:
        return

    # Extract file paths
    file_paths = extract_file_paths(ruff_content)

    # Process each file
    success_count = 0
    for file_path in file_paths:
        if add_copyright_to_file(file_path):
            success_count += 1


if __name__ == "__main__":
    main()
