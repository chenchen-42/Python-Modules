def input_temperature(temp_str: str) -> int:
    temp = int(temp_str)
    if temp > 40:
      raise ValueError (f"{temp} ºC is too hot for plants (max 40ºC)")
    if temp < 0:
      raise ValueError (f"{temp} ºC is too cold for plants (max 0ºC)")
    return temp


def test_temperature() -> None:
    print("=== Garden Temperature ===")
    print("")
    temperature = ["25", "abc", "100", "-50"]
    for values in temperature:
      print(f"Input data is '{values}'")    
      try:
        test = input_temperature(values)    
        print(f"Temperature is now {values}°C\n")
      except ValueError as error:
        print(f"Caught input_temperature error: {error}\n")
    print("All tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()
