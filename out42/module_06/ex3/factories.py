from abc import ABC, abstractmethod

from .creature import Creature
from .entities import Flameling, Morphagon, Pyrodon, Shiftling


class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> Creature:
        """Create the basic form of a creature family."""

    @abstractmethod
    def create_evolved(self) -> Creature:
        """Create the evolved form of the same family."""


class FlameFactory(CreatureFactory):
    def create_base(self) -> Flameling:
        return Flameling()

    def create_evolved(self) -> Pyrodon:
        return Pyrodon()


class TransformCreatureFactory(CreatureFactory):
    def create_base(self) -> Shiftling:
        return Shiftling()

    def create_evolved(self) -> Morphagon:
        return Morphagon()
