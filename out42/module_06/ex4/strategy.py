from abc import ABC, abstractmethod

from ex3.creature import Creature

from .errors import StrategyError


class BattleStrategy(ABC):
    label: str = "abstract"

    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        """Tell whether the creature is suitable for this strategy."""

    @abstractmethod
    def act(self, creature: Creature) -> None:
        """Make the creature act (raise StrategyError if not valid)."""

    def _invalid(self, creature: Creature) -> StrategyError:
        return StrategyError(f"Invalid Creature '{creature.name}' for this "
                             f"{self.label.lower()} strategy")
