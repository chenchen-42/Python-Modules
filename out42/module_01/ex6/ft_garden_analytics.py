class Plant:
    class Stats:
        def __init__(self) -> None:
            self._grow_calls: int = 0
            self._age_calls: int = 0
            self._show_calls: int = 0

        def count_grow(self) -> None:
            self._grow_calls += 1

        def count_age(self) -> None:
            self._age_calls += 1

        def count_show(self) -> None:
            self._show_calls += 1

        def display(self) -> None:
            print(f"Stats: {self._grow_calls} grow, "
                  f"{self._age_calls} age, {self._show_calls} show")

    def __init__(self, name: str, height: float, days: int,
                 growth_rate: float = 0.8) -> None:
        self._name: str = name
        self._height: float = 0.0
        self._days: int = 0
        self._growth_rate: float = growth_rate
        self._stats: Plant.Stats = Plant.Stats()
        self.set_height(height)
        self.set_age(days)

    @staticmethod
    def is_older_than_one_year(days: int) -> bool:
        return days > 365

    @classmethod
    def anonymous(cls) -> "Plant":
        return cls("Unknown plant", 0.0, 0)

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

    def get_stats(self) -> "Plant.Stats":
        return self._stats

    def show(self) -> None:
        self._stats.count_show()
        print(f"{self._name}: {round(self._height, 1)}cm, "
              f"{self._days} days old")

    def grow(self) -> None:
        self._stats.count_grow()
        self._height += self._growth_rate

    def age(self, days: int = 1) -> None:
        self._stats.count_age()
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


class Seed(Flower):
    def __init__(self, name: str, height: float, days: int, color: str,
                 growth_rate: float = 0.8) -> None:
        super().__init__(name, height, days, color, growth_rate)
        self._seeds: int = 0

    def bloom(self) -> None:
        super().bloom()
        self._seeds = 42

    def show(self) -> None:
        super().show()
        print(f" Seeds: {self._seeds}")


class Tree(Plant):
    class TreeStats(Plant.Stats):
        def __init__(self) -> None:
            super().__init__()
            self._shade_calls: int = 0

        def count_shade(self) -> None:
            self._shade_calls += 1

        def display(self) -> None:
            super().display()
            print(f" {self._shade_calls} shade")

    def __init__(self, name: str, height: float, days: int,
                 trunk_diameter: float, growth_rate: float = 0.1) -> None:
        super().__init__(name, height, days, growth_rate)
        self._trunk_diameter: float = trunk_diameter
        self._tree_stats: Tree.TreeStats = Tree.TreeStats()
        self._stats = self._tree_stats

    def produce_shade(self) -> None:
        self._tree_stats.count_shade()
        print(f"Tree {self._name} now produces a shade of "
              f"{round(self._height, 1)}cm long and "
              f"{round(self._trunk_diameter, 1)}cm wide.")

    def show(self) -> None:
        super().show()
        print(f" Trunk diameter: {round(self._trunk_diameter, 1)}cm")


def display_stats(plant: Plant) -> None:
    print(f"[statistics for {plant.get_name()}]")
    plant.get_stats().display()


def main() -> None:
    print("=== Garden statistics ===")

    print("=== Check year-old")
    for days in [30, 400]:
        print(f"Is {days} days more than a year? -> "
              f"{Plant.is_older_than_one_year(days)}")

    print("\n=== Flower")
    rose: Flower = Flower("Rose", 15.0, 10, "red", 8.0)
    rose.show()
    display_stats(rose)
    print("[asking the rose to grow and bloom]")
    rose.grow()
    rose.bloom()
    rose.show()
    display_stats(rose)

    print("\n=== Tree")
    oak: Tree = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    display_stats(oak)
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    display_stats(oak)

    print("\n=== Seed")
    sunflower: Seed = Seed("Sunflower", 80.0, 45, "yellow", 30.0)
    sunflower.show()
    print("[make sunflower grow, age and bloom]")
    sunflower.grow()
    sunflower.age(20)
    sunflower.bloom()
    sunflower.show()
    display_stats(sunflower)

    print("\n=== Anonymous")
    unknown: Plant = Plant.anonymous()
    unknown.show()
    display_stats(unknown)


if __name__ == "__main__":
    main()
