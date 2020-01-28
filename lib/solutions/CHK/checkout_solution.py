# noinspection PyUnusedLocal
from collections import Counter
import math
from typing import Dict, List, Tuple

SKU = str
Price = int  # This should be decimal.Decimal if we wish to handle pennies


class PricingInfo:
    def __init__(self) -> None:
        self.price_table: Dict[SKU, List[Tuple[int, Price]]] = {}
        self.cart_discounts: Dict[SKU, Tuple[int, int, SKU]] = {}

    def add_sku(self, sku: SKU, unit_price: Price) -> None:
        if sku in self.price_table:
            raise KeyError(sku)
        self.price_table[sku] = [(1, unit_price)]

    def add_multi_price_offer(
        self, sku: SKU, count: int, discount_price: Price
    ) -> None:
        # Assumes no conflicting offers
        self.price_table[sku].append((count, discount_price))
        self.price_table[sku].sort(reverse=True)

    def add_buy_many_get_some_free(self, x: SKU, n: int, y: SKU, m: int) -> None:
        if x == y:
            # This is a hidden multi-price discount
            self.add_multi_price_offer(x, n + m, (n - m) * self.get_price(x, 1))
        else:
            self.cart_discounts[x] = (n, m, y)

    def get_price(self, sku: SKU, count: int) -> Price:
        """
        Returns price using best offer for the given count of a product by sku
        """
        price = 0
        # This depends on
        #  - the offers being stable
        #  - having a unit price at the end
        for offer_count, offer_price in self.price_table[sku]:
            total_offers, count = divmod(count, offer_count)
            price += total_offers * offer_price
        return price


# initialize price table
supermarket = PricingInfo()
for sku, unit in zip("ABCDEF", [50, 30, 20, 15, 40, 10]):
    supermarket.add_sku(sku, unit)
supermarket.add_multi_price_offer("A", 3, 130)
supermarket.add_multi_price_offer("A", 5, 200)
supermarket.add_multi_price_offer("B", 2, 45)
supermarket.add_buy_many_get_some_free("E", 2, "B", 1)
supermarket.add_buy_many_get_some_free("F", 2, "F", 1)


def get_best_price(sku: SKU, count: int) -> Price:
    return supermarket.get_price(sku, count)


def apply_cart_discounts(cart: Counter) -> None:
    """
    Modify cart for discounts of the type "buy N×X, get M×Y free".

    Assumes it's always beneficial for the user to get this offer.
    """
    print(supermarket.cart_discounts)
    for x in supermarket.cart_discounts:
        n, m, y = supermarket.cart_discounts[x]
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
            total += supermarket.get_price(sku, count)
        except KeyError:
            return -1
    return total



