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


def test_checkout_offer_combined_groups():
    assert checkout_solution.checkout("AAAAAAAA") == 200+130


def test_checkout_offer_combined_groups_2():
    assert checkout_solution.checkout("AAAAAAAAA") == 200+130+50


def test_checkout_offer_mixed():
    assert checkout_solution.checkout("ABABAA") == 130+45+50


def test_checkout_get_one_free_offer():
    assert checkout_solution.checkout("EE") == 40*2
    assert checkout_solution.checkout("EEB") == 40*2  # B is free


def test_checkout_get_many_free_offer():
    assert checkout_solution.checkout("EEEEBB") == 40*4  # 2xB are free


def test_checkout_group_discount():
    assert checkout_solution.checkout("SSS") == 45


def test_checkout_group_discount_mixed():
    assert checkout_solution.checkout("STX") == 45


def test_checkout_group_discount_leftover():
    # we pay a group and the Y, which is cheapest
    assert checkout_solution.checkout("YSTX") == 45 + 17


def test_checkout_group_discount_repeat():
    assert checkout_solution.checkout("STXYSTX") == 2*45+17



def test_checkout_get_one_free_combined():
    # In this scenario one B is free, the other pays unit price
    assert checkout_solution.checkout("EEBB") == 40*2 + 30
    # In this scenario one B is free, the other gets multi-price offer
    assert checkout_solution.checkout("EEBBB") == 40*2 + 45


def test_checkout_get_one_free_same():
    assert checkout_solution.checkout("FFF") == checkout_solution.checkout("FF") == 20
    assert checkout_solution.checkout("FFFF") == 30
    assert checkout_solution.checkout("FFFFF") == 40
    assert checkout_solution.checkout("FFFFFF") == 40
    assert checkout_solution.checkout("FFFFFFF") == 50
    assert checkout_solution.checkout("FFFFFFFF") == 60


def test_combined_discount_kinds():
    # Get one Q free, pay the other 2 unit price
    assert checkout_solution.checkout("RRRQQQ") == 3*50 + 2*30
    # Get one Q free, pay the other 3 special offer
    assert checkout_solution.checkout("RRRQQQQ") == 3*50 + 80


def test_checkout_invalid():
    assert checkout_solution.checkout("*") == -1


def test_checkout_partially_invalid():
    assert checkout_solution.checkout("A*") == -1


def test_get_best_price():
    assert checkout_solution.supermarket.get_price("A", 4) == 130+50


def test_get_best_price_no_offer():
    assert checkout_solution.supermarket.get_price("D", 42) == 42*15


def test_get_best_price_null():
    assert checkout_solution.supermarket.get_price("B", 0) == 0


def test_apply_discounts():
    cart = Counter("EEBBB")
    checkout_solution.supermarket.apply_cart_discounts(cart)
    assert cart["B"] == 2  # One was free


def test_apply_discounts_no_matching_offer():
    cart = Counter("AABBB")
    checkout_solution.supermarket.apply_cart_discounts(cart)
    # No changes
    assert cart["A"] == 2
    assert cart["B"] == 3


def test_apply_discounts_no_free_items_asked():
    cart = Counter("EE")
    checkout_solution.supermarket.apply_cart_discounts(cart)
    # No changes
    assert cart["E"] == 2
    assert cart["B"] == 0


def test_external_tests():
    # These came from my first deploy run on R2
    assert checkout_solution.checkout("") == 0
    assert checkout_solution.checkout("A") == 50
    assert checkout_solution.checkout("B") == 30
    assert checkout_solution.checkout("C") == 20
    assert checkout_solution.checkout("D") == 15
    assert checkout_solution.checkout("E") == 40
    assert checkout_solution.checkout("a") == -1
    assert checkout_solution.checkout("-") == -1
    assert checkout_solution.checkout("ABCa") == -1
    assert checkout_solution.checkout("AxA") == -1
    assert checkout_solution.checkout("ABCDE") == 155
    assert checkout_solution.checkout("A") == 50
    assert checkout_solution.checkout("AA") == 100
    assert checkout_solution.checkout("AAA") == 130
    assert checkout_solution.checkout("AAAA") == 180
    assert checkout_solution.checkout("AAAAA") == 200
    assert checkout_solution.checkout("AAAAAA") == 250
    assert checkout_solution.checkout("AAAAAAA") == 300
    assert checkout_solution.checkout("AAAAAAAA") == 330
    assert checkout_solution.checkout("AAAAAAAAA") == 380
    assert checkout_solution.checkout("AAAAAAAAAA") == 400
    assert checkout_solution.checkout("EE") == 80
    assert checkout_solution.checkout("EEB") == 80
    assert checkout_solution.checkout("EEEB") == 120
    assert checkout_solution.checkout("EEEEBB") == 160
    assert checkout_solution.checkout("BEBEEE") == 160
    assert checkout_solution.checkout("A") == 50
    assert checkout_solution.checkout("AA") == 100
    assert checkout_solution.checkout("AAA") == 130
    assert checkout_solution.checkout("AAAA") == 180
    assert checkout_solution.checkout("AAAAA") == 200
    assert checkout_solution.checkout("AAAAAA") == 250
    assert checkout_solution.checkout("B") == 30
    assert checkout_solution.checkout("BB") == 45
    assert checkout_solution.checkout("BBB") == 75
    assert checkout_solution.checkout("BBBB") == 90
    assert checkout_solution.checkout("ABCDEABCDE") == 280
    assert checkout_solution.checkout("CCADDEEBBA") == 280
    assert checkout_solution.checkout("AAAAAEEBAAABB") == 455
    assert checkout_solution.checkout("ABCDECBAABCABBAAAEEAA") == 665


def test_external_tests_r5():
    assert checkout_solution.checkout("KK") == 120
    assert checkout_solution.checkout("KKK") == 190
    assert checkout_solution.checkout("KKKK") == 240



