# noinspection PyUnusedLocal
from collections import Counter
import math
from typing import Dict, List, Tuple

SKU = str
Price = int  # This should be decimal.Decimal if we wish to handle pennies


class PricingInfo:
    def __init__(self) -> None:
        self.price_table: Dict[SKU, List[Tuple[int, Price]]] = {}

    def add_sku(self, sku: SKU, unit_price: Price) -> None:
        if sku in self.price_table:
            raise KeyError(sku)
        self.price_table[sku] = [(1, Price)]

    def add_multi_price_offer(sku: SKU, count: int, discount_price: Price) -> None:
        self.price_table[sku].append((count, discount_price))


# Given an SKU, a list of possible ways to buy it (including by unit),
# pairing count and price. Counts should be in decreasing order, and
# the last count should always be unit price (1)
PRICE_TABLE: Dict[SKU, List[Tuple[int, Price]]] = {
    "A": [(5, 200), (3, 130), (1, 50)],
    "B": [(2, 45), (1, 30)],
    "C": [(1, 20)],
    "D": [(1, 15)],
    "E": [(1, 40)],
    # Buy 2Fs get one free is equivalent to buy 3Fs, pay 2 == 20
    "F": [(3, 20), (1, 10)],
}

# Cart wide discounts of the type "buy N×X, get M×Y free"
# represented as CART_DISCOUNTS[X] == (N, M, Y)
CART_DISCOUNTS: Dict[SKU, Tuple[int, int, SKU]] = {"E": (2, 1, "B")}


def get_best_price(sku: SKU, count: int) -> Price:
    """
    Returns price using best offer for the given count of a product by sku
    """
    price = 0
    # This depends on
    #  - the PRICE_TABLE having offers from larger to smaller
    #  - the offers being stable
    #  - having a unit price at the end
    for offer_count, offer_price in PRICE_TABLE[sku]:
        total_offers, count = divmod(count, offer_count)
        price += total_offers * offer_price
    return price


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
