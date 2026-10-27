def secure_archive(
    filename: str,
    action: str = "read",
    content: str = "",
) -> tuple[bool, str]:
    try:
        if action == "read":
            with open(filename, "r") as file:
                return (True, file.read())
        if action == "write":
            with open(filename, "w") as file:
                file.write(content)
            return (True, "Content successfully written to file")
        return (False, f"Unknown action '{action}' (use 'read' or 'write')")
    except (OSError, UnicodeError) as error:
        return (False, str(error))


def main() -> None:
    print("=== Cyber Archives Security ===")

    print("\nUsing 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file"))

    print("\nUsing 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("/etc/shadow"))

    print("\nUsing 'secure_archive' to read from a regular file:")
    result: tuple[bool, str] = secure_archive("ancient_fragment.txt")
    print(result)

    print("\nUsing 'secure_archive' to write previous content to a new file:")
    print(secure_archive("new_fragment.txt", "write", result[1]))


if __name__ == "__main__":
    main()
