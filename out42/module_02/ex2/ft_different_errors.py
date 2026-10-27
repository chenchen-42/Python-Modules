def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("abc")
    elif operation_number == 1:
        10 / 0
    elif operation_number == 2:
        open("/non/existent/file")
    elif operation_number == 3:
        "abc" + 5


def test_error_types() -> None:
    print("=== Garden Error Types Demo ===")
    for operation in [0, 1, 2, 3, 4]:
        print(f"Testing operation {operation}...")
        try:
            garden_operations(operation)
            print("Operation completed successfully")
        except ValueError as error:
            print(f"Caught ValueError: {error}")
        except ZeroDivisionError as error:
            print(f"Caught ZeroDivisionError: {error}")
        except FileNotFoundError as error:
            print(f"Caught FileNotFoundError: {error}")
        except TypeError as error:
            print(f"Caught TypeError: {error}")

    print()
    print("Catching several error types with a single try block:")
    for operation in [0, 1, 2, 3]:
        try:
            garden_operations(operation)
        except (ValueError, ZeroDivisionError,
                FileNotFoundError, TypeError) as error:
            print(f"Operation {operation} failed, caught: {error}")

    print()
    print("All error types tested successfully!")


if __name__ == "__main__":
    test_error_types()
