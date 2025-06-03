import os


def main() -> None:
    """Copy the project .bashrc to the user's home directory for the devcontainer.

    Overwrites any existing ~/.bashrc file.
    """
    src = "/workspaces/greenova/.dotfiles/.bashrc"
    dest = os.path.expanduser("~/.bashrc")

    # Ensure the source file exists
    if not os.path.isfile(src):
        msg = f"Source .bashrc not found at {src}"
        raise FileNotFoundError(msg)

    # Copy with UTF-8 encoding
    with open(src, encoding="utf-8") as fsrc, \
            open(dest, "w", encoding="utf-8") as fdest:
        fdest.write(fsrc.read())


if __name__ == "__main__":
    main()
