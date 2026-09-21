class Plant:
    def __init__(self, name, height, age, growth_rate):
        self.name = name
        self.height = height
        self.age = age
        self.growth_rate = growth_rate

    def grow(self):
        self.height += self.growth_rate

    def age_up(self):
        self.age += 1

    def show(self):
        print(f"{self.name}: {round(self.height, 1)}cm, {self.age} days old")


def ft_plant_growth():
    print("=== Garden Plant Growth ===")

    rose = Plant("Rose", 25.0, 30, 0.8)
    rose.show()

    start_height = rose.height

    for day in range(1, 8):
        print(f"=== Day {day} ===")
        rose.grow()
        rose.age_up()
        rose.show()

    weekly_growth = rose.height - start_height
    print(f"Growth this week: {round(weekly_growth, 1)}cm")


if __name__ == "__main__":
    ft_plant_growth()
