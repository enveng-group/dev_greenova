#!/usr/bin/env fish

# Define the target directory
set target_dir "greenova/"

# Use the find command to locate files matching the specified patterns
find $target_dir \( -name "**test**.py" \) -print
