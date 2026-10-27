class Plant:
    def __init__(self, name: str, height: float, days: int,
                 growth_rate: float = 0.8) -> None:
        self._name: str = name
        self._height: float = 0.0
        self._days: int = 0
        self._growth_rate: float = growth_rate
        self.set_height(height)
        self.set_age(days)

    def set_height(self, height: float) -> bool:
        if height < 0:
            print(f"{self._name}: Error, height can't be negative")
            return False
        self._height = float(height)
        return True

    def set_age(self, days: int) -> bool:
        if days < 0:
            print(f"{self._name}: Error, age can't be negative")
            return False
        self._days = days
        return True

    def get_name(self) -> str:
        return self._name

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._days

    def show(self) -> None:
        print(f"{self._name}: {round(self._height, 1)}cm, "
              f"{self._days} days old")

    def grow(self) -> None:
        self._height += self._growth_rate

    def age(self, days: int = 1) -> None:
        self._days += days


class Flower(Plant):
    def __init__(self, name: str, height: float, days: int, color: str,
                 growth_rate: float = 0.8) -> None:
        super().__init__(name, height, days, growth_rate)
        self._color: str = color
        self._bloomed: bool = False

    def bloom(self) -> None:
        self._bloomed = True

    def show(self) -> None:
        super().show()
        print(f" Color: {self._color}")
        if self._bloomed:
            print(f" {self._name} is blooming beautifully!")
        else:
            print(f" {self._name} has not bloomed yet")


class Tree(Plant):
    def __init__(self, name: str, height: float, days: int,
                 trunk_diameter: float, growth_rate: float = 0.1) -> None:
        super().__init__(name, height, days, growth_rate)
        self._trunk_diameter: float = trunk_diameter

    def produce_shade(self) -> None:
        print(f"Tree {self._name} now produces a shade of "
              f"{round(self._height, 1)}cm long and "
              f"{round(self._trunk_diameter, 1)}cm wide.")

    def show(self) -> None:
        super().show()
        print(f" Trunk diameter: {round(self._trunk_diameter, 1)}cm")


class Vegetable(Plant):
    def __init__(self, name: str, height: float, days: int,
                 harvest_season: str, growth_rate: float = 0.8) -> None:
        super().__init__(name, height, days, growth_rate)
        self._harvest_season: str = harvest_season
        self._nutritional_value: float = 0

    def grow(self) -> None:
        super().grow()
        self._nutritional_value += 0.5

    def age(self, days: int = 1) -> None:
        super().age(days)
        self._nutritional_value += 0.5

    def show(self) -> None:
        super().show()
        print(f" Harvest season: {self._harvest_season}")
        print(f" Nutritional value: {self._nutritional_value:g}")


def main() -> None:
    print("=== Garden Plant Types ===")

    print("=== Flower")
    rose: Flower = Flower("Rose", 15.0, 10, "red")
    rose.show()
    print("[asking the rose to bloom]")
    rose.bloom()
    rose.show()

    print("\n=== Tree")
    oak: Tree = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    print("[asking the oak to produce shade]")
    oak.produce_shade()

    print("\n=== Vegetable")
    tomato: Vegetable = Vegetable("Tomato", 5.0, 10, "April", 2.1)
    tomato.show()
    print("[make tomato grow and age for 20 days]")
    for _ in range(20):
        tomato.grow()
        tomato.age()
    tomato.show()


if __name__ == "__main__":
    main()
