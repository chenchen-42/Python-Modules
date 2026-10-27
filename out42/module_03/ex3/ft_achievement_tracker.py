import random

ALL_ACHIEVEMENTS: list[str] = [
    "Crafting Genius", "World Savior", "Master Explorer",
    "Collector Supreme", "Untouchable", "Boss Slayer", "Strategist",
    "Unstoppable", "Speed Runner", "Survivor", "Treasure Hunter",
    "First Steps", "Sharp Mind", "Hidden Path Finder", "Lone Wolf",
    "Team Player", "Night Owl", "Early Bird", "Marathoner",
    "Pacifist", "Sharpshooter", "Architect", "Diplomat", "Alchemist",
    "Legend",
]


def gen_player_achievements() -> set[str]:
    count: int = random.randint(10, 15)
    return set(random.sample(ALL_ACHIEVEMENTS, count))


def main() -> None:
    print("=== Achievement Tracker System ===\n")

    players: list[tuple[str, set[str]]] = [
        ("Alice", gen_player_achievements()),
        ("Bob", gen_player_achievements()),
        ("Charlie", gen_player_achievements()),
        ("Dylan", gen_player_achievements()),
    ]

    for name, achievements in players:
        print(f"Player {name}: {achievements}")

    distinct: set[str] = set()
    common: set[str] = players[0][1]
    for _, achievements in players:
        distinct = distinct.union(achievements)
        common = common.intersection(achievements)
    print(f"\nAll distinct achievements: {distinct}")
    print(f"\nCommon achievements: {common}\n")

    for name, achievements in players:
        others: set[str] = set()
        for other_name, other_achievements in players:
            if other_name != name:
                others = others.union(other_achievements)
        print(f"Only {name} has: {achievements.difference(others)}")

    print()
    everything: set[str] = set(ALL_ACHIEVEMENTS)
    for name, achievements in players:
        print(f"{name} is missing: {everything.difference(achievements)}")


if __name__ == "__main__":
    main()
