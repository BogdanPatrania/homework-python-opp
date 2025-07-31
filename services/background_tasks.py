from services.math_ops import compute_factorial, compute_fibonacci, compute_pow
from storage.sqlite_store import store_request_sqlite
from storage.task_status import set_status, set_result

def store_and_compute_fibonacci(n: int, task_id: str):
    set_status(task_id, "in_progress")
    result = compute_fibonacci(n)
    store_request_sqlite("fibonacci", {"n": n}, result)
    set_result(task_id, result)
    set_status(task_id, "done")

def store_and_compute_factorial(n: int, task_id: str):
    set_status(task_id, "in_progress")
    result = compute_factorial(n)
    store_request_sqlite("factorial", {"n": n}, result)
    set_result(task_id, result)
    set_status(task_id, "done")

def store_and_compute_pow(a: float, b: float, task_id: str):
    set_status(task_id, "in_progress")
    result = compute_pow(a, b)
    store_request_sqlite("pow", {"base": a, "exponent": b}, result)
    set_result(task_id, result)
    set_status(task_id, "done")