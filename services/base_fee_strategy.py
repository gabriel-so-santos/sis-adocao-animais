from abc import ABC, abstractmethod
from models.animals import Cat, Dog

class BaseFeeStrategy(ABC):
    """Interface para estratégias de cálculo de taxa."""

    @abstractmethod
    def calculate_fee(self, animal: Cat|Dog) -> float:
        pass