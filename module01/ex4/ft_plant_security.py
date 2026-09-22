class Plant:
    def __init__(self, name: str, height: float, age: int,
                 growth_rate: float = 1.0) -> None:
        self._name = name
        self._growth_rate = growth_rate

        if height < 0:
            print(f"{name}: Error, height can't be negative")
            self._height = 0.0
        else:
            self._height = height

        if age < 0:
            print(f"{name}: Error, age can't be negative")
            self._age = 0
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

    def age_up(self) -> None:
        self._age += 1

    def show(self) -> None:
        print(f"{self._name}: {round(self._height, 1)}cm, "
              f"{self._age} days old")


def ft_garden_security() -> None:
    print("=== Garden Security System ===")

    rose = Plant("Rose", 15.0, 10)
    print(f"Plant created: {rose.get_name()}: "
          f"{round(rose.get_height(), 1)}cm, {rose.get_age()} days old")

    rose.set_height(25)
    rose.set_age(30)

    rose.set_height(-5)
    rose.set_age(-3)

    print(f"Current state: {rose.get_name()}: "
          f"{round(rose.get_height(), 1)}cm, {rose.get_age()} days old")


if __name__ == "__main__":
    ft_garden_security()
