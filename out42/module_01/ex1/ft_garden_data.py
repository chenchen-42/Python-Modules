class Plant:
    name: str
    height: int
    days: int

    def show(self) -> None:
        print(f"{self.name}: {self.height}cm, {self.days} days old")


def main() -> None:
    print("=== Garden Plant Registry ===")

    rose: Plant = Plant()
    rose.name = "Rose"
    rose.height = 25
    rose.days = 30

    sunflower: Plant = Plant()
    sunflower.name = "Sunflower"
    sunflower.height = 80
    sunflower.days = 45

    cactus: Plant = Plant()
    cactus.name = "Cactus"
    cactus.height = 15
    cactus.days = 120

    rose.show()
    sunflower.show()
    cactus.show()


if __name__ == "__main__":
    main()
