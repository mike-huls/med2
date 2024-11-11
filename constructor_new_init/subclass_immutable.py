class Currency(float):
    def __new__(cls, value: float, symbol: str):
        obj = super(Currency, cls).__new__(cls, value)
        obj.symbol = symbol
        return obj

    def __str__(self) -> str:
        return f"{self.symbol} {self:.2f}"


price = Currency(12.768544, symbol="€")
print(price)  # prints: "€ 12.74"
print(f"{price.symbol} {price}")  # prints: "€ 12.74"
