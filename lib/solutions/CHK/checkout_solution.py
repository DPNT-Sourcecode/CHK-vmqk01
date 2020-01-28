# noinspection PyUnusedLocal
from collections import Counter
import math
from typing import Dict, Tuple

SKU = str
Price = int  # This should be decimal.Decimal if we wish to handle pennies

# Given an SKU, a map of possible ways to buy it (including by unit), attaching
# count to price
# This allows for more offers. Could be a list of pairs (all we do on this dict
# is iteration on key-value pairs), but it's slightly easier to read this way
PRICE_TABLE: Dict[SKU, Dict[int, Price]] = {
    "A": {1: 50, 3: 130, 5: 200},
    "B": {1: 30, 2: 45},
    "C": {1: 20},
    "D": {1: 15},
    "E": {1: 40},
}

# Cart wide discounts of the type "buy N×X, get M×Y free"
# represented as CART_DISCOUNTS[X] == (N, M, Y)
CART_DISCOUNTS: Dict[SKU, Tuple[int, int, SKU]] = {"E": (2, 1, "B")}


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


def apply_cart_discounts(cart: Counter) -> None:
    """
    Modify cart for discounts of the type "buy N×X, get M×Y free".

    Assumes it's always beneficial for the user to get this offer.
    """
    for x in CART_DISCOUNTS:
        n, m, y = CART_DISCOUNTS[x]
        x_bought = cart[x]
        free_items = m * (x_bought // n)
        cart[y] = max(0, cart[y] - free_items)


# skus = unicode string
def checkout(skus: str) -> Price:
    total = 0
    counts = Counter(skus)
    apply_cart_discounts(counts)
    for sku, count in counts.items():
        try:
            total += get_best_price(sku, count)
        except KeyError:
            return -1
    return total
