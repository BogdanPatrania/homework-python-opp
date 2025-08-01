import uuid
from fastapi import APIRouter, BackgroundTasks, Query, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.request_models import PowRequest
from models.response_models import ResultResponse
from services.math_ops import compute_pow, compute_fibonacci, compute_factorial
from services.background_tasks import store_and_compute_fibonacci
from storage.memory_store import store_request
from storage.sqlite_store import store_request_sqlite, get_all_requests_sqlite
from services.auth import authorize_combined, ensure_logged_in
from storage.task_store import get_all_tasks

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/pow", response_model=ResultResponse)
def pow_endpoint(req: PowRequest, _=Depends(authorize_combined)):
    result = compute_pow(req.base, req.exponent)
    store_request("pow", req.model_dump(), result)
    store_request_sqlite("pow", req.model_dump(), result)
    return {"result": result}


@router.get("/fibonacci", response_model=ResultResponse)
def fibonacci_endpoint(
    n: int = Query(..., ge=0),
    background_tasks: BackgroundTasks = None,
    _=Depends(authorize_combined)
):
    task_id = str(uuid.uuid4())
    background_tasks.add_task(store_and_compute_fibonacci, n, task_id)
    return {
        "result": f"Task {task_id} started: Calculating Fibonacci({n}) in background... Check status at /status/{task_id}"
    }


@router.get("/factorial", response_model=ResultResponse)
def factorial_endpoint(
    n: int = Query(..., ge=0),
    _=Depends(authorize_combined)
):
    result = compute_factorial(n)
    store_request("factorial", {"n": n}, result)
    store_request_sqlite("factorial", {"n": n}, result)
    return {"result": result}


@router.get("/history", response_class=HTMLResponse)
def view_history(
    request: Request,
    mode: str = Query("all"),
    operation: str = Query(None),
):
    auth_result = ensure_logged_in(request)
    if auth_result is not None:
        return auth_result

    all_history = get_all_requests_sqlite()
    if mode == "last10":
        history = all_history[:10]
    elif mode == "filter" and operation:
        history = [entry for entry in all_history if entry[1] == operation]
    else:
        history = all_history

    return templates.TemplateResponse(
        request,
        "history.html",
        {
            "history": history,
            "mode": mode,
            "operation": operation or ""
        }
    )

@router.get("/tasks", response_class=HTMLResponse)
def view_tasks(request: Request):
    auth_result = ensure_logged_in(request)
    if auth_result is not None:
        return auth_result

    tasks = get_all_tasks()
    return templates.TemplateResponse(
        request,
        "tasks.html",
        {"tasks": tasks}
    )