from collections import Counter

from solutions.CHK import checkout_solution


def test_checkout_single():
    assert checkout_solution.checkout("A") == 50


def test_checkout_empty():
    assert checkout_solution.checkout("") == 0


def test_checkout_multiple():
    assert checkout_solution.checkout("ABCD") == 50+30+20+15


def test_checkout_offer():
    assert checkout_solution.checkout("AAA") == 130


def test_checkout_offer_partial():
    assert checkout_solution.checkout("AAAA") == 130+50


def test_checkout_offer_mixed():
    assert checkout_solution.checkout("ABABAA") == 130+45+50


def test_checkout_get_one_free_offer():
    assert checkout_solution.checkout("EE") == 40*2
    assert checkout_solution.checkout("EEB") == 40*2  # B is free


def test_checkout_get_many_free_offer():
    assert checkout_solution.checkout("EEEEBB") == 40*4  # 2xB are free


def test_checkout_get_one_free_combined():
    # In this scenario one B is free, the other pays unit price
    assert checkout_solution.checkout("EEBB") == 40*2 + 30
    # In this scenario one B is free, the other gets multi-price offer
    assert checkout_solution.checkout("EEBBB") == 40*2 + 45


def test_checkout_invalid():
    assert checkout_solution.checkout("X") == -1


def test_checkout_partially_invalid():
    assert checkout_solution.checkout("AX") == -1


def test_get_best_price():
    assert checkout_solution.get_best_price("A", 4) == 130+50


def test_get_best_price_no_offer():
    assert checkout_solution.get_best_price("D", 42) == 42*15


def test_apply_discounts():
    cart = Counter("EEBBB")
    checkout_solution.apply_cart_discounts(cart)
    assert cart["B"] == 2  # One was free


def test_apply_discounts_no_matching_offer():
    cart = Counter("AABBB")
    checkout_solution.apply_cart_discounts(cart)
    # No changes
    assert cart["A"] == 2
    assert cart["B"] == 3


def test_apply_discounts_no_free_items_asked():
    cart = Counter("EE")
    checkout_solution.apply_cart_discounts(cart)
    # No changes
    assert cart["E"] == 2
    assert cart["B"] == 0


