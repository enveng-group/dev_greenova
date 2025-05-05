# EditorConfig

## Overview

EditorConfig helps maintain consistent coding styles across various editors and IDEs.
It consists of a file format for defining coding styles and a collection of text
editor plugins that enable editors to read the file format and adhere to defined
styles.
In collaborative projects like Greenova, consistent code formatting is essential
for:

## Why EditorConfig Matters

In collaborative projects like Greenova, consistent code formatting is essential for:

- **Readability**: Consistent indentation and line endings make code easier to read
- **Collaboration**: Reduces merge conflicts caused by formatting differences
- **Onboarding**: New team members can immediately follow project conventions
- **Focus**: Spend less time discussing style and more time on functionality

## How EditorConfig Works

1. A `.editorconfig` file defines coding styles for different file types
2. When you open a file in an editor with EditorConfig support, it reads the configuration
   Our project uses a comprehensive `.editorconfig` file with specific settings for
   different file types:

## Greenova's EditorConfig Configuration

Our project uses a comprehensive `.editorconfig` file with specific settings for different file types:

### Python Configuration

```editorconfig
[*.py]
indent_size = 4
max_line_length = 88
profile = black
```

This configuration:

- Uses 4 spaces for indentation
- Limits line length to 88 characters
- Follows Black code style conventions

### HTML/Django Templates

```editorconfig
[*.{html,htm,djhtml}]
indent_size = 2
max_line_length = 88
```

### JavaScript and CSS

```editorconfig
[*.{js,jsx,ts,tsx}]
indent_size = 2
max_line_length = 80

[*.{css,scss,sass,less}]
indent_size = 2
max_line_length = 80
```

### Other Formats

The configuration includes specific settings for JSON, YAML, Markdown, shell scripts, and more. See the full `.editorconfig` file for details.
Most popular editors and IDEs support EditorConfig either natively or through
plugins:

## Using EditorConfig

### Editor Support

Most popular editors and IDEs support EditorConfig either natively or through plugins:

- **VS Code**: Install the "EditorConfig for VS Code" extension
- **PyCharm/JetBrains IDEs**: Built-in support
- **Sublime Text**: Install the "EditorConfig" package
- **Vim**: Install the "editorconfig-vim" plugin
- **Emacs**: Install the "editorconfig-emacs" package
- **Atom**: Install the "editorconfig" package

### Installing the Python Package

If you need programmatic access to EditorConfig functionality:

```bash
pip install editorconfig
```

### Using the Command Line Tool

After installing the Python package:

```bash
editorconfig /path/to/file
```

1. **Verify Plugin Installation**: Ensure your editor has the EditorConfig plugin
   installed and enabled
2. **Check File Location**: The `.editorconfig` file must be in your project root
   or a parent directory

## Troubleshooting

### EditorConfig Not Working

- **Black**: Our `.editorconfig` is configured with `profile = black` to align
  with Black's formatting
- **Prettier**: For frontend files, ensure Prettier is configured to respect
  `.editorconfig` settings

3. **Validate Syntax**: Use an online validator to check your `.editorconfig` file

### Conflicts with Other Formatting Tools

In the Greenova project:

- **Black**: Our `.editorconfig` is configured with `profile = black` to align with Black's formatting
- **Prettier**: For frontend files, ensure Prettier is configured to respect `.editorconfig` settings
  For Django projects like Greenova, EditorConfig helps maintain consistent
  formatting across:

## Further Reading

- [Official EditorConfig Website](https://editorconfig.org/)
- [Python EditorConfig Package](https://pypi.org/project/EditorConfig/)
- [EditorConfig Core Python](https://github.com/editorconfig/editorconfig-core-py)
  This consistency supports our HTML-first development approach and progressive
  enhancement layers by ensuring all code follows the same structural conventions
  regardless of which team member created it.

## Integration with Django Development

For Django projects like Greenova, EditorConfig helps maintain consistent formatting across:

1. **Python Files**: Models, views, forms, and utility functions
2. **HTML Templates**: Django templates with proper indentation
3. **JavaScript/CSS**: Frontend asset formatting
4. **Configuration Files**: Settings files, URLs, and routing

This consistency supports our HTML-first development approach and progressive enhancement layers by ensuring all code follows the same structural conventions regardless of which team member created it.
