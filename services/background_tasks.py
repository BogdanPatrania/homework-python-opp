from services.math_ops import compute_factorial, compute_fibonacci, compute_pow
from storage.sqlite_store import store_request_sqlite
from storage.task_store import save_task, update_task_status, update_task_result

def store_and_compute_fibonacci(n: int, task_id: str):
    save_task(task_id, "fibonacci", {"n": n})
    update_task_status(task_id, "in_progress")
    result = compute_fibonacci(n)
    store_request_sqlite("fibonacci", {"n": n}, result)
    update_task_result(task_id, result)

def store_and_compute_factorial(n: int, task_id: str):
    save_task(task_id, "factorial", {"n": n})
    update_task_status(task_id, "in_progress")
    result = compute_factorial(n)
    store_request_sqlite("factorial", {"n": n}, result)
    update_task_result(task_id, result)

def store_and_compute_pow(a: float, b: float, task_id: str):
    save_task(task_id, "pow", {"base": a, "exponent": b})
    update_task_status(task_id, "in_progress")
    result = compute_pow(a, b)
    store_request_sqlite("pow", {"base": a, "exponent": b}, result)
    update_task_result(task_id, result)