import io
import csv
import uuid
import os
import sys
from math import log10
from dotenv import load_dotenv
from fastapi import (
    FastAPI, Request, Form, BackgroundTasks,
    HTTPException, status, Depends
)
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.openapi.docs import get_swagger_ui_html
from api.routes import router
from services.math_ops import compute_pow, compute_fibonacci, compute_factorial
from services.background_tasks import (
    store_and_compute_fibonacci,
    store_and_compute_factorial,
    store_and_compute_pow
)
from storage.sqlite_store import (
    init_db, store_request_sqlite, get_all_requests_sqlite
)
from storage.task_store import (
    init_task_db, get_task, get_all_tasks
)
from services.auth import (
    authorize, ensure_logged_in, set_session, USERNAME, PASSWORD
)

# Increase int string limit
sys.set_int_max_str_digits(25000)

# Initialize DBs
init_db()
init_task_db()

# App + templates
app = FastAPI(
    title="Math Microservice",
    docs_url=None,         # Disable default /docs
    redoc_url=None,        # Disable default /redoc
    openapi_url=None       # Disable default /openapi.json
)
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

@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login_submit(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == USERNAME and password == PASSWORD:
        response = RedirectResponse(url="/", status_code=302)
        session_token = set_session(username)
        response.set_cookie("session", session_token, httponly=True)
        return response
    return templates.TemplateResponse("login.html", {
        "request": request,
        "error": "Invalid username or password"
    })

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("session")
    return response

@app.get("/", response_class=HTMLResponse)
def get_form(request: Request):
    auth_result = ensure_logged_in(request)
    if isinstance(auth_result, RedirectResponse):
        return auth_result
    return templates.TemplateResponse(request, "index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
def post_form(
    request: Request,
    background_tasks: BackgroundTasks,
    op_type: str = Form(...),
    a: int = Form(0),
    b: int = Form(0),
    _=Depends(ensure_logged_in)
):
    if op_type == "pow":
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
def export_history(_=Depends(authorize)):
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

@app.get("/docs", include_in_schema=False)
def custom_swagger_ui(request: Request):
    auth_result = ensure_logged_in(request)
    if auth_result is not None:
        return auth_result
    return get_swagger_ui_html(openapi_url=app.openapi_url, title=app.title + " - Docs")

@app.get("/openapi.json", include_in_schema=False)
def custom_openapi(request: Request):
    auth_result = ensure_logged_in(request)
    if auth_result is not None:
        return auth_result
    return app.openapi()