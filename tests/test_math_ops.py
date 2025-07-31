from services.math_ops import compute_pow, compute_fibonacci, compute_factorial

def test_compute_pow():
    assert compute_pow(2, 3) == 8
    assert compute_pow(5, 0) == 1
    assert compute_pow(9, 0.5) == 3

def test_compute_fibonacci():
    assert compute_fibonacci(0) == 0
    assert compute_fibonacci(1) == 1
    assert compute_fibonacci(10) == 55

def test_compute_factorial():
    assert compute_factorial(0) == 1
    assert compute_factorial(1) == 1
    assert compute_factorial(5) == 120