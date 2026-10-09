def input_temperature(temp_str: str) -> int:
    temp = int(temp_str)
    return temp


def test_temperature() -> None:
    print("=== Garden Temperature ===")
    print("")
    temperature = ["25", "abc"]
    for values in temperature:
      print(f"Input data is '{values}'")    
      try:
        test = input_temperature(values)    
        print(f"Temperature is now {values}°C\n")
      except ValueError as error:
        print(f"Caught input_temperature error: {error}")
    print("")
    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()
