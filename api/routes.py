import uuid
from fastapi import APIRouter, BackgroundTasks, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models.request_models import PowRequest
from models.response_models import ResultResponse
from services.math_ops import compute_pow, compute_fibonacci, compute_factorial
from services.background_tasks import store_and_compute_fibonacci
from storage.memory_store import store_request
from storage.sqlite_store import store_request_sqlite, get_all_requests_sqlite


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post("/pow", response_model=ResultResponse)
def pow_endpoint(req: PowRequest):
    result = compute_pow(req.base, req.exponent)
    store_request("pow", req.model_dump(), result)
    store_request_sqlite("pow", req.model_dump(), result)
    return {"result": result}


@router.get("/fibonacci", response_model=ResultResponse)
def fibonacci_endpoint(
    n: int = Query(..., ge=0),
    background_tasks: BackgroundTasks = None
):
    task_id = str(uuid.uuid4())
    background_tasks.add_task(store_and_compute_fibonacci, n, task_id)
    return {"result": f"Task {task_id} started: Calculating Fibonacci({n}) in background... Check status at /status/{task_id}"}


@router.get("/factorial", response_model=ResultResponse)
def factorial_endpoint(n: int = Query(..., ge=0)):
    result = compute_factorial(n)
    store_request("factorial", {"n": n}, result)
    store_request_sqlite("factorial", {"n": n}, result)
    return {"result": result}

@router.get("/history", response_class=HTMLResponse)
def view_history(
    request: Request,
    mode: str = Query("all"),  # 'all', 'last10', or 'filter'
    operation: str = Query(None)
):
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