# noinspection PyUnusedLocal
from collections import Counter
import math
from typing import Dict

SKU = str
Price = int  # This should be decimal.Decimal if we wish to handle pennies

# Given an SKU, a map of possible ways to buy it (including by unit), attaching
# count to price
# This allows for more offers. Could be a list of pairs (all we do on this dict
# is iteration on key-value pairs), but it's slightly easier to read this way
PRICE_TABLE: Dict[SKU, Dict[int, Price]] = {
    "A": {1: 50, 3: 130},
    "B": {1: 30, 2: 45},
    "C": {1: 20},
    "D": {1: 15},
}


def get_best_price(sku: SKU, count: int) -> Price:
    """
    Returns price using best offer for the given count of a product by sku
    """
    unit_price = PRICE_TABLE[sku][1]  # This should always be present
    best: Price = math.inf  # type: ignore
    for offer_count, offer_price in PRICE_TABLE[sku].items():
        total_offers, remaining = divmod(count, offer_count)
        best = min(best, total_offers * offer_price + remaining * unit_price)
    return best


# skus = unicode string
def checkout(skus: str) -> Price:
    total = 0
    counts = Counter(skus)
    for sku, count in counts.items():
        total += get_best_price(sku, count)
    return total


