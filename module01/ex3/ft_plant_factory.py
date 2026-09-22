class Plant:
    def __init__(self, name: str, height: float, age: int,
                 growth_rate: float) -> None:
        self.name = name
        self.height = height
        self.age = age
        self.growth_rate = growth_rate

    def grow(self) -> None:
        self.height += self.growth_rate

    def age_up(self) -> None:
        self.age += 1

    def show(self) -> None:
        print(f"{self.name}: {round(self.height, 1)}cm, "
              f"{self.age} days old")


def ft_plant_factory() -> None:
    print("=== Plant Factory ===")

    plants = [
        Plant("Rose", 25.0, 30, 0.8),
        Plant("Sunflower", 80.0, 45, 2.5),
        Plant("Cactus", 15.0, 120, 0.1),
        Plant("Tulip", 18.0, 20, 1.0),
        Plant("Fern", 10.0, 60, 0.4),
    ]

    for plant in plants:
        plant.show()


if __name__ == "__main__":
    ft_plant_factory()
