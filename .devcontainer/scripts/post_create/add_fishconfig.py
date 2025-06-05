import os


def main() -> None:
    """Copy the project fish.config to the user's home directory for the devcontainer.

    Overwrites any existing ~/.config/fish/fish.config file.
    """
    src = "/workspaces/greenova/.dotfiles/fish.config"
    dest = os.path.expanduser("~/.config/fish/fish.config")
    dest_dir = os.path.dirname(dest)

    # Ensure the source file exists
    if not os.path.isfile(src):
        msg = f"Source fish.config not found at {src}"
        raise FileNotFoundError(msg)

    # Ensure the destination directory exists
    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)

    # Copy with UTF-8 encoding
    with open(src, encoding="utf-8") as fsrc, \
            open(dest, "w", encoding="utf-8") as fdest:
        fdest.write(fsrc.read())


if __name__ == "__main__":
    main()
