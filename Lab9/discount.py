from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Strategy interface: every discount turns an order total into a discounted total."""

    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    """Returns the total unchanged."""

    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """PercentageDiscount(10) takes 10% off the total."""

    def __init__(self, percentage: float):
        if not 0 <= percentage <= 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.percentage: float = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)


class BulkDiscount(DiscountStrategy):
    """BulkDiscount(200, 20) takes 20 off any total of 200 or more."""

    def __init__(self, threshold: float, amount: float):
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and amount cannot be negative.")
        self.threshold: float = threshold
        self.amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self.threshold:
            return max(total - self.amount, 0.0)
        return total


class StudentDiscount(DiscountStrategy):
    """Fourth strategy, added without touching Order: a flat 5% student discount."""

    RATE: float = 0.05

    def apply(self, total: float) -> float:
        return total * (1 - self.RATE)
