import random


def main() -> None:
    print("=== Game Data Alchemist ===\n")

    players: list[str] = ["Alice", "bob", "Charlie", "dylan", "Emma",
                          "Gregory", "john", "kevin", "Liam"]
    print(f"Initial list of players: {players}")

    all_cap: list[str] = [p.capitalize() for p in players]
    print(f"New list with all names capitalized: {all_cap}")

    only_cap: list[str] = [p for p in players if p == p.capitalize()]
    print(f"New list of capitalized names only: {only_cap}\n")

    scores: dict[str, int] = {p: random.randint(0, 1000) for p in all_cap}
    print(f"Score dict: {scores}")

    average: float = sum(scores.values()) / len(scores)
    print(f"Score average is {round(average, 2)}")

    high: dict[str, int] = {p: s for p, s in scores.items() if s > average}
    print(f"High scores: {high}")


if __name__ == "__main__":
    main()
