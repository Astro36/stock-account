from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass(frozen=True)
class HeldAsset:
    account_number: str
    name: str
    currency: str
    exchange_rate: float = field(repr=False)
    market_value: float

    def prettify_account_number(self) -> str:
        return self.account_number[0:3] + "-" + self.account_number[3:5] + "-" + self.account_number[5:]


@dataclass(frozen=True)
class HeldCash(HeldAsset):
    pass


@dataclass(frozen=True)
class HeldCashEquivalent(HeldCash):
    maturity_date: date
    entry_value: Optional[float] = field(repr=False)

    def get_pnl(self) -> float:
        return self.market_value - self.entry_value

    def get_pnl_percent(self) -> float:
        return self.get_pnl() / self.entry_value

    def get_market_price(self) -> float:
        return self.market_value / self.quantity

    def get_entry_price(self) -> float:
        return self.entry_value / self.quantity


@dataclass(frozen=True)
class HeldEquity(HeldAsset):
    symbol: str
    quantity: float
    entry_value: Optional[float] = field(repr=False)

    def get_pnl(self) -> float:
        return self.market_value - self.entry_value

    def get_pnl_percent(self) -> float:
        return self.get_pnl() / self.entry_value

    def get_market_price(self) -> float:
        return self.market_value / self.quantity

    def get_entry_price(self) -> float:
        return self.entry_value / self.quantity


@dataclass(frozen=True)
class HeldGoldSpot(HeldAsset):
    symbol: str
    quantity: float
    entry_value: Optional[float] = field(repr=False)

    def get_pnl(self) -> float:
        return self.market_value - self.entry_value

    def get_pnl_percent(self) -> float:
        return self.get_pnl() / self.entry_value

    def get_market_price(self) -> float:
        return self.market_value / self.quantity

    def get_entry_price(self) -> float:
        return self.entry_value / self.quantity