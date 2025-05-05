#!/usr/bin/env fish

# Define the target directory
set target_dir "greenova/"

# Define code patterns to search for
set code_patterns "**tests**.py"

# Use the find command to locate files matching the specified patterns in their source code
# and print their paths
for pattern in $code_patterns
    find $target_dir -type f -exec grep -l $pattern {} \;
end
