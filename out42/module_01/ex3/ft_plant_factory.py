class Plant:
    def __init__(self, name: str, height: float, days: int,
                 growth_rate: float = 0.8) -> None:
        self.name: str = name
        self.height: float = float(height)
        self.days: int = days
        self.growth_rate: float = growth_rate

    def show(self) -> None:
        print(f"{self.name}: {round(self.height, 1)}cm, "
              f"{self.days} days old")

    def grow(self) -> None:
        self.height += self.growth_rate

    def age(self) -> None:
        self.days += 1


def main() -> None:
    print("=== Plant Factory Output ===")

    plants: list[Plant] = [
        Plant("Rose", 25.0, 30),
        Plant("Oak", 200.0, 365, 0.1),
        Plant("Cactus", 5.0, 90, 0.05),
        Plant("Sunflower", 80.0, 45, 3.0),
        Plant("Fern", 15.0, 120, 0.3),
    ]
    for plant in plants:
        print("Created: ", end="")
        plant.show()


if __name__ == "__main__":
    main()
