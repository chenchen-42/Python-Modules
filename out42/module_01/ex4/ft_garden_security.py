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

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._days

    def show(self) -> None:
        print(f"{self._name}: {round(self._height, 1)}cm, "
              f"{self._days} days old")

    def grow(self) -> None:
        self._height += self._growth_rate

    def age(self) -> None:
        self._days += 1


def main() -> None:
    print("=== Garden Security System ===")
    rose: Plant = Plant("Rose", 15.0, 10)
    print("Plant created: ", end="")
    rose.show()

    print()
    if rose.set_height(25):
        print("Height updated: 25cm")
    if rose.set_age(30):
        print("Age updated: 30 days")

    print()
    if not rose.set_height(-5):
        print("Height update rejected")
    if not rose.set_age(-3):
        print("Age update rejected")

    print()
    print("Current state: ", end="")
    rose.show()


if __name__ == "__main__":
    main()
