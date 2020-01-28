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


def test_checkout_best_price():
    assert checkout_solution.get_best_price("A", 4) == 130+50


def test_checkout_best_price_no_offer():
    assert checkout_solution.get_best_price("D", 42) == 42*15
