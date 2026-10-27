class Plant:
    name: str
    height: float
    days: int
    growth_rate: float

    def show(self) -> None:
        print(f"{self.name}: {round(self.height, 1)}cm, "
              f"{self.days} days old")

    def grow(self) -> None:
        self.height += self.growth_rate

    def age(self) -> None:
        self.days += 1


def main() -> None:
    print("=== Garden Plant Growth ===")

    rose: Plant = Plant()
    rose.name = "Rose"
    rose.height = 25.0
    rose.days = 30
    rose.growth_rate = 0.8

    start_height: float = rose.height
    rose.show()
    for day in range(1, 8):
        print(f"=== Day {day} ===")
        rose.grow()
        rose.age()
        rose.show()
    print(f"Growth this week: {round(rose.height - start_height, 1)}cm")


if __name__ == "__main__":
    main()
