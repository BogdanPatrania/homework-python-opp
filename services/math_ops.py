from functools import lru_cache

@lru_cache(maxsize=128)
def compute_pow(base: float, exp: float) -> float:
    return base ** exp

@lru_cache(maxsize=512)
def compute_fibonacci(n: int) -> int:
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

@lru_cache(maxsize=512)
def compute_factorial(n: int) -> int:
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
