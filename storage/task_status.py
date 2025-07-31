from threading import Lock

_task_status = {}
task_results = {}
_lock = Lock()

def set_status(task_id: str, status: str):
    with _lock:
        _task_status[task_id] = status

def get_status(task_id: str) -> str:
    with _lock:
        return _task_status.get(task_id, "unknown")

def set_result(task_id: str, result):
    with _lock:
        task_results[task_id] = result

def get_result(task_id: str):
    with _lock:
        return task_results.get(task_id)