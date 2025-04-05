#!/usr/bin/env python3
"""
Fix for hyperscript_dump.py type annotation syntax for Python 3.9 compatibility.
"""
import logging
import os
import re
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def fix_hyperscript_dump():
    """Fix type annotation syntax in hyperscript_dump.py for Python 3.9."""
    # Get the virtual environment path
    venv_path = os.environ.get('VIRTUAL_ENV', '/workspaces/greenova/.venv')

    # Sanitize and validate the virtual environment path
    allowed_base_path = Path('/workspaces/greenova/.venv').resolve()
    try:
        venv_path = Path(venv_path).resolve(strict=True)
        if not venv_path.is_dir() or not str(venv_path).startswith(str(allowed_base_path)):
            raise ValueError(f'Unsafe or invalid virtual environment path: {venv_path}')
    except (ValueError, FileNotFoundError) as e:
        logger.error(str(e))
        return False

    file_path = venv_path / 'lib' / 'python3.9' / 'site-packages' / 'hyperscript_dump.py'

    if not file_path.exists():
        logger.info(f'File not found: {file_path}')
        return True

    logger.info(f'Found hyperscript_dump.py at {file_path}')

    # Read the file
    # Ensure the file path is within the expected directory
    try:
        with open(file_path, encoding='utf-8') as f:
            pass  # Placeholder for actual file handling logic
    except FileNotFoundError:
        logger.error(f'Invalid or unsafe file path: {file_path}')
        return False

    with open(file_path) as f:
        content = f.read()

    # Check if the file already imports Union
    imports_union = re.search(r'from\s+typing\s+import\s+.*Union.*', content) is not None

    # Replace the pipe syntax with Union
    pattern = r'event:\s*str\s*\|\s*None\s*='
    replacement = 'event: Union[str, None] ='

    if re.search(pattern, content):
        # Add Union import if needed
        if not imports_union:
            if 'from typing import' in content:
                content = re.sub(
                    r'from\s+typing\s+import\s+(.*)',
                    r'from typing import \1, Union',
                    content
                )
            else:
                content = re.sub(
                    r'import json',
                    r'import json\nfrom typing import Union',
                    content
                )
        with open(file_path, 'w', encoding='utf-8') as f:
            # Replace the type annotation
            content = re.sub(pattern, replacement, content)

        # Write the fixed content back
        with open(file_path, 'w') as f:
            f.write(content)
        logger.info('Successfully fixed the type annotation in hyperscript_dump.py')
        return True
    else:
        logger.info("No type annotation issue found or it's already fixed")
        return True

if __name__ == '__main__':
    success = fix_hyperscript_dump()
    sys.exit(0 if success else 1)
