from dataclasses import dataclass
import math


@dataclass
class TradeState:
    qty_yes: float = 0.0
    qty_no: float = 0.0
    cost_yes: float = 0.0
    cost_no: float = 0.0

    def pair_cost(self) -> tuple[float, float, float]:
        avg_yes = self.cost_yes / self.qty_yes if self.qty_yes else math.inf
        avg_no = self.cost_no / self.qty_no if self.qty_no else math.inf
        return avg_yes + avg_no, avg_yes, avg_no

    def simulate_buy(self, side: str, price: float, qty: float) -> "TradeState":
        next_state = TradeState(**self.__dict__)
        if side.upper() == "YES":
            next_state.qty_yes += qty
            next_state.cost_yes += price * qty
        else:
            next_state.qty_no += qty
            next_state.cost_no += price * qty
        return next_state

    def update_after_fill(self, side: str, price: float, qty: float) -> None:
        filled = self.simulate_buy(side, price, qty)
        self.qty_yes, self.qty_no = filled.qty_yes, filled.qty_no
        self.cost_yes, self.cost_no = filled.cost_yes, filled.cost_no

    def locked_profit(self) -> float:
        return min(self.qty_yes, self.qty_no) - (self.cost_yes + self.cost_no)
