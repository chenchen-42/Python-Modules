import sys
from typing import IO


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_ancient_text.py <file>")
        return

    filename: str = sys.argv[1]
    print("=== Cyber Archives Recovery ===")
    print(f"Accessing file '{filename}'")

    file: IO[str]
    try:
        file = open(filename, "r")
    except OSError as error:
        print(f"Error opening file '{filename}': {error}")
        return

    try:
        content: str = file.read()
    except (OSError, UnicodeDecodeError) as error:
        print(f"Error reading file '{filename}': {error}")
        file.close()
        return

    print("---")
    print()
    print(content)
    print("---")
    file.close()
    print(f"File '{filename}' closed.")


if __name__ == "__main__":
    main()
