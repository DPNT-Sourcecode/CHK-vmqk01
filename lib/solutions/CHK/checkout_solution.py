# noinspection PyUnusedLocal
from collections import Counter
import math
from typing import Dict

SKU = str
Price = int  # This should be decimal.Decimal if we wish to handle pennies
PRICE_TABLE: Dict[SKU, Dict[int, Price]] = {
    "A": {1: 50, 3: 130},
    "B": {1: 30, 2: 45},
    "C": {1: 20},
    "D": {1: 15},
}


def get_best_price(sku: SKU, count: int) -> Price:
    """Returns price using best offer for the given count of a product by sku"""
    unit_price = PRICE_TABLE[sku][1]  # This should always be present
    best = math.inf
    for offer_count, offer_price in PRICE_TABLE[sku].items():
        total_offers, remaining = (count // offer_count), (count % offer_count)
        best = min(best, total_offers * offer_price + remaining * unit_price)


# skus = unicode string
def checkout(skus: str) -> Price:
    total = 0
    counts = Counter(skus)
    for sku, count in counts.items():

        total += get_best_price(sku, count)
    return total





