from abc import ABC, abstractmethod


class TransformCapability(ABC):
    """An ability kept apart from Creature on purpose."""

    def __init__(self) -> None:
        self.transformed: bool = False

    @abstractmethod
    def transform(self) -> str:
        """Enter the transformed state and return a message."""

    @abstractmethod
    def revert(self) -> str:
        """Leave the transformed state and return a message."""
