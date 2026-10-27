class GardenError(Exception):
    default_message: str = "Unknown garden error"

    def __str__(self) -> str:
        if self.args:
            return str(self.args[0])
        return self.default_message


class PlantError(GardenError):
    default_message: str = "Unknown plant error"


def water_plant(plant_name: str) -> None:
    if plant_name == "" or plant_name != plant_name.capitalize():
        raise PlantError(f"Invalid plant name to water: '{plant_name}'")
    print(f"Watering {plant_name}: [OK]")


def test_watering_system() -> None:
    print("=== Garden Watering System ===")
    tests: list[tuple[str, list[str]]] = [
        ("valid", ["Tomato", "Lettuce", "Carrots"]),
        ("invalid", ["Tomato", "lettuce", "Carrots"]),
    ]
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


if __name__ == "__main__":
    test_watering_system()
    print()
    print("Cleanup always happens, even with errors!")
