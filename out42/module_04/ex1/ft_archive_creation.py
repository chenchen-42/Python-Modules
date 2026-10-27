import sys
from typing import IO


def read_file(filename: str) -> str | None:
    file: IO[str]
    try:
        file = open(filename, "r")
    except OSError as error:
        print(f"Error opening file '{filename}': {error}")
        return None

    try:
        content: str = file.read()
    except (OSError, UnicodeDecodeError) as error:
        print(f"Error reading file '{filename}': {error}")
        file.close()
        return None

    print("---")
    print()
    print(content)
    print("---")
    file.close()
    print(f"File '{filename}' closed.")
    return content


def transform(content: str) -> str:
    result: str = ""
    for line in content.splitlines():
        result += line + "#\n"
    return result


def save_file(filename: str, data: str) -> None:
    print(f"Saving data to '{filename}'")
    file: IO[str]
    try:
        file = open(filename, "w")
    except OSError as error:
        print(f"Error opening file '{filename}': {error}")
        print("Data not saved.")
        return

    try:
        file.write(data)
    except OSError as error:
        print(f"Error writing file '{filename}': {error}")
        print("Data not saved.")
        file.close()
        return

    file.close()
    print(f"Data saved in file '{filename}'.")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: ft_archive_creation.py <file>")
        return

    filename: str = sys.argv[1]
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{filename}'")

    content: str | None = read_file(filename)
    if content is None:
        return

    print()
    print("Transform data:")
    new_content: str = transform(content)
    print("---")
    print()
    print(new_content)
    print("---")

    try:
        new_name: str = input("Enter new file name (or empty): ")
    except EOFError:
        new_name = ""
    if new_name == "":
        print("Not saving data.")
    else:
        save_file(new_name, new_content)


if __name__ == "__main__":
    main()
