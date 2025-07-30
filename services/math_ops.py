
def compute_pow(base: float, exponent: float) -> float:
    return base ** exponent


def compute_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n+1):
        a, b = b, a + b
    return b


def compute_factorial(n: int) -> int:
    result = 1
    for i in range(2, n+1):
        result *= i
    return result
