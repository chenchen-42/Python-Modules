class Plant:
    class _Stats:
        def __init__(self) -> None:
            self._grow_count: int = 0
            self._age_count: int = 0
            self._show_count: int = 0

        def increment_grow(self) -> None:
            self._grow_count += 1

        def increment_age(self) -> None:
            self._age_count += 1

        def increment_show(self) -> None:
            self._show_count += 1

        def display(self) -> None:
            print(f"Stats: {self._grow_count} grow, "
                  f"{self._age_count} age, {self._show_count} show")

    def __init__(self, name: str, height: float, age: int,
                 growth_rate: float = 1.0, age_step: int = 1) -> None:
        self._name: str = name
        self._growth_rate: float = growth_rate
        self._age_step: int = age_step
        self._stats: Plant._Stats = Plant._Stats()

        if height < 0:
            print(f"{name}: Error, height can't be negative")
            self._height: float = 0.0
        else:
            self._height = height

        if age < 0:
            print(f"{name}: Error, age can't be negative")
            self._age: int = 0
        else:
            self._age = age

    def get_name(self) -> str:
        return self._name

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._age

    def set_height(self, height: float) -> None:
        if height < 0:
            print(f"{self._name}: Error, height can't be negative")
            print("Height update rejected")
        else:
            self._height = height
            print(f"Height updated: {height}cm")

    def set_age(self, age: int) -> None:
        if age < 0:
            print(f"{self._name}: Error, age can't be negative")
            print("Age update rejected")
        else:
            self._age = age
            print(f"Age updated: {age} days")

    def grow(self) -> None:
        self._height += self._growth_rate
        self._stats.increment_grow()

    def age_up(self) -> None:
        self._age += self._age_step
        self._stats.increment_age()

    def show(self) -> None:
        print(f"{self._name}: {round(self._height, 1)}cm, "
              f"{self._age} days old")
        self._stats.increment_show()

    def show_stats(self) -> None:
        self._stats.display()

    @staticmethod
    def is_older_than_year(age: int) -> bool:
        return age > 365

    @classmethod
    def create_anonymous(cls) -> "Plant":
        return cls("Unknown plant", 0.0, 0)


class Flower(Plant):
    def __init__(self, name: str, height: float, age: int, color: str,
                 growth_rate: float = 1.0, age_step: int = 1) -> None:
        super().__init__(name, height, age, growth_rate, age_step)
        self._color: str = color
        self._bloomed: bool = False

    def bloom(self) -> None:
        self._bloomed = True

    def show(self) -> None:
        super().show()
        print(f"Color: {self._color}")
        if self._bloomed:
            print(f"{self._name} is blooming beautifully!")
        else:
            print(f"{self._name} has not bloomed yet")


class Tree(Plant):
    class _TreeStats(Plant._Stats):
        def __init__(self) -> None:
            super().__init__()
            self._shade_count: int = 0

        def increment_shade(self) -> None:
            self._shade_count += 1

        def display(self) -> None:
            super().display()
            print(f"{self._shade_count} shade")

    def __init__(self, name: str, height: float, age: int,
                 trunk_diameter: float, growth_rate: float = 1.0,
                 age_step: int = 1) -> None:
        super().__init__(name, height, age, growth_rate, age_step)
        self._trunk_diameter: float = trunk_diameter
        self._stats: Tree._TreeStats = Tree._TreeStats()

    def produce_shade(self) -> None:
        print(f"Tree {self._name} now produces a shade of "
              f"{round(self._height, 1)}cm long and "
              f"{round(self._trunk_diameter, 1)}cm wide.")
        self._stats.increment_shade()

    def show(self) -> None:
        super().show()
        print(f"Trunk diameter: {round(self._trunk_diameter, 1)}cm")


class Seed(Flower):
    def __init__(self, name: str, height: float, age: int, color: str,
                 seeds_on_bloom: int, growth_rate: float = 1.0,
                 age_step: int = 1) -> None:
        super().__init__(name, height, age, color, growth_rate, age_step)
        self._seeds_on_bloom: int = seeds_on_bloom
        self._num_seeds: int = 0

    def bloom(self) -> None:
        super().bloom()
        self._num_seeds = self._seeds_on_bloom

    def show(self) -> None:
        super().show()
        print(f"Seeds: {self._num_seeds}")


def display_stats(plant: Plant) -> None:
    plant.show_stats()


def main() -> None:
    print("=== Garden statistics ===")

    print("=== Check year-old")
    print(f"Is 30 days more than a year? -> "
          f"{Plant.is_older_than_year(30)}")
    print(f"Is 400 days more than a year? -> "
          f"{Plant.is_older_than_year(400)}")
    print("")
    
    print("=== Flower")
    rose = Flower("Rose", 15.0, 10, "red", growth_rate=8.0)
    rose.show()
    print(f"[statistics for {rose.get_name()}]")
    display_stats(rose)
    print("[asking the rose to grow and bloom]")
    rose.grow()
    rose.bloom()
    rose.show()
    print(f"[statistics for {rose.get_name()}]")
    display_stats(rose)
    print("")

    print("=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    print(f"[statistics for {oak.get_name()}]")
    display_stats(oak)
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    print(f"[statistics for {oak.get_name()}]")
    display_stats(oak)
    print("")

    print("=== Seed")
    sunflower = Seed(
        "Sunflower", 80.0, 45, "yellow", 42,
        growth_rate=30.0, age_step=20
    )
    sunflower.show()
    print("[make sunflower grow, age and bloom]")
    sunflower.grow()
    sunflower.age_up()
    sunflower.bloom()
    sunflower.show()
    print(f"[statistics for {sunflower.get_name()}]")
    display_stats(sunflower)
    print("")

    print("=== Anonymous")
    unknown = Plant.create_anonymous()
    unknown.show()
    print(f"[statistics for {unknown.get_name()}]")
    display_stats(unknown)


if __name__ == "__main__":
    main()
