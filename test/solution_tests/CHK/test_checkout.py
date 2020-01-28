from solutions.CHK import checkout_solution


def test_checkout_single():
    assert checkout_solution.checkout("A") == 50


def test_checkout_empty():
    assert checkout_solution.checkout("") == 0


def test_checkout_multiple():
    assert checkout_solution.checkout("ABCD") == 50+30+20+15


def test_checkout_promotion():
    assert checkout_solution.checkout("AAA") == 130


def test_checkout_promotion_PARTIAL():
    assert checkout_solution.checkout("AAAA") == 130+50



