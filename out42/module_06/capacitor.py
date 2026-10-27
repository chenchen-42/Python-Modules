from typing import Protocol

from ex3 import TransformCreatureFactory


class Transformer(Protocol):
    """What this script needs from an entity (structural typing)."""

    def describe(self) -> str:
        ...

    def attack(self) -> str:
        ...

    def transform(self) -> str:
        ...

    def revert(self) -> str:
        ...


def demonstrate(entity: Transformer) -> None:
    print(entity.describe())
    print(entity.attack())
    print(entity.transform())
    print(entity.attack())
    print(entity.revert())


def main() -> None:
    print("Testing Creature with transform capability")
    factory = TransformCreatureFactory()
    print(" base:")
    demonstrate(factory.create_base())
    print(" evolved:")
    demonstrate(factory.create_evolved())


if __name__ == "__main__":
    main()
