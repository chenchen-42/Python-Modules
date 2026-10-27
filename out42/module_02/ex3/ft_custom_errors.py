class GardenError(Exception):
    default_message: str = "Unknown garden error"

    def __str__(self) -> str:
        if self.args:
            return str(self.args[0])
        return self.default_message


class PlantError(GardenError):
    default_message: str = "Unknown plant error"


class WaterError(GardenError):
    default_message: str = "Unknown water error"


def raise_plant_error() -> None:
    raise PlantError("The tomato plant is wilting!")


def raise_water_error() -> None:
    raise WaterError("Not enough water in the tank!")


def test_custom_errors() -> None:
    print("=== Custom Garden Errors Demo ===")

    print("\nTesting PlantError...")
    try:
        raise_plant_error()
    except PlantError as error:
        print(f"Caught PlantError: {error}")

    print("\nTesting WaterError...")
    try:
        raise_water_error()
    except WaterError as error:
        print(f"Caught WaterError: {error}")

    print("\nTesting catching all garden errors...")
    try:
        raise_plant_error()
    except GardenError as error:
        print(f"Caught GardenError: {error}")
    try:
        raise_water_error()
    except GardenError as error:
        print(f"Caught GardenError: {error}")

    print("\nTesting default messages...")
    for error_class in [GardenError, PlantError, WaterError]:
        try:
            raise error_class()
        except GardenError as error:
            print(f"Default message: {error}")

    print("\nAll custom error types work correctly!")


if __name__ == "__main__":
    test_custom_errors()
