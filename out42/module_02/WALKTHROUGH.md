# Module 02: Garden Guardian (exceptions)

Every file in this module was run against the subject's sample outputs, and
`flake8` is clean on all of them. `mypy --strict` is clean too, except for the one line the subject asks
you to keep broken (`"abc" + 5` in ex2).

**Before you read: how to use this for your defense.** Your own AI rules
say you must be able to explain everything you hand in. So: read a
program, close this file, retype it from memory, run it, then explain it
out loud to a peer. Where I made a design choice that the subject leaves
open, I flag it with **[choice]**, so you can defend or change it.

Concepts that come back all the time:

- **f-string**: `f"x is {x}"` puts the value of `x` inside the text.
- **Type hint**: `name: str` / `-> None` are labels for mypy. Python ignores them
  at runtime.
- **`if __name__ == "__main__":`**: `__name__` is `"__main__"` only when the
  file is run directly (`python3 file.py`), not when it is imported by
  another file. It lets a file be both a program and a reusable module.
- **Exception**: an error object that travels up the call stack until some
  `except` catches it; if nobody does, the program crashes.

---

Vocabulary: **try** = code that may fail; **except X** = what to do if an
`X` error happens; **raise** = create an error on purpose; **finally** =
runs no matter what.

## ex0: ft_first_exception.py

```python
def input_temperature(temp_str: str) -> int:
    return int(temp_str)
```
Converts a string to an integer. It does **not** catch anything: it lets
the error travel up to the caller. `int("abc")` raises `ValueError`
(`int(None)` would raise `TypeError`, but with `temp_str: str` only
`ValueError` is realistic, so that is what we catch).

```python
def test_temperature() -> None:
    print("=== Garden Temperature ===")
    for value in ["25", "abc"]:
        print()
        print(f"Input data is '{value}'")
        try:
            temperature: int = input_temperature(value)
            print(f"Temperature is now {temperature}°C")
        except ValueError as error:
            print(f"Caught input_temperature error: {error}")
    print()
    print("All tests completed - program didn't crash!")
```
Looping over a list avoids copying the same block twice. If
`input_temperature` raises, the rest of the `try` body is skipped, the
`except` runs, then the loop continues with the next value: that is "the
program keeps running". `{error}` prints the message from the sample.

## ex1: ft_raise_exception.py

```python
    temperature: int = int(temp_str)
    if temperature > 40:
        raise ValueError(f"{temperature}°C is too hot for plants (max 40°C)")
    if temperature < 0:
        raise ValueError(f"{temperature}°C is too cold for plants (min 0°C)")
    return temperature
```
`raise ValueError("message")` builds an error and throws it. We reuse
`ValueError` ("the value is unacceptable") so the caller can use one
`except ValueError` for both bad text and out-of-range numbers. The limits
0 and 40 are *included* as valid, hence strict `>` and `<`. The test list
gains `"100"` and `"-50"`.

## ex2: ft_different_errors.py

```python
def garden_operations(operation_number: int) -> None:
    if operation_number == 0:
        int("abc")               # ValueError
    elif operation_number == 1:
        10 / 0                   # ZeroDivisionError
    elif operation_number == 2:
        open("/non/existent/file")   # FileNotFoundError
    elif operation_number == 3:
        "abc" + 5                # TypeError
```
Each branch is deliberately faulty. Other numbers do nothing and return.
The bare expressions (not assigned to a variable) keep flake8 quiet about
unused variables. The open that fails never produced a file, so nothing to
close. mypy rightly reports `"abc" + 5` as an error, and the subject tells
you to leave it (adding `# type: ignore` at the end of that line would
silence it, but then you wouldn't show the "mypy error on purpose").

```python
        try:
            garden_operations(operation)
            print("Operation completed successfully")
        except ValueError as error:
            ...
        except ZeroDivisionError as error:
            ...
```
Several `except` clauses on one `try` are checked **in order**; the first
matching one runs. Python has different exception *types* so you can react
differently to different problems (retry on network errors, fix input on
ValueError...). The success message only prints when nothing was raised.

```python
        except (ValueError, ZeroDivisionError,
                FileNotFoundError, TypeError) as error:
```
A **tuple** of types catches several kinds with a single `except`, the
"multiple types with one try" requirement (you can't print the type name
here without `type()`, which is banned, so the message alone is printed).

## ex3: ft_custom_errors.py

```python
class GardenError(Exception):
    default_message: str = "Unknown garden error"

    def __str__(self) -> str:
        if self.args:
            return str(self.args[0])
        return self.default_message
```
- `class GardenError(Exception)`: inheriting from `Exception` makes it a
  real exception.
- `self.args` is the tuple of arguments given at `raise`. If a message was
  provided it is used, otherwise the class's `default_message`.
- `__str__` is what `print(error)` / `f"{error}"` call.

```python
class PlantError(GardenError):
    default_message: str = "Unknown plant error"
```
Child class: it inherits `__str__` and only overrides the default text.
`WaterError` is the same idea. **[choice]** I avoided `__init__` + `super()`
because only `print()` is authorized; the alternative is
`def __init__(self, message="Unknown plant error"): super().__init__(message)`.

**Why inheritance helps:** `except GardenError` catches `PlantError` *and*
`WaterError`, because a `PlantError` *is a* `GardenError`. You can catch
precisely (`except PlantError`) or broadly (`except GardenError`). **When to
make your own errors:** when built-in names are too vague, or when you want
callers to catch "everything that comes from my garden code" without also
catching unrelated bugs.

The functions `raise_plant_error` / `raise_water_error` raise them. In
`test_custom_errors`, the last loop does `raise error_class()` on the *class*
(calling it creates an instance with no message) to show the default texts.

## ex4: ft_finally_block.py

The exercise needs `PlantError` from the previous one, but each exercise
must be a standalone file, so the classes are copied (only the two needed).

```python
def water_plant(plant_name: str) -> None:
    if plant_name == "" or plant_name != plant_name.capitalize():
        raise PlantError(f"Invalid plant name to water: '{plant_name}'")
    print(f"Watering {plant_name}: [OK]")
```
"Capitalized" means equal to its own `.capitalize()`. `"lettuce"` becomes
`"Lettuce"`, which differs, so error. `"TOMATO"` also fails (the rest must be
lowercase). The empty string is explicitly rejected.

```python
    tests = [("valid", [...]), ("invalid", [...])]
    for label, plants in tests:
        print()
        print(f"Testing {label} plants...")
        print("Opening watering system")
        try:
            for plant in plants:
                water_plant(plant)
        except PlantError as error:
            print(f"Caught PlantError: {error}")
            print(".. ending tests and returning to main")
            return
        finally:
            print("Closing watering system")
```
The key point: **`finally` runs in every case**: no error, an error that
was caught, an error that was not caught, even when there's a `return` in
the `except` block. In the "invalid" run the order is: error caught, the
two messages printed, `return` starts leaving the function, **then** the
`finally` prints "Closing watering system", then the function really ends
and `main` prints "Cleanup always happens...". That is why `finally` is the
right place for cleanup (closing files, releasing connections, stopping
the water): you can't forget it on some path.

---
# Things evaluators like to ask

1. `except Exception` vs a specific one? (specific = you know what failed)
2. What does `finally` guarantee, even with `return`?
