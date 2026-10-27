from ex3.capability import TransformCapability
from ex3.creature import Creature

from .strategy import BattleStrategy


class NormalStrategy(BattleStrategy):
    label = "Normal"

    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise self._invalid(creature)
        print(creature.attack())


class AggressiveStrategy(BattleStrategy):
    label = "Aggressive"

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> None:
        if not isinstance(creature, TransformCapability):
            raise self._invalid(creature)
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())
