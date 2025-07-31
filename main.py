import io
import csv
import uuid
from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from api.routes import router
from services.math_ops import compute_pow, compute_fibonacci, compute_factorial
from storage.sqlite_store import init_db, store_request_sqlite, get_all_requests_sqlite
from services.background_tasks import store_and_compute_fibonacci, store_and_compute_factorial, store_and_compute_pow
from math import log10
from storage.task_store import init_task_db, get_task, get_all_tasks

import sys

sys.set_int_max_str_digits(25000)

init_db()
init_task_db()


app = FastAPI(title="Math Microservice")
app.include_router(router)

templates = Jinja2Templates(directory="templates")

MAX_DISPLAY_DIGITS = 300

def summarize_result(result: int | float | str) -> str:
    try:
        s = str(result)
        if len(s) > MAX_DISPLAY_DIGITS:
            return f"{s[:MAX_DISPLAY_DIGITS]}... [{len(s)} digits total]"
        return s
    except Exception:
        return "[unrepresentable result]"


@app.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@app.post("/", response_class=HTMLResponse)
def post_form(
    request: Request,
    background_tasks: BackgroundTasks,
    op_type: str = Form(...),
    a: int = Form(0),
    b: int = Form(0)
):
    if op_type == "pow":
        # Estimate digit count for a ** b
        if a > 0 and b > 0:
            est_digits = int(b * log10(a)) + 1
        else:
            est_digits = 1
        if est_digits < 3000:
            result = compute_pow(a, b)
            store_request_sqlite("pow", {"base": a, "exponent": b}, result)
        else:
            task_id = str(uuid.uuid4())
            background_tasks.add_task(store_and_compute_pow, a, b, task_id)
            result = (
                f"Task {task_id} started: Calculating {a}^{b} (~{est_digits} digits) in background... "
                f'<a href="/status/{task_id}" target="_blank" class="btn btn-sm btn-outline-info mt-1">Check status</a>'
            )

    elif op_type == "fibonacci":
        if a < 5000:
            result = compute_fibonacci(a)
            store_request_sqlite("fibonacci", {"n": a}, result)
        else:
            task_id = str(uuid.uuid4())
            background_tasks.add_task(store_and_compute_fibonacci, a, task_id)
            result = (
                f"Task {task_id} started: Calculating Fibonacci({a}) in background... "
                f'<a href="/status/{task_id}" target="_blank" class="btn btn-sm btn-outline-info mt-1">Check status</a>'
            )

    elif op_type == "factorial":
        if a < 3000:
            result = compute_factorial(a)
            store_request_sqlite("factorial", {"n": a}, result)
        else:
            task_id = str(uuid.uuid4())
            background_tasks.add_task(store_and_compute_factorial, a, task_id)
            result = (
                f"Task {task_id} started: Calculating Factorial({a}) in background... "
                f'<a href="/status/{task_id}" target="_blank" class="btn btn-sm btn-outline-info mt-1">Check status</a>'
            )
    else:
        result = "Invalid operation"

    return templates.TemplateResponse(
    request,
    "index.html",
    {
        "result": summarize_result(result),
        "op_type": op_type
    }
)

@app.get("/history/export")
def export_history():
    history = get_all_requests_sqlite()
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Operation', 'Input', 'Result', 'Timestamp'])
    cw.writerows(history)
    si.seek(0)
    return StreamingResponse(
        si,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=history.csv"}
    )


@app.get("/status/{task_id}")
def get_task_status(task_id: str):
    task = get_task(task_id)
    if task:
        return task
    return {"task_id": task_id, "status": "not found"}

@app.get("/tasks", response_class=HTMLResponse)
def view_tasks(request: Request):
    tasks = get_all_tasks()
    return templates.TemplateResponse(
        request,
        "tasks.html",
        {"tasks": tasks}
    )