def input_temperature(temp_str: str) -> int:
    temp = int(temp_str)
    return temp


def test_temperature() -> None:
    print("=== Garden Temperature ===")
    print("")
    print("Input data is '25'")
    valid_temp = input_temperature("25")
    print(f"Temperature is now {valid_temp}°C")
    print("")
    print("Input data is 'abc'")
    try:
        invalid_temp = input_temperature("abc")
        print(f"Temperature is now {invalid_temp}°C")
    except ValueError as error:
        print(f"Caught input_temperature error: {error}")
    print("")
    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()
