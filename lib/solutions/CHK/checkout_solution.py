# noinspection PyUnusedLocal
from collections import Counter
from typing import Dict

SKU = str
Price = int  # This should be decimal.Decimal if we wish to handle pennies
PRICE_TABLE: Dict[SKU, Dict[int, Price]] = {
    "A": {1: 50, 3: 130},
    "B": {1: 30, 2: 45},
    "C": {1: 20},
    "D": {1: 15},
}


# skus = unicode string
def checkout(skus: str):
    total = 0
    counts = Counter(skus)
    for sku, count in counts.items():
        total += PRICE_TABLE[sku][count]
    return total




