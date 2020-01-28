# noinspection PyUnusedLocal
from collections import Counter
from typing import Dict, List, NamedTuple, Sequence, Tuple, Set, Union

SKU = str
Price = int  # This should be decimal.Decimal if we wish to handle pennies


class Pack(NamedTuple):
    # each instance of this is a virtual SKU for packs of related products
    size: int
    info: str


class PricingInfo:
    """
    Helper class to build the price table. This is same functionality as
    before, but makes writing/updating the price table more readable
    """

    def __init__(self) -> None:
        self.price_table: Dict[Union[SKU, Pack], List[Tuple[int, Price]]] = {}
        self.cart_discounts: Dict[SKU, Tuple[int, int, SKU]] = {}
        self.group_discounts: List[Tuple[Set[SKU], Pack]] = []

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
            self.add_multi_price_offer(x, n + m, n * self.get_price(x, 1))
        else:
            self.cart_discounts[x] = (n, m, y)

    def add_group_discount_offer(
        self, skus: Sequence[SKU], count: int, discount_price: Price
    ) -> None:
        # Create a virtual product that will replace these in the cart
        pack = Pack(count, f"Any {count} of {','.join(skus)} for £{discount_price}")
        self.price_table[pack] = [(1, discount_price)]
        self.group_discounts.append((set(skus), pack))

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

    def apply_cart_discounts(self, cart: Counter) -> None:
        """
        Modify cart for discounts of the type "buy N×X, get M×Y free"

        Assumes it's always beneficial for the user to get this offer.
        """
        for x in self.cart_discounts:
            n, m, y = self.cart_discounts[x]
            x_bought = cart[x]
            free_items = m * (x_bought // n)
            cart[y] = max(0, cart[y] - free_items)

    def apply_group_discounts(self, cart: Counter) -> None:
        """
        Modify cart for group discounts (any N of these for £XX).

        Assumes it's always beneficial for the user to get this offer.
        """
        for skus, pack in self.group_discounts:
            # Find all items that could go into the pack and their prices
            pack_items = []
            for sku in skus:
                pack_items += cart[sku]*[(self.get_price(sku, 1), sku)]
            # Sort by price (most expensive first)
            pack_items.sort(reverse=True)
            npacks = len(pack_items) // pack.size
            cart[pack] = npacks
            # remove the most expensive items that went into groups
            for _, sku in pack_items[:npacks * packsize]:
                cart[sku -= 1]



# initialize price table
supermarket = PricingInfo()
for sku, unit in zip(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    [
        50,  # A
        30,  # B
        20,  # C
        15,  # D
        40,  # E
        10,  # F
        20,  # G
        10,  # H
        35,  # I
        60,  # J
        70,  # K
        90,  # L
        15,  # M
        40,  # N
        10,  # O
        50,  # P
        30,  # Q
        50,  # R
        20,  # S
        20,  # T
        40,  # U
        50,  # V
        20,  # W
        17,  # X
        20,  # Y
        21,  # Z
    ],
):
    supermarket.add_sku(sku, unit)
# Initialize special offers
supermarket.add_multi_price_offer("A", 3, 130)
supermarket.add_multi_price_offer("A", 5, 200)
supermarket.add_multi_price_offer("B", 2, 45)
supermarket.add_buy_many_get_some_free("E", 2, "B", 1)
supermarket.add_buy_many_get_some_free("F", 2, "F", 1)
supermarket.add_multi_price_offer("H", 5, 45)
supermarket.add_multi_price_offer("H", 10, 80)
supermarket.add_multi_price_offer("K", 2, 150)
supermarket.add_buy_many_get_some_free("N", 3, "M", 1)
supermarket.add_multi_price_offer("P", 5, 200)
supermarket.add_multi_price_offer("Q", 3, 80)
supermarket.add_buy_many_get_some_free("R", 3, "Q", 1)
supermarket.add_buy_many_get_some_free("U", 3, "U", 1)
supermarket.add_multi_price_offer("V", 2, 90)
supermarket.add_multi_price_offer("V", 3, 130)
supermarket.add_group_discount_offer("STXYZ", 3, 45)


# skus = unicode string
def checkout(skus: str) -> Price:
    total = 0
    counts = Counter(skus)
    supermarket.apply_cart_discounts(counts)
    for sku, count in counts.items():
        try:
            total += supermarket.get_price(sku, count)
        except KeyError:
            return -1
    return total

