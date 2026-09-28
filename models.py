from dataclasses import dataclass


@dataclass
class Expense:
    id: int
    amount: float
    expense_date: str
    category: str
    description: str


@dataclass
class BudgetStatus:
    category: str
    budget: float
    spent: float

    @property
    def remaining(self):
        return self.budget - self.spent
