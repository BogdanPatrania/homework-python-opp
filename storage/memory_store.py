from typing import List, Dict

memory_db: List[Dict] = []


def store_request(operation: str, input_data: dict, result: float | int):
    memory_db.append({
        "operation": operation,
        "input": input_data,
        "result": result
    })


def get_all_requests() -> List[Dict]:
    return memory_db
