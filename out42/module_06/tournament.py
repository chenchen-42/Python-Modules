from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory
from ex4 import (AggressiveStrategy, BattleStrategy, NormalStrategy,
                 StrategyError)


def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    fighters = [(factory.create_base(), strategy)
                for factory, strategy in opponents]
    try:
        for i, (first, first_strategy) in enumerate(fighters):
            for second, second_strategy in fighters[i + 1:]:
                print("* Battle *")
                print(first.describe())
                print(" vs.")
                print(second.describe())
                print(" now fight!")
                first_strategy.act(first)
                second_strategy.act(second)
    except StrategyError as error:
        print(f"Battle error, aborting tournament: {error}")


def run_tournament(title: str,
                   opponents: list[tuple[CreatureFactory, BattleStrategy]]
                   ) -> None:
    print(title)
    labels: str = ", ".join(
        f"({factory.create_base().name}+{strategy.label})"
        for factory, strategy in opponents)
    print(f" [ {labels} ]")
    battle(opponents)


def main() -> None:
    flame = FlameFactory()
    transform = TransformCreatureFactory()
    normal = NormalStrategy()
    aggressive = AggressiveStrategy()

    run_tournament("Tournament 0 (basic)",
                   [(flame, normal), (transform, aggressive)])
    run_tournament("Tournament 1 (error)",
                   [(transform, aggressive), (flame, aggressive)])
    run_tournament("Tournament 2 (three opponents)",
                   [(flame, normal), (transform, aggressive),
                    (transform, normal)])


if __name__ == "__main__":
    main()
